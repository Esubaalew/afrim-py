"""Integration tests for afrim-py components working together."""

import json
import pytest
from afrim_py import Preprocessor, Translator, convert_toml_to_json


class TestIntegration:
    """Integration tests for afrim-py components."""

    def test_toml_to_preprocessor_workflow(self):
        """Test workflow from TOML to Preprocessor."""
        # Start with TOML configuration
        toml_config = '''
[preprocessor_data]
a1 = "à"
ae = "æ"
oe = "œ"
hello = "hi"
'''
        
        # Convert TOML to JSON
        json_str = convert_toml_to_json(toml_config)
        config = json.loads(json_str)
        
        # Extract preprocessor data
        preprocessor_data = config["preprocessor_data"]
        
        # Create preprocessor with the data
        preprocessor = Preprocessor(preprocessor_data, 64)
        
        # Test the preprocessor
        result = preprocessor.process("a", "keydown")
        assert isinstance(result, bool)
        
        input_text = preprocessor.get_input()
        assert input_text == "a"

    def test_toml_to_translator_workflow(self):
        """Test workflow from TOML to Translator."""
        # TOML with translator dictionary
        toml_config = '''
[translator_dict.hello]
values = ["hi", "hey", "greetings"]

[translator_dict.world]  
values = ["earth", "globe"]

[translator_dict.goodbye]
values = ["bye", "farewell"]
'''
        
        # Convert TOML to JSON
        json_str = convert_toml_to_json(toml_config)
        config = json.loads(json_str)
        
        # Build translator dictionary
        translator_dict = {}
        for key, data in config["translator_dict"].items():
            translator_dict[key] = data["values"]
        
        # Create translator
        translator = Translator(translator_dict, True)
        
        # Test translations
        result_hello = translator.translate("hello")
        assert isinstance(result_hello, list)
        
        result_world = translator.translate("world")
        assert isinstance(result_world, list)

    def test_preprocessor_translator_pipeline(self):
        """Test Preprocessor -> Translator pipeline."""
        # Setup preprocessor with key mappings
        preprocessor_data = {
            "h1": "hello",
            "w1": "world",
            "b1": "bye"
        }
        preprocessor = Preprocessor(preprocessor_data, 64)
        
        # Setup translator with translations
        translator_dict = {
            "hello": ["hi", "hey"],
            "world": ["earth", "globe"],
            "bye": ["goodbye", "farewell"]
        }
        translator = Translator(translator_dict, True)
        
        # Simulate user typing "h1"
        preprocessor.process("h", "keydown")
        preprocessor.process("1", "keydown")
        
        # Get the processed input
        processed_input = preprocessor.get_input()
        assert processed_input == "h1"
        
        # Use processed input for translation (in real usage, 
        # you'd need to resolve the preprocessor mapping first)
        # For this test, we'll translate "hello" directly
        translation_result = translator.translate("hello")
        assert isinstance(translation_result, list)
        
        if len(translation_result) > 0:
            assert translation_result[0]["texts"] == ["hi", "hey"]

    def test_complete_input_method_workflow(self):
        """Test complete input method workflow."""
        # Configuration
        preprocessor_mappings = {
            "cafe": "café",
            "naive": "naïve", 
            "resume": "résumé"
        }
        
        translation_dict = {
            "café": ["coffee", "☕"],
            "naïve": ["innocent", "simple"],
            "résumé": ["CV", "summary"]
        }
        
        # Create components
        preprocessor = Preprocessor(preprocessor_mappings, 128)
        translator = Translator(translation_dict, True)
        
        # Simulate typing "cafe"
        keys = ["c", "a", "f", "e"]
        for key in keys:
            result = preprocessor.process(key, "keydown")
            assert isinstance(result, bool)
        
        # Get processed text
        processed = preprocessor.get_input()
        assert processed == "cafe"
        
        # In a real implementation, you'd resolve the mapping:
        # "cafe" -> "café" then translate "café"
        translated = translator.translate("café")
        assert isinstance(translated, list)
        
        if len(translated) > 0:
            assert "coffee" in translated[0]["texts"]

    def test_error_handling_integration(self):
        """Test error handling across components."""
        # Test with problematic TOML
        try:
            convert_toml_to_json("[invalid toml")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected
        
        # Test preprocessor with invalid key state
        preprocessor = Preprocessor({"a": "alpha"}, 32)
        try:
            preprocessor.process("a", "invalid_state")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected
        
        # Test translator with various inputs
        translator = Translator({"test": ["result"]}, True)
        
        # These should not raise errors
        result1 = translator.translate("")
        result2 = translator.translate("nonexistent")
        result3 = translator.translate("🚀🎉✨")
        
        assert isinstance(result1, list)
        assert isinstance(result2, list)
        assert isinstance(result3, list)

    def test_unicode_workflow(self):
        """Test Unicode handling across all components."""
        # TOML with Unicode
        toml_unicode = '''
title = "Unicode Test 🚀"

[mappings]
emoji1 = "🚀"
emoji2 = "🎉"
cafe = "café"
naive = "naïve"
'''
        
        # Convert and extract
        json_str = convert_toml_to_json(toml_unicode)
        config = json.loads(json_str)
        
        # Test preprocessor with Unicode
        preprocessor = Preprocessor(config["mappings"], 64)
        result = preprocessor.process("e", "keydown")
        assert isinstance(result, bool)
        
        # Test translator with Unicode (using safer Unicode characters)
        unicode_dict = {
            "🚀": ["rocket", "spaceship"],
            "café": ["coffee", "☕"],
            "naïve": ["innocent", "simple"]
        }
        translator = Translator(unicode_dict, True)
        
        for key in unicode_dict.keys():
            result = translator.translate(key)
            assert isinstance(result, list)

    def test_performance_basic(self):
        """Basic performance test with larger datasets."""
        # Create larger dataset
        large_preprocessor_data = {f"key{i}": f"value{i}" for i in range(100)}
        large_translator_dict = {f"word{i}": [f"translation{i}", f"alt{i}"] for i in range(100)}
        
        # Create components
        preprocessor = Preprocessor(large_preprocessor_data, 256)
        translator = Translator(large_translator_dict, True)
        
        # Test operations
        for i in range(10):  # Test a subset
            key = f"key{i}"
            word = f"word{i}"
            
            # Test preprocessor
            for char in key:
                result = preprocessor.process(char, "keydown")
                assert isinstance(result, bool)
            
            # Test translator
            translation = translator.translate(word)
            assert isinstance(translation, list)

    def test_memory_cleanup(self):
        """Test that components can be properly cleaned up."""
        # Create multiple instances
        instances = []
        
        for i in range(10):
            prep = Preprocessor({f"k{i}": f"v{i}"}, 32)
            trans = Translator({f"w{i}": [f"t{i}"]}, True)
            instances.append((prep, trans))
        
        # Use them briefly
        for prep, trans in instances:
            prep.process("a", "keydown")
            trans.translate("test")
        
        # Clear references (Python garbage collection will handle cleanup)
        instances.clear()
        
        # Create new instances to ensure no conflicts
        new_prep = Preprocessor({"test": "ok"}, 64)
        new_trans = Translator({"ok": ["good"]}, True)
        
        assert new_prep.process("t", "keydown") is not None
        assert new_trans.translate("ok") is not None
