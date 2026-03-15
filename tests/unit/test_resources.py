"""Tests for API resources."""

from unittest.mock import MagicMock

import pytest

from mailjunky.resources.contacts import Contacts
from mailjunky.resources.emails import Emails
from mailjunky.resources.events import Events


class TestEmails:
    """Tests for Emails resource."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.connection = MagicMock()
        self.emails = Emails(self.connection)

    def test_send_basic(self) -> None:
        """Test basic email send."""
        self.connection.post.return_value = {"id": "msg_123"}

        result = self.emails.send(
            from_="sender@example.com",
            to="recipient@example.com",
            subject="Test",
            html="<p>Hello</p>",
        )

        self.connection.post.assert_called_once_with(
            "/api/v1/emails/send",
            {
                "from": "sender@example.com",
                "to": ["recipient@example.com"],
                "subject": "Test",
                "html": "<p>Hello</p>",
            },
        )
        assert result == {"id": "msg_123"}

    def test_send_with_all_options(self) -> None:
        """Test email send with all options."""
        self.emails.send(
            from_="sender@example.com",
            to=["a@example.com", "b@example.com"],
            subject="Test",
            html="<p>Hello</p>",
            text="Hello",
            cc="cc@example.com",
            bcc=["bcc1@example.com", "bcc2@example.com"],
            reply_to="reply@example.com",
            headers={"X-Custom": "value"},
            tags=["transactional"],
            metadata={"user_id": "123"},
        )

        call_args = self.connection.post.call_args[0]
        payload = call_args[1]

        assert payload["to"] == ["a@example.com", "b@example.com"]
        assert payload["cc"] == ["cc@example.com"]
        assert payload["bcc"] == ["bcc1@example.com", "bcc2@example.com"]
        assert payload["reply_to"] == ["reply@example.com"]
        assert payload["headers"] == {"X-Custom": "value"}
        assert payload["tags"] == ["transactional"]
        assert payload["metadata"] == {"user_id": "123"}

    def test_send_batch(self) -> None:
        """Test batch email send."""
        emails = [
            {"from": "a@example.com", "to": "b@example.com", "subject": "Test 1"},
            {"from": "a@example.com", "to": "c@example.com", "subject": "Test 2"},
        ]

        self.emails.send_batch(emails)

        self.connection.post.assert_called_once_with(
            "/api/v1/emails/batch", {"emails": emails}
        )


class TestContacts:
    """Tests for Contacts resource."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.connection = MagicMock()
        self.contacts = Contacts(self.connection)

    def test_list_no_params(self) -> None:
        """Test listing contacts without filters."""
        self.contacts.list()

        self.connection.get.assert_called_once_with("/api/v1/contacts", None)

    def test_list_with_filters(self) -> None:
        """Test listing contacts with filters."""
        self.contacts.list(page=1, limit=10, tag="customer")

        self.connection.get.assert_called_once_with(
            "/api/v1/contacts", {"page": 1, "limit": 10, "tag": "customer"}
        )

    def test_get(self) -> None:
        """Test getting a contact."""
        self.contacts.get(id="contact_123")

        self.connection.get.assert_called_once_with("/api/v1/contacts/contact_123")

    def test_create(self) -> None:
        """Test creating a contact."""
        self.contacts.create(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            tags=["customer"],
        )

        self.connection.post.assert_called_once_with(
            "/api/v1/contacts",
            {
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "tags": ["customer"],
            },
        )

    def test_upsert(self) -> None:
        """Test upserting a contact."""
        self.contacts.upsert(email="test@example.com", first_name="John")

        self.connection.post.assert_called_once_with(
            "/api/v1/contacts/upsert",
            {"email": "test@example.com", "first_name": "John"},
        )

    def test_update(self) -> None:
        """Test updating a contact."""
        self.contacts.update(id="contact_123", first_name="Jane", status="active")

        self.connection.patch.assert_called_once_with(
            "/api/v1/contacts/contact_123",
            {"first_name": "Jane", "status": "active"},
        )

    def test_delete(self) -> None:
        """Test deleting a contact."""
        self.contacts.delete(id="contact_123")

        self.connection.delete.assert_called_once_with("/api/v1/contacts/contact_123")

    def test_batch(self) -> None:
        """Test batch contact operations."""
        contacts = [
            {"email": "a@example.com", "first_name": "A"},
            {"email": "b@example.com", "first_name": "B"},
        ]

        self.contacts.batch(contacts)

        self.connection.post.assert_called_once_with(
            "/api/v1/contacts/batch", {"contacts": contacts}
        )


class TestEvents:
    """Tests for Events resource."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.connection = MagicMock()
        self.events = Events(self.connection)

    def test_track_basic(self) -> None:
        """Test basic event tracking."""
        self.events.track(event="page_viewed")

        self.connection.post.assert_called_once_with(
            "/api/v1/events/track", {"event": "page_viewed"}
        )

    def test_track_with_all_options(self) -> None:
        """Test event tracking with all options."""
        self.events.track(
            event="purchase_completed",
            user={"email": "user@example.com"},
            properties={"amount": 99.99},
            session_id="sess_123",
            timestamp="2026-03-15T10:00:00Z",
        )

        self.connection.post.assert_called_once_with(
            "/api/v1/events/track",
            {
                "event": "purchase_completed",
                "user": {"email": "user@example.com"},
                "properties": {"amount": 99.99},
                "session_id": "sess_123",
                "timestamp": "2026-03-15T10:00:00Z",
            },
        )
