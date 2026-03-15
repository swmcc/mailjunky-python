"""Base resource class for MailJunky API resources."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..connection import Connection


class BaseResource:
    """Base class for API resources.

    Args:
        connection: Connection instance for making API requests
    """

    def __init__(self, connection: "Connection") -> None:
        self._connection = connection
