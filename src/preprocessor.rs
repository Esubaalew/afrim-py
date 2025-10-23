#![deny(missing_docs)]
/// Python binding of the afrim preprocessor.
use afrim_preprocessor::Preprocessor as NativePreprocessor;
use pyo3::prelude::*;
use pythonize::pythonize;
use serde_json::Value;
use std::collections::HashMap;

/// Core structure of the preprocessor.
///
/// Marked `unsendable` because the native Preprocessor contains `Rc` internals
/// (not `Send`), which is fine for single-thread Python usage.
#[pyclass(unsendable)]
pub struct Preprocessor {
    engine: NativePreprocessor,
}

#[pymethods]
impl Preprocessor {
    /// Initialize the preprocessor
    ///
    /// `data` is a Python dict (str -> str) which will be converted to the
    /// native map expected by afrim_preprocessor.
    #[new]
    fn new(data: HashMap<String, String>, buffer_size: usize) -> PyResult<Self> {
        let data_vec: Vec<Vec<&str>> = data
            .iter()
            .map(|(k, v)| vec![k.as_str(), v.as_str()])
            .collect();
        let native_map = afrim_preprocessor::utils::build_map(data_vec);
        Ok(Self {
            engine: NativePreprocessor::new(native_map.into(), buffer_size),
        })
    }

    /// Process a keyboard event (key string, state "keydown"|"keyup")
    fn process(&mut self, key: &str, state: &str) -> PyResult<bool> {
        let event = crate::preprocessor::utils::deserialize_event(key, state)
            .map_err(pyo3::exceptions::PyValueError::new_err)?;
        let (changed, _) = self.engine.process(event);
        Ok(changed)
    }

    /// Commit text
    fn commit(&mut self, text: String) {
        self.engine.commit(text);
    }

    /// Pop next command; returns a JSON-like Python object (serde_json::Value)
    fn pop_queue(&mut self, py: Python) -> PyResult<PyObject> {
        let value = self
            .engine
            .pop_queue()
            .as_ref()
            .map(|v| serde_json::to_value(v).unwrap())
            .unwrap_or(Value::String("NOP".into()));
        pythonize(py, &value).map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
    }

    /// Get input from memory
    fn get_input(&self) -> String {
        self.engine.get_input()
    }

    /// Clear queue
    fn clear_queue(&mut self) {
        self.engine.clear_queue();
    }
}

/// utils (local to this module) re-exporting the original utils and a small helper.
pub mod utils {
    use afrim_preprocessor::{Key, KeyState, KeyboardEvent};
    use std::str::FromStr;

    pub fn deserialize_event(key: &str, state: &str) -> Result<KeyboardEvent, String> {
        let event = KeyboardEvent {
            key: Key::from_str(key)
                .map_err(|err| format!("Unrecognized key.\nCaused by:\n\t{err:?}"))?,
            state: match state {
                "keydown" => KeyState::Down,
                "keyup" => KeyState::Up,
                _ => return Err(format!("Unrecognized state `{state}`.")),
            },
            ..Default::default()
        };
        Ok(event)
    }
}
