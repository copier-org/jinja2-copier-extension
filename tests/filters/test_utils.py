"""Tests for miscelleaneous filters."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING
from typing import Any

import pytest
from jinja2 import UndefinedError

from tests.utils import render

if TYPE_CHECKING:
    from collections.abc import Sequence

    from jinja2 import Environment


@pytest.mark.parametrize(
    ("filter_call", "key", "expected"),
    [
        ("extract({'k': 'v'})", "k", "v"),
        ("extract(['a', 'b'])", 1, "b"),
        ("extract({'k': ['a', 'b']}, 1)", "k", "b"),
        ("extract({'k': ['a', {'x': 'y'}]}, [1, 'x'])", "k", "y"),
        ("extract({'k': 'v'}) is undefined", "missing", "True"),
        ("extract({'k': 'v'}, 'missing') is undefined", "k", "True"),
        ("extract({'k': 'v'}, ['missing']) is undefined", "k", "True"),
    ],
)
def test_extract(env: Environment, filter_call: str, key: Any, expected: str) -> None:
    """Test extracting a value from a container."""
    assert render(env, f"[[ k | {filter_call} ]]", k=key) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ([], "[]"),
        ([1], "[1]"),
        ([1, [2]], "[1, 2]"),
        ([1, 2, [3, [4, 5]]], "[1, 2, 3, 4, 5]"),
        ([None], "[]"),
        ([1, None, 3], "[1, 3]"),
        ([1, [None, [2, None, [3]]]], "[1, 2, 3]"),
    ],
)
def test_flatten(env: Environment, value: Sequence[Any], expected: str) -> None:
    """Test flattening nested lists."""
    assert render(env, "[[ v | flatten ]]", v=value) == expected


@pytest.mark.parametrize(
    ("value", "levels", "expected"),
    [
        ([], 0, "[]"),
        ([], 1, "[]"),
        ([1, 2, [3, [4, 5]]], 0, "[1, 2, [3, [4, 5]]]"),
        ([1, 2, [3, [4, 5]]], 1, "[1, 2, 3, [4, 5]]"),
        ([1, 2, [3, [4, 5]]], 2, "[1, 2, 3, 4, 5]"),
    ],
)
def test_flatten_with_levels(
    env: Environment,
    value: Sequence[Any],
    levels: int,
    expected: str,
) -> None:
    """Test flattening nested lists with levels."""
    assert render(env, "[[ v | flatten(levels=l) ]]", v=value, l=levels) == expected


def test_groupby(env: Environment) -> None:
    """Test grouping a sequence of objects by an attribute."""
    value = [
        {"name": "Jane", "age": 30},
        {"name": "Alice", "age": 30},
        {"name": "John", "age": 20},
    ]
    expected = [
        (20, [{"name": "John", "age": 20}]),
        (30, [{"name": "Jane", "age": 30}, {"name": "Alice", "age": 30}]),
    ]
    assert render(env, "[[ v | ans_groupby('age') ]]", v=value) == f"{expected}"


def test_mandatory(env: Environment) -> None:
    """Test requiring a variable to be defined when it is defined."""
    assert render(env, "[[ v | mandatory ]]", v="foo") == "foo"


def test_mandatory_with_undefined_value(env: Environment) -> None:
    """Test requiring a variable to be defined when it is undefined."""
    with pytest.raises(
        UndefinedError,
        match=re.escape("Mandatory variable `v` is undefined"),
    ):
        render(env, "[[ v | mandatory ]]")


@pytest.mark.parametrize(
    ("condition", "expected"),
    [(True, "t"), (False, "f"), (None, "f")],
)
def test_ternary(env: Environment, condition: bool | None, expected: str) -> None:
    """Test ternary filter."""
    result = render(env, "[[ c | ternary('t', 'f') ]]", c=condition)
    assert result == expected


@pytest.mark.parametrize(
    ("condition", "expected"),
    [(True, "t"), (False, "f"), (None, "n")],
)
def test_ternary_with_none_val(
    env: Environment,
    condition: bool | None,
    expected: str,
) -> None:
    """Test ternary filter with a "none" value."""
    result = render(env, "[[ c | ternary('t', 'f', 'n') ]]", c=condition)
    assert result == expected
