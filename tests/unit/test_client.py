"""Tests for Client class."""

import pytest

from mailjunky import Client, ConfigurationError, configure, reset_config


class TestClient:
    """Tests for Client class."""

    def setup_method(self) -> None:
        """Reset configuration before each test."""
        reset_config()

    def teardown_method(self) -> None:
        """Reset configuration after each test."""
        reset_config()

    def test_init_with_api_key(self) -> None:
        """Test client initialization with API key."""
        client = Client(api_key="test-key")

        assert client.emails is not None
        assert client.contacts is not None
        assert client.events is not None

        client.close()

    def test_init_without_api_key(self) -> None:
        """Test client initialization fails without API key."""
        with pytest.raises(ConfigurationError, match="API key is required"):
            Client()

    def test_init_with_global_config(self) -> None:
        """Test client uses global configuration."""
        configure(api_key="global-key")

        client = Client()

        assert client.emails is not None
        client.close()

    def test_context_manager(self) -> None:
        """Test client as context manager."""
        with Client(api_key="test-key") as client:
            assert client.emails is not None

    def test_custom_base_url(self) -> None:
        """Test client with custom base URL."""
        client = Client(api_key="test-key", base_url="https://custom.api.com")

        assert client._connection._config.base_url == "https://custom.api.com"
        client.close()

    def test_custom_timeouts(self) -> None:
        """Test client with custom timeouts."""
        client = Client(api_key="test-key", timeout=60.0, connect_timeout=20.0)

        assert client._connection._config.timeout == 60.0
        assert client._connection._config.connect_timeout == 20.0
        client.close()
