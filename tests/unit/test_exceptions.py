"""Tests for exceptions module."""

from mailjunky import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    MailJunkyError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class TestExceptions:
    """Tests for exception classes."""

    def test_mailjunky_error(self) -> None:
        """Test base MailJunkyError."""
        error = MailJunkyError("Something went wrong")

        assert str(error) == "Something went wrong"
        assert isinstance(error, Exception)

    def test_configuration_error(self) -> None:
        """Test ConfigurationError."""
        error = ConfigurationError("Invalid config")

        assert str(error) == "Invalid config"
        assert isinstance(error, MailJunkyError)

    def test_api_error_basic(self) -> None:
        """Test APIError with basic message."""
        error = APIError("Request failed")

        assert error.message == "Request failed"
        assert error.status is None
        assert error.code is None
        assert error.body == {}

    def test_api_error_full(self) -> None:
        """Test APIError with all attributes."""
        error = APIError(
            "Validation failed",
            status=422,
            code="INVALID_EMAIL",
            body={"errors": ["Invalid email format"]},
        )

        assert error.message == "Validation failed"
        assert error.status == 422
        assert error.code == "INVALID_EMAIL"
        assert error.body == {"errors": ["Invalid email format"]}

    def test_api_error_repr(self) -> None:
        """Test APIError string representation."""
        error = APIError("Test error", status=400)

        assert "APIError" in repr(error)
        assert "Test error" in repr(error)
        assert "400" in repr(error)

    def test_authentication_error(self) -> None:
        """Test AuthenticationError."""
        error = AuthenticationError("Invalid API key", status=401)

        assert isinstance(error, APIError)
        assert error.status == 401

    def test_not_found_error(self) -> None:
        """Test NotFoundError."""
        error = NotFoundError("Contact not found", status=404)

        assert isinstance(error, APIError)
        assert error.status == 404

    def test_validation_error(self) -> None:
        """Test ValidationError."""
        error = ValidationError("Invalid data", status=422)

        assert isinstance(error, APIError)
        assert error.status == 422

    def test_rate_limit_error(self) -> None:
        """Test RateLimitError."""
        error = RateLimitError("Too many requests", status=429)

        assert isinstance(error, APIError)
        assert error.status == 429

    def test_server_error(self) -> None:
        """Test ServerError."""
        error = ServerError("Internal error", status=500)

        assert isinstance(error, APIError)
        assert error.status == 500
