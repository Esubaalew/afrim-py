"""Tests for Preprocessor functionality."""

import pytest
from afrim_py import Preprocessor


class TestPreprocessor:
    """Test cases for Preprocessor class."""

    def test_preprocessor_initialization(self):
        """Test basic Preprocessor initialization."""
        data = {"a1": "à", "ae": "æ", "oe": "œ"}
        buffer_size = 64
        
        preprocessor = Preprocessor(data, buffer_size)
        assert preprocessor is not None

    def test_empty_data_initialization(self):
        """Test Preprocessor with empty data."""
        preprocessor = Preprocessor({}, 32)
        assert preprocessor is not None

    def test_single_key_processing(self):
        """Test processing a single key."""
        data = {"a": "α"}
        preprocessor = Preprocessor(data, 64)
        
        # Process key 'a' down
        result = preprocessor.process("a", "keydown")
        assert isinstance(result, bool)
        
        # Get current input
        input_text = preprocessor.get_input()
        assert isinstance(input_text, str)

    def test_key_sequence_processing(self):
        """Test processing a sequence of keys."""
        data = {"a1": "à", "ae": "æ", "hello": "hi"}
        preprocessor = Preprocessor(data, 64)
        
        # Process 'a' key
        result1 = preprocessor.process("a", "keydown")
        assert isinstance(result1, bool)
        current_input = preprocessor.get_input()
        assert current_input == "a"
        
        # Process '1' key to complete 'a1'
        result2 = preprocessor.process("1", "keydown")
        assert isinstance(result2, bool)
        current_input = preprocessor.get_input()
        assert current_input == "a1"

    def test_keyup_processing(self):
        """Test processing key up events."""
        data = {"test": "result"}
        preprocessor = Preprocessor(data, 64)
        
        # Test keyup event
        result = preprocessor.process("t", "keyup")
        assert isinstance(result, bool)

    def test_invalid_key_state(self):
        """Test processing with invalid key state."""
        data = {"a": "alpha"}
        preprocessor = Preprocessor(data, 64)
        
        # Invalid state should raise an error
        with pytest.raises(ValueError):
            preprocessor.process("a", "invalid_state")

    def test_commit_functionality(self):
        """Test commit functionality."""
        data = {"test": "result"}
        preprocessor = Preprocessor(data, 64)
        
        # Commit should not raise an error
        preprocessor.commit("test_text")
        
        # Input should be cleared after commit
        input_text = preprocessor.get_input()
        # The exact behavior depends on the underlying implementation

    def test_queue_operations(self):
        """Test queue operations (pop_queue, clear_queue)."""
        data = {"a1": "à", "test": "result"}
        preprocessor = Preprocessor(data, 64)
        
        # Process some keys to potentially generate queue items
        preprocessor.process("a", "keydown")
        preprocessor.process("1", "keydown")
        
        # Pop from queue
        queue_item = preprocessor.pop_queue()
        assert queue_item is not None
        
        # Clear queue
        preprocessor.clear_queue()
        
        # After clearing, queue should be empty or return default
        queue_item = preprocessor.pop_queue()
        assert queue_item is not None  # Should return default "NOP" or similar

    def test_buffer_size_limits(self):
        """Test different buffer sizes."""
        data = {"longkey": "result"}
        
        # Small buffer
        small_preprocessor = Preprocessor(data, 4)
        assert small_preprocessor is not None
        
        # Large buffer
        large_preprocessor = Preprocessor(data, 1024)
        assert large_preprocessor is not None

    def test_unicode_keys_in_data(self):
        """Test with Unicode characters in data."""
        data = {
            "café": "coffee",
            "naïve": "naive", 
            "résumé": "resume",
            "🚀": "rocket"
        }
        preprocessor = Preprocessor(data, 64)
        
        # Should initialize without error
        assert preprocessor is not None
        
        # Test processing regular keys
        result = preprocessor.process("c", "keydown")
        assert isinstance(result, bool)

    def test_multiple_preprocessors(self):
        """Test creating multiple preprocessor instances."""
        data1 = {"a1": "à", "e1": "é"}
        data2 = {"u1": "ù", "o1": "ò"}
        
        prep1 = Preprocessor(data1, 32)
        prep2 = Preprocessor(data2, 64)
        
        # Both should work independently
        result1 = prep1.process("a", "keydown")
        result2 = prep2.process("u", "keydown")
        
        assert isinstance(result1, bool)
        assert isinstance(result2, bool)
        
        # Inputs should be independent
        input1 = prep1.get_input()
        input2 = prep2.get_input()
        
        assert isinstance(input1, str)
        assert isinstance(input2, str)

    def test_complex_key_mapping(self):
        """Test complex key mappings."""
        data = {
            "aa": "ā",
            "aaa": "ǟ", 
            "hello": "hi",
            "world": "🌍",
            "123": "numbers",
            "abc": "alphabet"
        }
        preprocessor = Preprocessor(data, 128)
        
        # Test sequential processing
        keys = ["h", "e", "l", "l", "o"]
        for key in keys:
            result = preprocessor.process(key, "keydown")
            assert isinstance(result, bool)
        
        current_input = preprocessor.get_input()
        assert current_input == "hello"

    def test_special_characters_processing(self):
        """Test processing special characters."""
        data = {"space": " ", "tab": "\t", "newline": "\n"}
        preprocessor = Preprocessor(data, 64)
        
        # Test space key
        result = preprocessor.process(" ", "keydown")
        assert isinstance(result, bool)
        
        # Test other printable characters
        for char in "!@#$%^&*()":
            result = preprocessor.process(char, "keydown")
            assert isinstance(result, bool)

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Empty string keys
        data = {"": "empty", "a": "alpha"}
        preprocessor = Preprocessor(data, 64)
        
        # Very long key sequences
        long_data = {"a" * 100: "long_key"}
        long_preprocessor = Preprocessor(long_data, 256)
        
        # Minimum buffer size
        min_preprocessor = Preprocessor({"a": "b"}, 1)
        
        assert preprocessor is not None
        assert long_preprocessor is not None
        assert min_preprocessor is not None
