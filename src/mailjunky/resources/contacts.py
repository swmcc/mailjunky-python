"""Contact resource for managing contacts in MailJunky."""

from typing import Any, Dict, List, Optional

from .base import BaseResource


class Contacts(BaseResource):
    """Contact management operations.

    Example:
        >>> client.contacts.create(
        ...     email="user@example.com",
        ...     first_name="John",
        ...     tags=["customer", "newsletter"]
        ... )
    """

    def list(
        self,
        *,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        email: Optional[str] = None,
        tag: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List contacts with optional filtering.

        Args:
            page: Page number for pagination
            limit: Number of results per page
            email: Filter by email address
            tag: Filter by tag
            status: Filter by status (active, unsubscribed, etc.)

        Returns:
            Paginated list of contacts
        """
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if email is not None:
            params["email"] = email
        if tag is not None:
            params["tag"] = tag
        if status is not None:
            params["status"] = status

        return self._connection.get("/api/v1/contacts", params or None)

    def get(self, id: str) -> Dict[str, Any]:
        """Get a contact by ID.

        Args:
            id: Contact ID

        Returns:
            Contact details
        """
        return self._connection.get(f"/api/v1/contacts/{id}")

    def create(
        self,
        *,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a new contact.

        Args:
            email: Contact email address
            first_name: First name
            last_name: Last name
            phone: Phone number
            properties: Custom properties
            tags: Tags for segmentation

        Returns:
            Created contact
        """
        payload: Dict[str, Any] = {"email": email}

        if first_name is not None:
            payload["first_name"] = first_name
        if last_name is not None:
            payload["last_name"] = last_name
        if phone is not None:
            payload["phone"] = phone
        if properties is not None:
            payload["properties"] = properties
        if tags is not None:
            payload["tags"] = tags

        return self._connection.post("/api/v1/contacts", payload)

    def upsert(
        self,
        *,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create or update a contact by email.

        Args:
            email: Contact email address
            first_name: First name
            last_name: Last name
            phone: Phone number
            properties: Custom properties
            tags: Tags for segmentation

        Returns:
            Created or updated contact
        """
        payload: Dict[str, Any] = {"email": email}

        if first_name is not None:
            payload["first_name"] = first_name
        if last_name is not None:
            payload["last_name"] = last_name
        if phone is not None:
            payload["phone"] = phone
        if properties is not None:
            payload["properties"] = properties
        if tags is not None:
            payload["tags"] = tags

        return self._connection.post("/api/v1/contacts/upsert", payload)

    def update(
        self,
        id: str,
        *,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an existing contact.

        Args:
            id: Contact ID
            first_name: First name
            last_name: Last name
            phone: Phone number
            properties: Custom properties
            tags: Tags for segmentation
            status: Contact status

        Returns:
            Updated contact
        """
        payload: Dict[str, Any] = {}

        if first_name is not None:
            payload["first_name"] = first_name
        if last_name is not None:
            payload["last_name"] = last_name
        if phone is not None:
            payload["phone"] = phone
        if properties is not None:
            payload["properties"] = properties
        if tags is not None:
            payload["tags"] = tags
        if status is not None:
            payload["status"] = status

        return self._connection.patch(f"/api/v1/contacts/{id}", payload)

    def delete(self, id: str) -> Dict[str, Any]:
        """Delete a contact.

        Args:
            id: Contact ID

        Returns:
            Deletion confirmation
        """
        return self._connection.delete(f"/api/v1/contacts/{id}")

    def batch(self, contacts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create or update multiple contacts.

        Args:
            contacts: List of contact objects

        Returns:
            Batch operation results
        """
        return self._connection.post("/api/v1/contacts/batch", {"contacts": contacts})
