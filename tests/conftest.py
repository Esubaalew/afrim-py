"""Pytest configuration and fixtures for afrim-py tests."""

import pytest


@pytest.fixture
def sample_preprocessor_data():
    """Sample data for Preprocessor tests."""
    return {
        "a1": "à",
        "ae": "æ", 
        "oe": "œ",
        "hello": "hi",
        "test": "result"
    }


@pytest.fixture
def sample_translator_dict():
    """Sample dictionary for Translator tests."""
    return {
        "hello": ["hi", "hey", "greetings"],
        "world": ["earth", "globe", "planet"],
        "bye": ["goodbye", "farewell", "see you"],
        "test": ["result", "outcome"],
        "café": ["coffee", "☕"]
    }


@pytest.fixture
def sample_toml_config():
    """Sample TOML configuration for testing."""
    return '''
[info]
name = "afrim-test"
version = "1.0.0"

[preprocessor]
a1 = "à"
ae = "æ"
hello = "hi"

[translator.hello]
values = ["hi", "hey"]

[translator.world]
values = ["earth", "globe"]
'''


@pytest.fixture
def complex_unicode_data():
    """Complex Unicode data for testing."""
    return {
        "preprocessor": {
            "cafe": "café",
            "naive": "naïve",
            "emoji1": "🚀",
            "resume": "résumé"
        },
        "translator": {
            "café": ["coffee", "☕"],
            "🚀": ["rocket", "spaceship"],
            "naïve": ["innocent", "simple"],
            "résumé": ["CV", "summary"]
        }
    }
