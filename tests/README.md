# Test Suite for afrim-py

This directory contains comprehensive tests for the afrim-py Python bindings.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest configuration and fixtures
├── test_toml_converter.py   # Tests for TOML to JSON conversion
├── test_preprocessor.py     # Tests for Preprocessor class
├── test_translator.py       # Tests for Translator class
├── test_integration.py      # Integration tests
└── README.md               # This file
```

## Running Tests

### Quick Start
```bash
# Activate virtual environment
source .venv/bin/activate

# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=afrim_py --cov-report=term-missing
```

### Using the Test Runner
```bash
# Activate virtual environment
source .venv/bin/activate

# Run the comprehensive test suite
python run_tests.py
```

## Test Categories

### Unit Tests

#### `test_toml_converter.py`
- Tests for `convert_toml_to_json()` function
- Covers simple and complex TOML structures
- Tests error handling for malformed TOML
- Unicode and multiline string support

#### `test_preprocessor.py`
- Tests for `Preprocessor` class initialization and methods
- Key processing (`process()`, `commit()`, `get_input()`)
- Queue operations (`pop_queue()`, `clear_queue()`)
- Edge cases and error conditions
- Unicode key handling

#### `test_translator.py`
- Tests for `Translator` class initialization and methods
- Translation functionality (`translate()`)
- Dictionary handling with various data types
- Error conditions and edge cases
- Unicode translation support

### Integration Tests

#### `test_integration.py`
- Tests component interactions
- TOML → Preprocessor → Translator workflows
- Error handling across components
- Performance and memory management tests
- Complete input method simulation

## Test Fixtures

The `conftest.py` file provides reusable test fixtures:

- `sample_preprocessor_data`: Standard preprocessor mappings
- `sample_translator_dict`: Standard translation dictionary
- `sample_toml_config`: TOML configuration for testing
- `complex_unicode_data`: Unicode test data

## Coverage

The test suite achieves 100% coverage of the Python bindings:

```
Name                                                      Stmts   Miss  Cover
-----------------------------------------------------------------------------
.venv/lib/python3.12/site-packages/afrim_py/__init__.py     4      0   100%
-----------------------------------------------------------------------------
TOTAL                                                        4      0   100%
```

## Test Configuration

### `pytest.ini`
- Configures test discovery patterns
- Sets up markers for test categorization
- Configures output formatting

### Markers
- `integration`: Integration tests
- `slow`: Slow-running tests
- `unit`: Unit tests

## Known Issues

### Unicode Limitations
Some complex Unicode characters (like Arabic script or certain CJK characters) may cause panics in the underlying Rust library. Tests have been designed to avoid these problematic characters while still testing Unicode support with safer characters like accented Latin letters and emojis.

### Skipped Tests
- `test_register_unregister_functionality`: Skipped when the `rhai` feature is not enabled in the Rust build

## Contributing

When adding new tests:

1. Follow the existing naming conventions
2. Use appropriate test fixtures from `conftest.py`
3. Add docstrings explaining what each test does
4. Consider both positive and negative test cases
5. Test edge cases and error conditions
6. Update this README if adding new test categories

## Running Specific Tests

```bash
# Run only unit tests
python -m pytest tests/test_*.py -v

# Run only integration tests  
python -m pytest tests/test_integration.py -v

# Run tests matching a pattern
python -m pytest -k "unicode" -v

# Run tests with specific markers
python -m pytest -m "not slow" -v
```
