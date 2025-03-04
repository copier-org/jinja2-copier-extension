"""Jinja2 filters related to types."""

from __future__ import annotations

from contextlib import suppress
from typing import Any

__all__ = ["do_bool", "do_type_debug"]


def do_bool(value: Any) -> bool:
    """Parse anything to boolean.

    Tries to be as smart as possible:

    1.  Cast to number. Then: `0 → False`; anything else `→ True`.
    2.  Find [YAML booleans](https://yaml.org/type/bool.html),
        [YAML nulls](https://yaml.org/type/null.html) or `none` in it
        and use it appropriately.
    3.  Cast to boolean using standard Python `bool(value)`.

    Args:
        value: Anything to be casted to a bool.

    Returns:
        The value parsed to boolean.
    """
    # Assume it's a number
    with suppress(TypeError, ValueError):
        return bool(float(value))
    # Assume it's a string
    with suppress(AttributeError):
        lower = value.lower()
        if lower in {"y", "yes", "t", "true", "on"}:
            return True
        if lower in {"n", "no", "f", "false", "off", "~", "null", "none"}:
            return False
    # Assume nothing
    return bool(value)


def do_type_debug(obj: object) -> str:
    """Get the type name of an object.

    Args:
        obj: An object.

    Returns:
        The type name of the object.
    """
    return obj.__class__.__name__
