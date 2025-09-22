#![deny(missing_docs)]
//! Python bindings for the afrim input method engine.

mod preprocessor;
mod translator;

pub use preprocessor::Preprocessor;
pub use translator::Translator;

use pyo3::prelude::*;
use toml;

/// Convert TOML to JSON (returns JSON string).
///
/// Example:
/// ```python
/// convert_toml_to_json("[info]\nname = 'sample'\n[data]\nhello = 'hi'")
/// ```
#[pyfunction]
fn convert_toml_to_json(content: &str) -> PyResult<String> {
    let data: toml::Value = toml::from_str(content)
        .map_err(|err| pyo3::exceptions::PyValueError::new_err(format!("Invalid TOML data.\nCaused by:\n\t{err}")))?;
    serde_json::to_string(&data)
        .map_err(|err| pyo3::exceptions::PyValueError::new_err(format!("Serialization error: {err}")))
}

/// Python module definition
#[pymodule]
fn afrim_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Preprocessor>()?;
    m.add_class::<Translator>()?;
    m.add_function(wrap_pyfunction!(convert_toml_to_json, m)?)?;
    Ok(())
}