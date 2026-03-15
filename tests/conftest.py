"""Pytest fixtures for MailJunky tests."""

import pytest


@pytest.fixture
def api_key() -> str:
    """Test API key."""
    return "test_api_key_12345"


@pytest.fixture
def base_url() -> str:
    """Test base URL."""
    return "https://api.mailjunky.ai"
