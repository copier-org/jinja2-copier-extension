"""Tests for UUID filters."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


def test_to_uuid(env: Environment) -> None:
    """Test generating a UUID from a name."""
    result = render(env, "[[ 'foo' | to_uuid ]]")
    assert result == "faf9357a-ee2a-58ed-94fd-cc8661984561"
