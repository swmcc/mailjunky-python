"""Tests for configuration module."""

import pytest

from mailjunky import Configuration, ConfigurationError, configure, get_config, reset_config


class TestConfiguration:
    """Tests for Configuration class."""

    def test_defaults(self) -> None:
        """Test default configuration values."""
        config = Configuration()

        assert config.api_key is None
        assert config.base_url == "https://api.mailjunky.ai"
        assert config.timeout == 30.0
        assert config.connect_timeout == 10.0

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = Configuration(
            api_key="my-key",
            base_url="https://custom.api.com",
            timeout=60.0,
            connect_timeout=20.0,
        )

        assert config.api_key == "my-key"
        assert config.base_url == "https://custom.api.com"
        assert config.timeout == 60.0
        assert config.connect_timeout == 20.0

    def test_validate_missing_api_key(self) -> None:
        """Test validation fails without API key."""
        config = Configuration()

        with pytest.raises(ConfigurationError, match="API key is required"):
            config.validate()

    def test_validate_empty_api_key(self) -> None:
        """Test validation fails with empty API key."""
        config = Configuration(api_key="")

        with pytest.raises(ConfigurationError, match="API key is required"):
            config.validate()

    def test_validate_with_api_key(self) -> None:
        """Test validation passes with API key."""
        config = Configuration(api_key="valid-key")

        config.validate()  # Should not raise


class TestGlobalConfiguration:
    """Tests for global configuration functions."""

    def setup_method(self) -> None:
        """Reset configuration before each test."""
        reset_config()

    def teardown_method(self) -> None:
        """Reset configuration after each test."""
        reset_config()

    def test_configure(self) -> None:
        """Test global configure function."""
        configure(api_key="global-key", timeout=45.0)

        config = get_config()
        assert config.api_key == "global-key"
        assert config.timeout == 45.0

    def test_reset_config(self) -> None:
        """Test configuration reset."""
        configure(api_key="some-key")
        reset_config()

        config = get_config()
        assert config.api_key is None
