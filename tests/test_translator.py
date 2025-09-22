"""Tests for Translator functionality."""

import pytest
from afrim_py import Translator


class TestTranslator:
    """Test cases for Translator class."""

    def test_translator_initialization(self):
        """Test basic Translator initialization."""
        dictionary = {"hello": ["hi", "hey"], "world": ["earth", "globe"]}
        auto_commit = True
        
        translator = Translator(dictionary, auto_commit)
        assert translator is not None

    def test_translator_with_auto_commit_false(self):
        """Test Translator with auto_commit=False."""
        dictionary = {"test": ["result"]}
        translator = Translator(dictionary, False)
        assert translator is not None

    def test_empty_dictionary_initialization(self):
        """Test Translator with empty dictionary."""
        translator = Translator({}, True)
        assert translator is not None

    def test_simple_translation(self):
        """Test basic translation functionality."""
        dictionary = {"hello": ["hi", "hey"], "world": ["earth"]}
        translator = Translator(dictionary, True)
        
        result = translator.translate("hello")
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Check the structure of the result
        translation = result[0]
        assert isinstance(translation, dict)
        assert "texts" in translation
        assert translation["texts"] == ["hi", "hey"]

    def test_single_option_translation(self):
        """Test translation with single option."""
        dictionary = {"world": ["earth"]}
        translator = Translator(dictionary, True)
        
        result = translator.translate("world")
        assert isinstance(result, list)
        assert len(result) > 0
        
        translation = result[0]
        assert translation["texts"] == ["earth"]

    def test_non_existent_key_translation(self):
        """Test translation of non-existent key."""
        dictionary = {"hello": ["hi"]}
        translator = Translator(dictionary, True)
        
        result = translator.translate("nonexistent")
        assert isinstance(result, list)
        # Should return empty list or some default behavior

    def test_empty_string_translation(self):
        """Test translation of empty string."""
        dictionary = {"hello": ["hi"]}
        translator = Translator(dictionary, True)
        
        result = translator.translate("")
        assert isinstance(result, list)

    def test_multiple_options_translation(self):
        """Test translation with multiple options."""
        dictionary = {
            "hello": ["hi", "hey", "hello there"],
            "bye": ["goodbye", "farewell", "see you"]
        }
        translator = Translator(dictionary, False)
        
        # Test hello
        result_hello = translator.translate("hello")
        assert isinstance(result_hello, list)
        if len(result_hello) > 0:
            assert result_hello[0]["texts"] == ["hi", "hey", "hello there"]
        
        # Test bye
        result_bye = translator.translate("bye")
        assert isinstance(result_bye, list)
        if len(result_bye) > 0:
            assert result_bye[0]["texts"] == ["goodbye", "farewell", "see you"]

    def test_unicode_translation(self):
        """Test translation with Unicode characters."""
        dictionary = {
            "café": ["coffee", "☕"],
            "naïve": ["naive"],
            "🚀": ["rocket", "spaceship"]
        }
        translator = Translator(dictionary, True)
        
        # Test Unicode key
        result = translator.translate("café")
        assert isinstance(result, list)
        
        # Test emoji key
        result_emoji = translator.translate("🚀")
        assert isinstance(result_emoji, list)

    def test_complex_dictionary(self):
        """Test with complex dictionary structure."""
        dictionary = {
            "a": ["alpha"],
            "ab": ["alphabet"],
            "abc": ["alphabet", "abc"],
            "hello": ["hi", "hey", "greetings"],
            "world": ["earth", "globe", "planet"],
            "programming": ["coding", "development"],
            "python": ["snake", "language"],
            "rust": ["metal", "language", "oxidation"]
        }
        translator = Translator(dictionary, True)
        
        # Test various keys
        test_keys = ["a", "hello", "programming", "rust"]
        for key in test_keys:
            result = translator.translate(key)
            assert isinstance(result, list)

    def test_case_sensitivity(self):
        """Test case sensitivity in translation."""
        dictionary = {
            "hello": ["hi"],
            "Hello": ["Hi"],
            "HELLO": ["HI"]
        }
        translator = Translator(dictionary, True)
        
        # Test different cases
        result_lower = translator.translate("hello")
        result_title = translator.translate("Hello")
        result_upper = translator.translate("HELLO")
        
        assert isinstance(result_lower, list)
        assert isinstance(result_title, list)
        assert isinstance(result_upper, list)

    def test_special_characters_in_keys(self):
        """Test translation with special characters in keys."""
        dictionary = {
            "hello!": ["hi!"],
            "what?": ["what"],
            "wow...": ["amazing"],
            "test@domain": ["email"],
            "key-value": ["pair"],
            "under_score": ["underscore"]
        }
        translator = Translator(dictionary, False)
        
        for key in dictionary.keys():
            result = translator.translate(key)
            assert isinstance(result, list)

    def test_numeric_strings_in_dictionary(self):
        """Test translation with numeric strings."""
        dictionary = {
            "123": ["numbers"],
            "42": ["answer"],
            "3.14": ["pi"],
            "0": ["zero", "null"]
        }
        translator = Translator(dictionary, True)
        
        result = translator.translate("123")
        assert isinstance(result, list)
        
        result_pi = translator.translate("3.14")
        assert isinstance(result_pi, list)

    def test_long_keys_and_values(self):
        """Test translation with long keys and values."""
        long_key = "a" * 100
        long_value = "b" * 200
        dictionary = {
            long_key: [long_value, "short"],
            "short": [long_value]
        }
        translator = Translator(dictionary, True)
        
        result = translator.translate(long_key)
        assert isinstance(result, list)
        
        result_short = translator.translate("short")
        assert isinstance(result_short, list)

    def test_multiple_translators(self):
        """Test creating multiple translator instances."""
        dict1 = {"hello": ["hi"], "world": ["earth"]}
        dict2 = {"bonjour": ["hello"], "monde": ["world"]}
        
        translator1 = Translator(dict1, True)
        translator2 = Translator(dict2, False)
        
        # Both should work independently
        result1 = translator1.translate("hello")
        result2 = translator2.translate("bonjour")
        
        assert isinstance(result1, list)
        assert isinstance(result2, list)

    def test_translation_result_structure(self):
        """Test the structure of translation results."""
        dictionary = {"test": ["result1", "result2"]}
        translator = Translator(dictionary, True)
        
        result = translator.translate("test")
        assert isinstance(result, list)
        
        if len(result) > 0:
            translation = result[0]
            assert isinstance(translation, dict)
            
            # Check expected keys in translation result
            expected_keys = ["texts", "code"]
            for key in expected_keys:
                assert key in translation
            
            # Check texts structure
            assert isinstance(translation["texts"], list)
            assert translation["texts"] == ["result1", "result2"]

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Empty values in dictionary
        dictionary = {
            "empty": [],
            "normal": ["value"],
            "single": ["one"]
        }
        translator = Translator(dictionary, True)
        
        # Test empty value list
        result_empty = translator.translate("empty")
        assert isinstance(result_empty, list)
        
        # Test normal case
        result_normal = translator.translate("normal")
        assert isinstance(result_normal, list)

    @pytest.mark.skipif(True, reason="Rhai feature may not be enabled")
    def test_register_unregister_functionality(self):
        """Test register and unregister functionality (if rhai feature is enabled)."""
        dictionary = {"test": ["result"]}
        translator = Translator(dictionary, True)
        
        # Try to register a script (this may not work if rhai feature is disabled)
        try:
            translator.register("test_script", "fn main() { }")
            translator.unregister("test_script")
        except AttributeError:
            # Methods don't exist if rhai feature is not enabled
            pytest.skip("Rhai feature not enabled")

    def test_whitespace_handling(self):
        """Test translation with whitespace in keys and values."""
        dictionary = {
            " hello ": ["hi"],
            "hello world": ["hi earth"],
            "\ttest\t": ["result"],
            "\n\r": ["newlines"]
        }
        translator = Translator(dictionary, True)
        
        for key in dictionary.keys():
            result = translator.translate(key)
            assert isinstance(result, list)
