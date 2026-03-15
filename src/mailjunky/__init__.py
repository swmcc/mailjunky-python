"""MailJunky Python SDK - Email API with AI-Powered Workflows.

Example:
    >>> from mailjunky import Client
    >>> client = Client(api_key="your-api-key")
    >>> client.emails.send(
    ...     from_="hello@yourapp.com",
    ...     to="user@example.com",
    ...     subject="Welcome!",
    ...     html="<h1>Welcome aboard</h1>"
    ... )

Or configure globally:
    >>> import mailjunky
    >>> mailjunky.configure(api_key="your-api-key")
    >>> client = mailjunky.Client()
"""

from .client import Client
from .configuration import Configuration, configure, get_config, reset_config
from .exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    MailJunkyError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)

__version__ = "0.1.0"

__all__ = [
    # Client
    "Client",
    # Configuration
    "Configuration",
    "configure",
    "get_config",
    "reset_config",
    # Exceptions
    "MailJunkyError",
    "ConfigurationError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
]
