#![deny(missing_docs)]
/// Python binding of the afrim translator.
use afrim_config::Config as NativeConfig;
use pyo3::prelude::*;
use pythonize::pythonize;
use serde_json::{self};
use std::collections::HashMap;
use std::path::Path;

/// Core structure of the config
#[pyclass]
#[derive(Clone)]
pub struct Config {
    /// The size of the memory (history).
    /// The number of elements that should be tracked.
    pub buffer_size: Option<usize>,
    /// The max numbers of predicates to display.
    pub page_size: Option<usize>,
    /// Whether the predicate should be automatically committed.
    pub auto_commit: Option<bool>,
    pub(crate) engine: NativeConfig,
}

#[pymethods]
impl Config {
    /// Initialize the config.
    #[new]
    pub fn new(config_file: String) -> PyResult<Self> {
        let config_file = Path::new(&config_file);
        let engine = NativeConfig::from_file(config_file).map_err(|err| {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Failed to load config file `{config_file:?}`.\nCaused by:\n\t{err}"
            ))
        })?;

        Ok(Self {
            buffer_size: engine.core.as_ref().and_then(|c| c.buffer_size),
            page_size: engine.core.as_ref().and_then(|c| c.page_size),
            auto_commit: engine.core.as_ref().and_then(|c| c.auto_commit),
            engine,
        })
    }

    /// Extracts the data from the configuration.
    pub fn extract_data(&self, py: Python) -> PyResult<PyObject> {
        let value = serde_json::to_value(self.engine.extract_data()).unwrap();
        pythonize(py, &value).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
    }

    /// Extracts the translation from the configuration.
    pub fn extract_translation(&self, py: Python) -> PyResult<PyObject> {
        let value = serde_json::to_value(self.engine.extract_translation()).unwrap();

        pythonize(py, &value).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
    }
}
