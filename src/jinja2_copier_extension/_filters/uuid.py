"""Jinja2 filters for UUIDs."""

from __future__ import annotations

from uuid import NAMESPACE_DNS
from uuid import uuid5

__all__ = ["do_to_uuid"]

_UUID_NAMESPACE = uuid5(NAMESPACE_DNS, "https://github.com/copier-org/copier")


def do_to_uuid(name: str) -> str:
    """Generate a UUID v5 string from a name.

    The UUID namespace is the DNS namespace `https://github.com/copier-org/copier`.

    Args:
        name: A name.

    Returns:
        The UUID v5 string.
    """
    return str(uuid5(_UUID_NAMESPACE, name))
