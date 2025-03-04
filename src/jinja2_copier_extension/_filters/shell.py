"""Jinja2 filters related to shell interaction."""

from __future__ import annotations

from shlex import quote

__all__ = ["do_quote"]


def do_quote(value: str) -> str:
    """Shell-escape a string.

    Args:
        value: A string.

    Returns:
        The shell-escape string.
    """
    return quote(value)
