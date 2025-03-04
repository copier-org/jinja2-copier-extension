"""Tests for regular expression filters."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING
from typing import Literal

import pytest

from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


def test_regex_escape(env: Environment) -> None:
    """Test escaping of regex characters with the default `re_type`."""
    result = render(env, "[[ v | regex_escape ]]", v=r"^a.*b(.+)\c?$")
    assert result == r"\^a\.\*b\(\.\+\)\\c\?\$"


@pytest.mark.parametrize(
    ("pattern", "re_type", "expected"),
    [
        (r"^a.*b(.+)\c?$", "python", r"\^a\.\*b\(\.\+\)\\c\?\$"),
        (r"^a.*b(.+)\c?$", "posix_basic", r"\^a\.\*b(\.+)\\c?\$"),
    ],
)
def test_regex_escape_with_re_type(
    env: Environment,
    pattern: str,
    re_type: Literal["python", "posix_basic"],
    expected: str,
) -> None:
    """Test escaping of regex characters with explicit `re_type`."""
    result = render(env, "[[ v | regex_escape(re_type=r) ]]", v=pattern, r=re_type)
    assert result == expected


def test_regex_findall(env: Environment) -> None:
    """Test extracting non-overlapping regex matches using `re.findall`."""
    result = render(env, "[[ v | regex_findall('[a-z]+') ]]", v="foo bar")
    assert result == "['foo', 'bar']"


def test_regex_replace(env: Environment) -> None:
    """Test substituting non-overlapping regex matches using `re.sub`."""
    result = render(
        env,
        r"[[ v | regex_replace('^(.*)ier$', '\\1y') ]]",
        v="copier",
    )
    assert result == "copy"


@pytest.mark.parametrize(
    ("value", "filter_call", "expected"),
    [
        ("foo/bar", "regex_search('[a-z]+')", "foo"),
        ("FOO/bar", "regex_search('[a-z]+')", "bar"),
        ("FOO/bar", "regex_search('[a-z]+', ignorecase=True)", "FOO"),
        ("123\nbar", "regex_search('^[a-z]+')", "None"),
        ("123\nbar", "regex_search('^[a-z]+', multiline=True)", "bar"),
        ("2/3", r"regex_search('^([0-9]+)/([0-9]+)$', '\\1', '\\2')", "['2', '3']"),
        (
            "2/3",
            r"regex_search('^(?P<dividend>[0-9]+)/(?P<divisor>[0-9]+)$', '\\g<dividend>', '\\g<divisor>')",  # noqa: E501
            "['2', '3']",
        ),
    ],
)
def test_regex_search(
    env: Environment,
    value: str,
    filter_call: str,
    expected: str,
) -> None:
    """Test searching a string for a regex match using `re.search`."""
    assert render(env, f"[[ v | {filter_call} ]]", v=value) == expected


def test_regex_search_with_invalid_backref_format(env: Environment) -> None:
    """Test searching a string for a regex match with an invalid backref format."""
    with pytest.raises(ValueError, match=re.escape("Invalid backref format")):
        render(env, "[[ 'foo/bar' | regex_search('([a-z]+)', 'invalid-backref') ]]")
