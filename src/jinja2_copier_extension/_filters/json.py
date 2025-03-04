"""Jinja2 filters for JSON (de)serialization."""

from __future__ import annotations

import json
from typing import Any

__all__ = ["do_from_json", "do_to_json", "do_to_nice_json"]


def do_from_json(data: str, /, **kwargs: Any) -> Any:
    """Deserialize JSON data.

    Args:
        data: JSON data to deserialize.
        **kwargs: Additional keyword arguments to pass to `json.loads`.

    Returns:
        Deserialized JSON data.
    """
    return json.loads(data, **kwargs)


def do_to_json(obj: Any, /, **kwargs: Any) -> str:
    """Serialize data as JSON.

    Args:
        obj: Data to serialize.
        **kwargs: Additional keyword arguments to pass to `json.dumps`.

    Returns:
        Serialized JSON data.
    """
    return json.dumps(obj, **kwargs)


def do_to_nice_json(obj: Any, /, **kwargs: Any) -> str:
    """Serialize data as JSON with nice formatting.

    Args:
        obj: Data to serialize.
        **kwargs: Additional keyword arguments to pass to `json.dumps`.

    Returns:
        Serialized JSON data.
    """
    kwargs.setdefault("skipkeys", False)
    kwargs.setdefault("ensure_ascii", True)
    kwargs.setdefault("check_circular", True)
    kwargs.setdefault("allow_nan", True)
    kwargs.setdefault("indent", 4)
    kwargs.setdefault("sort_keys", True)
    return json.dumps(obj, **kwargs)
