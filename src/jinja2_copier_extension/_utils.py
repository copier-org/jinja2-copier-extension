"""Utility functions."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from collections.abc import Sequence

    from typing_extensions import TypeGuard


__all__ = ["MISSING", "is_sequence"]

MISSING = object()


def is_sequence(obj: object) -> TypeGuard[Sequence[Any]]:
    """Checks whether an object is a sequence container.

    Args:
        obj: An object.

    Returns:
        `True` if the object is sequence container, `False` otherwise.
    """
    return hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes))
