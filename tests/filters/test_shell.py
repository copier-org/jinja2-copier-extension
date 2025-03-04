"""Tests for shell interaction filters."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


def test_quote(env: Environment) -> None:
    """Test shell-escaping a string."""
    assert render(env, "echo [[ v | quote ]]", v="hello world") == "echo 'hello world'"
