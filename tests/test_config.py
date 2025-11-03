"""Tests for TOML to JSON conversion functionality."""

import pytest
from afrim_py import Config, is_rhai_feature_enabled
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = (BASE_DIR / "data").as_posix()


class TestConfig:
    """Test cases for Config class."""

    def test_simple(self):
        config = Config(DATA_DIR + "/config_sample.toml")
        assert isinstance(config.extract_data(), dict)

        # data and core not provided
        config = Config(DATA_DIR + "/blank_sample.toml")
        assert config.extract_data() == {}

        # invalid config file
        with pytest.raises(ValueError, match="Failed to load config file"):
            Config(DATA_DIR + "/invalid_file.toml")

        # not found config file
        with pytest.raises(ValueError, match="Failed to load config file"):
            Config(DATA_DIR + "/not_found.toml")

        # invalid data in config file
        with pytest.raises(ValueError, match="Failed to load config file"):
            Config(DATA_DIR + "/invalid_data.toml")

    @pytest.mark.skipif(
        not is_rhai_feature_enabled(), reason="Rhai feature not be enabled"
    )
    def test_config_file_with_translators(self):
        # invalid translator
        with pytest.raises(ValueError, match="Failed to load config file"):
            Config(DATA_DIR + "/invalid_translator.toml")

    def test_config_file_with_translation(self):
        config = Config(DATA_DIR + "/config_sample.toml")
        assert isinstance(config.extract_translation(), dict)

        # no translation
        config = Config(DATA_DIR + "/blank_sample.toml")
        assert config.extract_translation() == {}
