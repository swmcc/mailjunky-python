"""Main client for MailJunky SDK."""

from typing import Optional

from .configuration import Configuration, get_config
from .connection import Connection
from .resources.contacts import Contacts
from .resources.emails import Emails
from .resources.events import Events


class Client:
    """MailJunky API client.

    The main entry point for interacting with the MailJunky API.

    Example:
        >>> from mailjunky import Client
        >>> client = Client(api_key="your-api-key")
        >>> client.emails.send(
        ...     from_="hello@yourapp.com",
        ...     to="user@example.com",
        ...     subject="Welcome!",
        ...     html="<h1>Welcome aboard</h1>"
        ... )

    Args:
        api_key: Your MailJunky API key
        base_url: Override the default API base URL
        timeout: Request timeout in seconds
        connect_timeout: Connection timeout in seconds
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
    ) -> None:
        # Build configuration from args + global config
        global_config = get_config()

        config = Configuration(
            api_key=api_key or global_config.api_key,
            base_url=base_url or global_config.base_url,
            timeout=timeout or global_config.timeout,
            connect_timeout=connect_timeout or global_config.connect_timeout,
        )

        self._connection = Connection(config)

        # Initialize resources
        self.emails = Emails(self._connection)
        self.contacts = Contacts(self._connection)
        self.events = Events(self._connection)

    def close(self) -> None:
        """Close the client and release resources."""
        self._connection.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
