"""Jinja2 filters for date/time functions."""

from __future__ import annotations

from datetime import datetime
from time import localtime
from time import strftime

__all__ = ["do_strftime", "do_to_datetime"]


def do_strftime(
    format: str,  # noqa: A002
    second: float | None = None,
) -> str:
    """Convert a Unix timestamp to a date/time string according to a date/time format.

    Args:
        format: A string that describes the expected date/time format.
        second: Unix timestamp in local time. If `None`, the current time is used.

    Returns:
        The formatted date/time string.
    """
    return strftime(format, localtime(second))


def do_to_datetime(
    string: str,
    format: str = "%Y-%m-%d %H:%M:%S",  # noqa: A002
) -> datetime:
    """Convert a string containing date/time information to a `datetime` object.

    Args:
        string: A string containing date/time information.
        format: A string that describes the expected date/time format of `string`.

    Returns:
        The corresponding `datetime` object.
    """
    return datetime.strptime(string, format)  # noqa: DTZ007
