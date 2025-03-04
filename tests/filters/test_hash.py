"""Tests for hashing filters."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


def test_hash_with_default_algorithm(env: Environment) -> None:
    """Test the `hash` filter with its default algorithm (SHA1)."""
    result = render(env, "[[ v | hash ]]", v="test2")
    assert result == "109f4b3c50d7b0df729d299bc6f8e9ef9066971f"


@pytest.mark.parametrize(
    "filter_call",
    [
        "hash('sha1')",
        "hash(algorithm='sha1')",
    ],
)
def test_hash_with_sha1_algorithm(env: Environment, filter_call: str) -> None:
    """Test the `hash` filter with its default algorithm (SHA1)."""
    result = render(env, f"[[ v | {filter_call} ]]", v="test2")
    assert result == "109f4b3c50d7b0df729d299bc6f8e9ef9066971f"


@pytest.mark.parametrize(
    "filter_call",
    [
        "hash('md5')",
        "hash(algorithm='md5')",
    ],
)
def test_hash_with_md5_algorithm(env: Environment, filter_call: str) -> None:
    """Test the `hash` filter with a custom algorithm."""
    result = render(env, f"[[ v | {filter_call} ]]", v="test2")
    assert result == "ad0234829205b9033196ba818f7a872b"


def test_sha1(env: Environment) -> None:
    """Test the `sha1` filter."""
    result = render(env, "[[ v | sha1 ]]", v="test2")
    assert result == "109f4b3c50d7b0df729d299bc6f8e9ef9066971f"


def test_md5(env: Environment) -> None:
    """Test the `md5` filter."""
    result = render(env, "[[ v | md5 ]]", v="test2")
    assert result == "ad0234829205b9033196ba818f7a872b"


def test_checksum(env: Environment) -> None:
    """Test the `checksum` filter."""
    result = render(env, "[[ v | checksum ]]", v="test2")
    assert result == "109f4b3c50d7b0df729d299bc6f8e9ef9066971f"
