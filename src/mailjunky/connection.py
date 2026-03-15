"""HTTP connection handling for MailJunky API."""

from typing import Any, Optional

import httpx

from .configuration import Configuration
from .exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class Connection:
    """Handles HTTP communication with the MailJunky API.

    Args:
        config: Configuration instance with API settings
    """

    def __init__(self, config: Configuration) -> None:
        config.validate()
        self._config = config
        self._client: Optional[httpx.Client] = None

    @property
    def client(self) -> httpx.Client:
        """Get or create the HTTP client."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._config.base_url,
                headers={
                    "Authorization": f"Bearer {self._config.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "mailjunky-python/0.1.0",
                },
                timeout=httpx.Timeout(
                    timeout=self._config.timeout,
                    connect=self._config.connect_timeout,
                ),
            )
        return self._client

    def get(self, path: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Make a GET request.

        Args:
            path: API endpoint path
            params: Query parameters

        Returns:
            Response data as dictionary
        """
        response = self.client.get(path, params=params)
        return self._handle_response(response)

    def post(self, path: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Make a POST request.

        Args:
            path: API endpoint path
            data: Request body

        Returns:
            Response data as dictionary
        """
        response = self.client.post(path, json=data)
        return self._handle_response(response)

    def patch(self, path: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Make a PATCH request.

        Args:
            path: API endpoint path
            data: Request body

        Returns:
            Response data as dictionary
        """
        response = self.client.patch(path, json=data)
        return self._handle_response(response)

    def delete(self, path: str) -> dict[str, Any]:
        """Make a DELETE request.

        Args:
            path: API endpoint path

        Returns:
            Response data as dictionary
        """
        response = self.client.delete(path)
        return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle API response and raise appropriate errors.

        Args:
            response: httpx Response object

        Returns:
            Parsed response body

        Raises:
            APIError: On API errors
        """
        body = self._parse_body(response)

        if 200 <= response.status_code < 300:
            return body

        message = body.get("message", "Request failed")
        code = body.get("code")
        status = response.status_code

        if status == 401:
            raise AuthenticationError(
                message or "Authentication failed", status=status, code=code, body=body
            )
        elif status == 404:
            raise NotFoundError(message or "Not found", status=status, code=code, body=body)
        elif status == 422:
            raise ValidationError(
                message or "Validation failed", status=status, code=code, body=body
            )
        elif status == 429:
            raise RateLimitError(
                message or "Rate limit exceeded", status=status, code=code, body=body
            )
        elif status >= 500:
            raise ServerError(message or "Server error", status=status, code=code, body=body)
        else:
            raise APIError(message, status=status, code=code, body=body)

    def _parse_body(self, response: httpx.Response) -> dict[str, Any]:
        """Parse response body as JSON.

        Args:
            response: httpx Response object

        Returns:
            Parsed JSON or empty dict
        """
        if not response.content:
            return {}
        try:
            result: dict[str, Any] = response.json()
            return result
        except Exception:
            return {}

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "Connection":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
