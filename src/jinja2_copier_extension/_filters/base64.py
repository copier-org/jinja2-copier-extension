"""Jinja2 filters for Base64 encoding/decoding."""

from __future__ import annotations

from base64 import b64decode
from base64 import b64encode

__all__ = ["do_b64decode", "do_b64encode"]


def do_b64decode(value: str, encoding: str = "utf-8") -> str:
    """Decode a Base64 encoded string.

    Args:
        value: A Base64 encoded string.
        encoding: The encoding with which to decode the Base64 decoded bytes.

    Returns:
        The Base64 decoded string.
    """
    return b64decode(value).decode(encoding)


def do_b64encode(value: str, encoding: str = "utf-8") -> str:
    """Encode a string using Base64.

    Args:
        value: A string.
        encoding: The encoding with which to encode the string.

    Returns:
        The Base64 encoded string.
    """
    return b64encode(value.encode(encoding)).decode()
