"""Tests for JSON (de)serialization filters."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


def test_from_json(env: Environment) -> None:
    """Test the `from_json` filter with default settings."""
    assert render(env, "[[ v | from_json ]]", v='"München"') == "München"


def test_to_json(env: Environment) -> None:
    """Test the `to_json` filter with default settings."""
    assert render(env, "[[ v | to_json ]]", v="München") == r'"M\u00fcnchen"'


def test_to_json_with_ensure_ascii_false(env: Environment) -> None:
    """Test the `to_json` filter with `ensure_ascii=False`."""
    result = render(env, "[[ v | to_json(ensure_ascii=False) ]]", v="München")
    assert result == '"München"'


def test_to_nice_json(env: Environment) -> None:
    """Test the `to_nice_json` filter with default settings."""
    result = render(env, "[[ v | to_nice_json ]]", v={"x": [1, 2], "k": "v"})
    assert result == '{\n    "k": "v",\n    "x": [\n        1,\n        2\n    ]\n}'


def test_to_nice_json_with_custom_indent(env: Environment) -> None:
    """Test the `to_nice_json` filter with custom indentation setting."""
    result = render(env, "[[ v | to_nice_json(indent=2) ]]", v={"x": [1, 2], "k": "v"})
    assert result == '{\n  "k": "v",\n  "x": [\n    1,\n    2\n  ]\n}'
