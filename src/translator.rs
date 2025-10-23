#![deny(missing_docs)]
//! Python binding of the afrim translator.

#[cfg(feature = "rhai")]
use afrim_translator::Engine;
use afrim_translator::Translator as NativeTranslator;
use indexmap::IndexMap;
use pyo3::prelude::*;
use pythonize::pythonize;
use std::collections::HashMap;

/// Core structure of the translator
#[pyclass(unsendable)]
pub struct Translator {
    engine: NativeTranslator,
}

#[pymethods]
impl Translator {
    /// Initialize the translator.
    ///
    /// `dictionary` should be a Python dict: str -> list[str]
    #[new]
    fn new(dictionary: HashMap<String, Vec<String>>, auto_commit: bool) -> PyResult<Self> {
        // Convert HashMap into IndexMap expected by native translator
        let mut idx = IndexMap::new();
        for (k, v) in dictionary.into_iter() {
            idx.insert(k, v);
        }

        Ok(Self {
            engine: NativeTranslator::new(idx, auto_commit),
        })
    }

    /// Register a Rhai translator (requires `rhai` feature)
    #[cfg(feature = "rhai")]
    fn register(&mut self, name: String, source: String) -> PyResult<()> {
        let engine = Engine::new_raw();
        let ast = engine.compile(source).map_err(|err| {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Failed to register translator `{name}`.\nCaused by:\n\t{err}"
            ))
        })?;
        self.engine.register(name, ast);
        Ok(())
    }

    /// Unregister (requires `rhai` feature)
    #[cfg(feature = "rhai")]
    fn unregister(&mut self, name: &str) {
        self.engine.unregister(name);
    }

    /// Translate input — returns a serde_json::Value that maps nicely to Python types
    fn translate(&self, py: Python, input: &str) -> PyResult<PyObject> {
        let value = serde_json::to_value(self.engine.translate(input)).unwrap();
        pythonize(py, &value).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
    }
}
