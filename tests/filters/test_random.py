"""Tests for random functions filters."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest

from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


def test_shuffle(env: Environment) -> None:
    """Test shuffling a sequence of elements."""
    assert render(env, "[[ v | shuffle(seed='123') ]]", v=[1, 2, 3]) == "[2, 1, 3]"


@pytest.mark.parametrize(
    ("filter_call", "expected"),
    [
        ("ans_random(seed='123')", 93),
        ("ans_random(start=94, step=2, seed='123')", 98),
    ],
)
def test_random_range(env: Environment, filter_call: str, expected: int) -> None:
    """Test generating a random integer in a range."""
    assert render(env, f"[[ v | {filter_call} ]]", v=100) == f"{expected}"


def test_random_choice(env: Environment) -> None:
    """Test choosing a random element from a sequence."""
    assert render(env, "[[ v | ans_random(seed='123') ]]", v=[1, 2, 3]) == "3"


@pytest.mark.parametrize(
    "filter_call",
    [
        "ans_random(step=1)",
        "ans_random(start=0)",
        "ans_random(start=0, step=1)",
    ],
)
def test_random_choice_with_incompatible_args(
    env: Environment,
    filter_call: str,
) -> None:
    """Test choosing a random element from a sequence with incompatible arguments."""
    with pytest.raises(
        ValueError,
        match=r'"(start|step)" can only be used when "stop" is an integer',
    ):
        render(env, f"[[ v | {filter_call} ]]", v=[1, 2, 3])


@pytest.mark.parametrize(
    ("prefix", "expected"),
    [
        ("", "25:a4:fc:1f:87:08"),
        ("52", "52:25:a4:fc:1f:87"),
        ("52:54", "52:54:25:a4:fc:1f"),
        ("52:54:00", "52:54:00:25:a4:fc"),
        ("52:54:00:25", "52:54:00:25:25:a4"),
        ("52:54:00:25:a4", "52:54:00:25:a4:25"),
    ],
)
def test_random_mac(env: Environment, prefix: str, expected: str) -> None:
    """Test generating a random MAC address given a prefix."""
    result = render(env, "[[ v | random_mac(seed='123') ]]", v=prefix)
    assert result == expected


@pytest.mark.parametrize(
    ("prefix", "error"),
    [
        (
            "52:54:xy",
            'Invalid MAC address prefix "52:54:xy": "xy" is not a hexadecimal byte',
        ),
        (
            "52:54:00:25:a4:fc",
            'Invalid MAC address prefix "52:54:00:25:a4:fc": too many parts',
        ),
    ],
)
def test_random_mac_with_invalid_prefix(
    env: Environment,
    prefix: str,
    error: str,
) -> None:
    """Test generating a random MAC address given an invalid prefix."""
    with pytest.raises(ValueError, match=re.escape(error)):
        render(env, "[[ v | random_mac(seed='123') ]]", v=prefix)
