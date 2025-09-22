"""Tests for TOML to JSON conversion functionality."""

import json
import pytest
from afrim_py import convert_toml_to_json


class TestTomlConverter:
    """Test cases for convert_toml_to_json function."""

    def test_simple_toml_conversion(self):
        """Test basic TOML to JSON conversion."""
        toml_input = '[data]\nhello="hi"'
        result = convert_toml_to_json(toml_input)
        expected = {"data": {"hello": "hi"}}
        
        assert json.loads(result) == expected

    def test_complex_toml_conversion(self):
        """Test complex TOML structure conversion."""
        toml_input = '''
[info]
name = "afrim"
version = "1.0.0"
author = "Test Author"

[data]
hello = "hi"
world = "earth"
numbers = [1, 2, 3]

[nested.section]
value = "nested_value"
boolean = true
'''
        result = convert_toml_to_json(toml_input)
        parsed = json.loads(result)
        
        assert parsed["info"]["name"] == "afrim"
        assert parsed["info"]["version"] == "1.0.0"
        assert parsed["data"]["hello"] == "hi"
        assert parsed["data"]["numbers"] == [1, 2, 3]
        assert parsed["nested"]["section"]["boolean"] is True

    def test_empty_toml(self):
        """Test empty TOML input."""
        result = convert_toml_to_json("")
        assert json.loads(result) == {}

    def test_toml_with_arrays(self):
        """Test TOML with arrays."""
        toml_input = '''
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = ["text", 42, true]
'''
        result = convert_toml_to_json(toml_input)
        parsed = json.loads(result)
        
        assert parsed["fruits"] == ["apple", "banana", "cherry"]
        assert parsed["numbers"] == [1, 2, 3, 4, 5]
        assert parsed["mixed"] == ["text", 42, True]

    def test_toml_with_dates(self):
        """Test TOML with date/time values."""
        toml_input = '''
date = 1979-05-27
datetime = 1979-05-27T07:32:00Z
'''
        result = convert_toml_to_json(toml_input)
        parsed = json.loads(result)
        
        # Dates should be converted to strings in JSON
        assert "date" in parsed
        assert "datetime" in parsed

    def test_invalid_toml_raises_error(self):
        """Test that invalid TOML raises ValueError."""
        invalid_toml = '[unclosed_section\nkey = "value"'
        
        with pytest.raises(ValueError, match="Invalid TOML data"):
            convert_toml_to_json(invalid_toml)

    def test_malformed_toml_raises_error(self):
        """Test that malformed TOML raises ValueError."""
        malformed_toml = 'key = "unclosed_string'
        
        with pytest.raises(ValueError, match="Invalid TOML data"):
            convert_toml_to_json(malformed_toml)

    def test_toml_with_unicode(self):
        """Test TOML with Unicode characters."""
        toml_input = '''
title = "TOML Example"
unicode_text = "Hello 世界 🌍"
emoji = "🚀 🎉 ✨"
'''
        result = convert_toml_to_json(toml_input)
        parsed = json.loads(result)
        
        assert parsed["unicode_text"] == "Hello 世界 🌍"
        assert parsed["emoji"] == "🚀 🎉 ✨"

    def test_toml_multiline_strings(self):
        """Test TOML with multiline strings."""
        toml_input = '''
multiline = """
This is a
multiline string
with multiple lines
"""
'''
        result = convert_toml_to_json(toml_input)
        parsed = json.loads(result)
        
        assert "This is a" in parsed["multiline"]
        assert "multiline string" in parsed["multiline"]
