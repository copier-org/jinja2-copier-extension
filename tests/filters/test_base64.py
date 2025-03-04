"""Tests for Base64 encoding/decoding filters."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


@pytest.mark.parametrize(
    "filter_call",
    [
        "b64decode",
        "b64decode('utf-8')",
        "b64decode(encoding='utf-8')",
    ],
)
def test_b64decode(env: Environment, filter_call: str) -> None:
    """Test decoding a Base64 encoded string."""
    assert render(env, f"[[ v | {filter_call} ]]", v="MTIz") == "123"


@pytest.mark.parametrize(
    "filter_call",
    [
        "b64encode",
        "b64encode('utf-8')",
        "b64encode(encoding='utf-8')",
    ],
)
def test_b64encode(env: Environment, filter_call: str) -> None:
    """Test encoding a string using Base64."""
    assert render(env, f"[[ v | {filter_call} ]]", v="123") == "MTIz"
