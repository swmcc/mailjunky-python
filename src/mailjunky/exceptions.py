"""Custom exceptions for MailJunky SDK."""

from typing import Any, Dict, Optional


class MailJunkyError(Exception):
    """Base exception for all MailJunky errors."""

    pass


class ConfigurationError(MailJunkyError):
    """Raised when there's a configuration problem."""

    pass


class APIError(MailJunkyError):
    """Base exception for API-related errors.

    Attributes:
        message: Error message
        status: HTTP status code
        code: API error code
        body: Full response body
    """

    def __init__(
        self,
        message: str,
        status: Optional[int] = None,
        code: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.status = status
        self.code = code
        self.body = body or {}
        super().__init__(message)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, status={self.status})"


class AuthenticationError(APIError):
    """Raised when authentication fails (401)."""

    pass


class NotFoundError(APIError):
    """Raised when a resource is not found (404)."""

    pass


class ValidationError(APIError):
    """Raised when request validation fails (422)."""

    pass


class RateLimitError(APIError):
    """Raised when rate limit is exceeded (429)."""

    pass


class ServerError(APIError):
    """Raised when the server returns an error (5xx)."""

    pass
