"""Email resource for sending emails via MailJunky."""

from typing import Any, Optional, Union

from .base import BaseResource


class Emails(BaseResource):
    """Email operations.

    Example:
        >>> client.emails.send(
        ...     from_="hello@yourapp.com",
        ...     to="user@example.com",
        ...     subject="Welcome!",
        ...     html="<h1>Welcome aboard</h1>"
        ... )
    """

    def send(
        self,
        *,
        from_: str,
        to: Union[str, list[str]],
        subject: str,
        html: Optional[str] = None,
        text: Optional[str] = None,
        cc: Optional[Union[str, list[str]]] = None,
        bcc: Optional[Union[str, list[str]]] = None,
        reply_to: Optional[Union[str, list[str]]] = None,
        headers: Optional[dict[str, str]] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Send a single email.

        Args:
            from_: Sender email address
            to: Recipient email address(es)
            subject: Email subject line
            html: HTML body content
            text: Plain text body content
            cc: CC recipients
            bcc: BCC recipients
            reply_to: Reply-to address(es)
            headers: Custom email headers
            tags: Tags for categorization
            metadata: Custom metadata

        Returns:
            API response with message ID
        """
        payload: dict[str, Any] = {
            "from": from_,
            "to": to if isinstance(to, list) else [to],
            "subject": subject,
        }

        if html is not None:
            payload["html"] = html
        if text is not None:
            payload["text"] = text
        if cc is not None:
            payload["cc"] = cc if isinstance(cc, list) else [cc]
        if bcc is not None:
            payload["bcc"] = bcc if isinstance(bcc, list) else [bcc]
        if reply_to is not None:
            payload["reply_to"] = reply_to if isinstance(reply_to, list) else [reply_to]
        if headers is not None:
            payload["headers"] = headers
        if tags is not None:
            payload["tags"] = tags
        if metadata is not None:
            payload["metadata"] = metadata

        return self._connection.post("/api/v1/emails/send", payload)

    def send_batch(self, emails: list[dict[str, Any]]) -> dict[str, Any]:
        """Send multiple emails in a batch.

        Args:
            emails: List of email objects, each with from, to, subject, etc.

        Returns:
            API response with batch results
        """
        return self._connection.post("/api/v1/emails/batch", {"emails": emails})
