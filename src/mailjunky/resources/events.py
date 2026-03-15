"""Events resource for tracking user behaviour in MailJunky."""

from typing import Any, Optional

from .base import BaseResource


class Events(BaseResource):
    """Event tracking operations.

    Track user behaviour for AI-powered email workflows.

    Example:
        >>> client.events.track(
        ...     event="purchase_completed",
        ...     user={"email": "user@example.com"},
        ...     properties={"order_id": "12345", "amount": 99.99}
        ... )
    """

    def track(
        self,
        *,
        event: str,
        user: Optional[dict[str, Any]] = None,
        properties: Optional[dict[str, Any]] = None,
        session_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> dict[str, Any]:
        """Track a user event.

        Args:
            event: Event name (e.g., "purchase_completed", "page_viewed")
            user: User identifier (email, id, or both)
            properties: Event-specific properties
            session_id: Session identifier for grouping events
            timestamp: ISO 8601 timestamp (defaults to now)

        Returns:
            API response confirming event tracked
        """
        payload: dict[str, Any] = {"event": event}

        if user is not None:
            payload["user"] = user
        if properties is not None:
            payload["properties"] = properties
        if session_id is not None:
            payload["session_id"] = session_id
        if timestamp is not None:
            payload["timestamp"] = timestamp

        return self._connection.post("/api/v1/events/track", payload)
