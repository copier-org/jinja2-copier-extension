"""Tests for filters related to types."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

import pytest

from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (True, True),
        (False, False),
        (None, False),
        (0, False),
        (1, True),
        (2, True),
        (3, True),
        (0.0, False),
        (1.1, True),
        (2.2, True),
        (-1.1, True),
        ("y", True),
        ("Y", True),
        ("yes", True),
        ("YES", True),
        ("yEs", True),
        ("t", True),
        ("T", True),
        ("true", True),
        ("TRUE", True),
        ("tRuE", True),
        ("on", True),
        ("ON", True),
        ("oN", True),
        ("n", False),
        ("N", False),
        ("no", False),
        ("nO", False),
        ("f", False),
        ("F", False),
        ("false", False),
        ("FALSE", False),
        ("fAlSe", False),
        ("off", False),
        ("OFF", False),
        ("oFf", False),
        ("~", False),
        ("null", False),
        ("NULL", False),
        ("nUlL", False),
        ("none", False),
        ("NONE", False),
        ("nOnE", False),
    ],
)
def test_bool(env: Environment, value: Any, expected: bool) -> None:
    """Test getting the type name of an object."""
    assert render(env, "[[ v | bool is boolean ]]", v=value) == "True"
    assert render(env, "[[ v | bool ]]", v=value) == str(expected)


@pytest.mark.parametrize(("obj", "expected"), [("foo", "str"), (123, "int")])
def test_type_debug(env: Environment, obj: object, expected: str) -> None:
    """Test getting the type name of an object."""
    assert render(env, "[[ v | type_debug ]]", v=obj) == expected
