# MailJunky Python SDK

[![CI](https://github.com/swmcc/mailjunky-python/actions/workflows/ci.yml/badge.svg)](https://github.com/swmcc/mailjunky-python/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Python SDK for [MailJunky](https://mailjunky.ai) - Email API with AI-Powered Workflows.

**[Documentation](https://swmcc.github.io/mailjunky-python)** | **[API Reference](https://mailjunky.ai/api-reference)** | **[Get API Key](https://mailjunky.ai)**

## Installation

```bash
pip install mailjunky
```

Or with pip from GitHub:

```bash
pip install git+https://github.com/swmcc/mailjunky-python.git
```

## Quick Start

```python
from mailjunky import Client

client = Client(api_key="your-api-key")

client.emails.send(
    from_="hello@yourapp.com",
    to="user@example.com",
    subject="Welcome!",
    html="<h1>Welcome aboard</h1>"
)
```

## Features

- **Emails** - Send transactional emails with full control
- **Contacts** - Manage contacts with tags and properties
- **Events** - Track user behaviour for AI-powered workflows
- **Type hints** - Full type annotations for IDE support
- **Async ready** - Built on httpx for future async support

## Usage

### Sending Emails

```python
from mailjunky import Client

client = Client(api_key="your-api-key")

# Simple send
client.emails.send(
    from_="hello@yourapp.com",
    to="user@example.com",
    subject="Welcome!",
    html="<h1>Welcome</h1>",
    text="Welcome"  # Plain text fallback
)

# With all options
client.emails.send(
    from_="hello@yourapp.com",
    to=["user1@example.com", "user2@example.com"],
    subject="Team Update",
    html="<h1>News</h1>",
    cc="manager@example.com",
    bcc="archive@example.com",
    reply_to="support@example.com",
    tags=["newsletter"],
    metadata={"campaign_id": "123"}
)

# Batch send
client.emails.send_batch([
    {"from": "hello@yourapp.com", "to": "a@example.com", "subject": "Hi A"},
    {"from": "hello@yourapp.com", "to": "b@example.com", "subject": "Hi B"},
])
```

### Managing Contacts

```python
# Create a contact
client.contacts.create(
    email="user@example.com",
    first_name="John",
    last_name="Doe",
    tags=["customer", "newsletter"]
)

# Upsert (create or update)
client.contacts.upsert(
    email="user@example.com",
    properties={"plan": "premium"}
)

# List with filters
contacts = client.contacts.list(tag="customer", limit=50)

# Update
client.contacts.update(id="contact_123", tags=["vip"])

# Delete
client.contacts.delete(id="contact_123")
```

### Tracking Events

```python
# Track user behaviour for AI workflows
client.events.track(
    event="purchase_completed",
    user={"email": "user@example.com"},
    properties={
        "order_id": "12345",
        "amount": 99.99,
        "items": ["SKU-001", "SKU-002"]
    }
)
```

### Global Configuration

```python
import mailjunky

# Configure once
mailjunky.configure(api_key="your-api-key")

# Create clients without passing api_key
client = mailjunky.Client()
```

### Context Manager

```python
with Client(api_key="your-api-key") as client:
    client.emails.send(...)
# Connection automatically closed
```

## Error Handling

```python
from mailjunky import (
    Client,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    ServerError,
)

client = Client(api_key="your-api-key")

try:
    client.emails.send(...)
except AuthenticationError:
    print("Invalid API key")
except ValidationError as e:
    print(f"Invalid request: {e.message}")
    print(f"Details: {e.body}")
except RateLimitError:
    print("Slow down! Rate limit exceeded")
except ServerError:
    print("MailJunky is having issues, try again later")
```

## Development

```bash
make install   # Install dependencies
make test      # Run tests
make lint      # Run ruff + mypy
make check     # Run all checks
```

## License

MIT
