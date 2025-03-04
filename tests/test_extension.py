"""Tests for adding the extension to the Jinja2 environment."""

from __future__ import annotations

from re import escape
from typing import Any

import pytest
from jinja2 import Environment
from jinja2.ext import Extension

from jinja2_copier_extension import CopierExtension


@pytest.mark.parametrize(
    "name",
    [
        "ans_groupby",
        "ans_random",
        "b64decode",
        "b64encode",
        "basename",
        "bool",
        "checksum",
        "dirname",
        "expanduser",
        "expandvars",
        "extract",
        "fileglob",
        "flatten",
        "from_json",
        "from_yaml",
        "from_yaml_all",
        "hash",
        "mandatory",
        "md5",
        "quote",
        "random_mac",
        "realpath",
        "regex_escape",
        "regex_findall",
        "regex_replace",
        "regex_search",
        "relpath",
        "sha1",
        "shuffle",
        "splitext",
        "strftime",
        "ternary",
        "to_datetime",
        "to_json",
        "to_nice_json",
        "to_nice_yaml",
        "to_uuid",
        "to_yaml",
        "type_debug",
        "win_basename",
        "win_dirname",
        "win_splitdrive",
    ],
)
def test_filter_name_conflict(name: str) -> None:
    """Test the behavior when a filter name conflict occurs."""

    def _fake_filter(*args: Any, **kwargs: Any) -> str:
        raise NotImplementedError

    class _TestExtension(Extension):
        def __init__(self, environment: Environment) -> None:
            super().__init__(environment)
            environment.filters[name] = _fake_filter

    with pytest.warns(
        RuntimeWarning,
        match=escape(
            f'A filter named "{name}" already exists in the Jinja2 environment',
        ),
    ):
        env = Environment(extensions=[_TestExtension, CopierExtension])

    assert env.filters[name] == _fake_filter
