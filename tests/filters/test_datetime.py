"""Tests for date/time filters."""

from __future__ import annotations

import platform
from datetime import datetime
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

import pytest
from time_machine import travel

from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


@travel(datetime(1970, 1, 1, 2, 3, 4, tzinfo=ZoneInfo("America/Los_Angeles")))
@pytest.mark.parametrize(
    ("filter_call", "expected"),
    [
        ("strftime", "02:03:04"),
        ("strftime(12345)", "19:25:45"),
        ("strftime(second=12345)", "19:25:45"),
    ],
)
@pytest.mark.skipif(
    condition=platform.system() not in {"Linux", "Darwin"},
    reason="time zone mocking via `time.tzset()` only works on Unix",
)
def test_strftime(env: Environment, filter_call: str, expected: str) -> None:
    """Test converting a string with date/time information to a `datetime` object."""
    assert render(env, f"[[ '%H:%M:%S' | {filter_call} ]]") == expected


def test_to_datetime(env: Environment) -> None:
    """Test converting a string with date/time inforation to a `datetime` object."""
    result = render(
        env,
        "[[ ((date1 | to_datetime) - (date2 | to_datetime('%Y-%m-%d'))).days ]]",
        date1="2016-08-14 20:00:12",
        date2="2016-08-12",
    )
    assert result == "2"
