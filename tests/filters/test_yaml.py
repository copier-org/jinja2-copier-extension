"""Tests for YAML (de)serialization filters."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


def test_from_yaml(env: Environment) -> None:
    """Test the `from_yaml` filter with default settings."""
    result = render(
        env,
        """\
        {%- set result = v | from_yaml -%}
        [[- result is mapping -]]|
        [[- result -]]
        """,
        v="k: true",
    )
    assert result == "True|{'k': True}"


def test_from_yaml_all(env: Environment) -> None:
    """Test the `from_yaml_all` filter with default settings."""
    result = render(
        env,
        """\
        {%- set result = v | from_yaml_all -%}
        [[- result is iterable -]]|
        [[- result is not sequence -]]|
        [[- result | list -]]
        """,
        v="k1: v1\n---\nk2: v2",
    )
    assert result == "True|True|[{'k1': 'v1'}, {'k2': 'v2'}]"


def test_to_yaml(env: Environment) -> None:
    """Test the `to_yaml` filter with default settings."""
    assert render(env, "[[ v | to_yaml ]]", v={"k": True}) == "k: true\n"


def test_to_nice_yaml(env: Environment) -> None:
    """Test the `to_nice_yaml` filter with default settings."""
    result = render(env, "[[ v | to_nice_yaml ]]", v={"x": {"y": [1, 2]}, "k": "v"})
    assert result == "k: v\nx:\n    y:\n    - 1\n    - 2\n"


def test_to_nice_yaml_with_custom_indent(env: Environment) -> None:
    """Test the `to_nice_yaml` filter with custom indentation setting."""
    result = render(
        env,
        "[[ v | to_nice_yaml(indent=2) ]]",
        v={"x": {"y": [1, 2]}, "k": "v"},
    )
    assert result == "k: v\nx:\n  y:\n  - 1\n  - 2\n"
