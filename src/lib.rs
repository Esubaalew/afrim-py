#![deny(missing_docs)]
//! Python bindings for the afrim input method engine.

mod config;
mod preprocessor;
mod translator;

pub use config::Config;
pub use preprocessor::Preprocessor;
pub use translator::Translator;

use pyo3::prelude::*;

#[pyfunction]
fn is_rhai_feature_enabled() -> bool {
    cfg!(feature = "rhai")
}

#[pyfunction]
fn is_strsim_feature_enabled() -> bool {
    cfg!(feature = "strsim")
}

/// Python module definition
#[pymodule]
fn afrim_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Preprocessor>()?;
    m.add_class::<Translator>()?;
    m.add_class::<Config>()?;
    m.add_function(wrap_pyfunction!(is_rhai_feature_enabled, m)?)?;
    m.add_function(wrap_pyfunction!(is_strsim_feature_enabled, m)?)?;

    Ok(())
}
