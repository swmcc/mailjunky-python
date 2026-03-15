"""Configuration for MailJunky client."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Configuration:
    """Configuration settings for the MailJunky client.

    Attributes:
        api_key: Your MailJunky API key
        base_url: Base URL for the API (default: https://api.mailjunky.ai)
        timeout: Request timeout in seconds (default: 30)
        connect_timeout: Connection timeout in seconds (default: 10)
    """

    api_key: Optional[str] = None
    base_url: str = "https://api.mailjunky.ai"
    timeout: float = 30.0
    connect_timeout: float = 10.0

    def validate(self) -> None:
        """Validate the configuration.

        Raises:
            ConfigurationError: If required settings are missing
        """
        from .exceptions import ConfigurationError

        if not self.api_key:
            raise ConfigurationError("API key is required")


# Global configuration instance
_config: Configuration = Configuration()


def get_config() -> Configuration:
    """Get the global configuration instance."""
    return _config


def configure(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: Optional[float] = None,
    connect_timeout: Optional[float] = None,
) -> None:
    """Configure the global MailJunky settings.

    Args:
        api_key: Your MailJunky API key
        base_url: Base URL for the API
        timeout: Request timeout in seconds
        connect_timeout: Connection timeout in seconds
    """
    global _config

    if api_key is not None:
        _config.api_key = api_key
    if base_url is not None:
        _config.base_url = base_url
    if timeout is not None:
        _config.timeout = timeout
    if connect_timeout is not None:
        _config.connect_timeout = connect_timeout


def reset_config() -> None:
    """Reset configuration to defaults."""
    global _config
    _config = Configuration()
