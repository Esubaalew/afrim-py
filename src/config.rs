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
pub struct Config {
    /// The size of the memory (history).
    /// The number of elements that should be tracked.
    pub buffer_size: Option<usize>,
    /// The max numbers of predicates to display.
    pub page_size: Option<usize>,
    /// Whether the predicate should be automatically committed.
    pub auto_commit: Option<bool>,
    config: NativeConfig,
}

#[pymethods]
impl Config {
    /// Initialize the config.
    #[new]
    pub fn new(config_file: String) -> PyResult<Self> {
        let config_file = Path::new(&config_file);
        let config = NativeConfig::from_file(config_file).map_err(|err| {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Failed to load config file `{config_file:?}`.\nCaused by:\n\t{err}"
            ))
        })?;

        Ok(Self {
            buffer_size: config.core.as_ref().and_then(|c| c.buffer_size),
            page_size: config.core.as_ref().and_then(|c| c.page_size),
            auto_commit: config.core.as_ref().and_then(|c| c.auto_commit),
            config,
        })
    }

    /// Extracts the data from the configuration.
    pub fn extract_data(&self, py: Python) -> PyResult<PyObject> {
        let value = serde_json::to_value(self.config.extract_data()).unwrap();
        pythonize(py, &value).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
    }

    /// Extracts the translation from the configuration.
    pub fn extract_translation(&self, py: Python) -> PyResult<PyObject> {
        let value = serde_json::to_value(self.config.extract_translation()).unwrap();

        pythonize(py, &value).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
    }

    /// Extracts the translators from the configuration.
    #[cfg(feature = "rhai")]
    pub fn extract_translators(&self, py: Python) -> PyResult<PyObject> {
        let translators = self.config.extract_translators().map_err(|err| {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Failed to load the translators`.\nCaused by:\n\t{err}"
            ))
        })?;
        let translators = translators
            .into_iter()
            .map(|(k, v)| (k, format!("{v:?}")))
            .collect::<HashMap<String, String>>();
        let value = serde_json::to_value(&translators).unwrap();

        pythonize(py, &value).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
    }
}
