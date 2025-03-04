"""Jinja2 filters for YAML (de)serialization."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

import yaml

if TYPE_CHECKING:
    from collections.abc import Iterator

__all__ = ["do_from_yaml", "do_from_yaml_all", "do_to_nice_yaml", "do_to_yaml"]


def do_from_yaml(value: str) -> Any:
    """Deserialize YAML data.

    Args:
       value: YAML data to deserialize.

    Returns:
       Deserialized YAML data.
    """
    return yaml.load(value, Loader=yaml.SafeLoader)


def do_from_yaml_all(value: str) -> Iterator[Any]:
    """Deserialize multi-document YAML data.

    Args:
       value: YAML data to deserialize.

    Returns:
       Deserialized YAML data with one item per YAML document.
    """
    return yaml.load_all(value, Loader=yaml.SafeLoader)


def do_to_yaml(value: Any, /, **kwargs: Any) -> str:
    """Serialize data as YAML.

    Args:
        value: Data to serialize.
        **kwargs: Additional keyword arguments to pass to `yaml.dump`.

    Returns:
        Serialized YAML data.
    """
    kwargs.setdefault("allow_unicode", True)
    return yaml.dump(value, **kwargs)  # type: ignore[no-any-return]


def do_to_nice_yaml(value: Any, /, **kwargs: Any) -> str:
    """Serialize data as YAML with nice formatting.

    Args:
        value: Data to serialize.
        **kwargs: Additional keyword arguments to pass to `yaml.dump`.

    Returns:
        Serialized YAML data.
    """
    kwargs.setdefault("allow_unicode", True)
    kwargs.setdefault("indent", 4)
    return yaml.dump(value, **kwargs)  # type: ignore[no-any-return]
