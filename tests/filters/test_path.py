"""Tests for filesystem path filters."""

from __future__ import annotations

import platform
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from pychoir import MatchesRegex

from tests.utils import build_file_tree
from tests.utils import cd
from tests.utils import render

if TYPE_CHECKING:
    from jinja2 import Environment


def test_basename(env: Environment) -> None:
    """Test getting the final component of a path."""
    assert render(env, "[[ v | basename ]]", v="/etc/asdf/foo.txt") == "foo.txt"


def test_dirname(env: Environment) -> None:
    """Test getting the directory component of a path."""
    assert render(env, "[[ v | dirname ]]", v="/etc/asdf/foo.txt") == "/etc/asdf"


def test_expanduser(env: Environment) -> None:
    """Test expanding a path with `~` and `~user` constructions."""
    result = render(env, "[[ v | expanduser ]]", v="~/path/to/foo.txt")
    assert result == MatchesRegex(
        {
            "Linux": r"/home/[^/]+/path/to/foo\.txt",
            "Darwin": r"/Users/[^/]+/path/to/foo\.txt",
            "Windows": r"[A-Z]:(/|\\)Users(/|\\)[^/\\]+(/|\\)path(/|\\)to(/|\\)foo\.txt",  # noqa: E501
        }[platform.system()],
    )


@pytest.mark.parametrize("var", ["$HOME", "${HOME}"])
def test_expandvars(env: Environment, var: str) -> None:
    """Test expanding a path with shell variables of form `$var` and `${var}`."""
    result = render(env, "[[ v | expandvars ]]", v=f"{var}/path/to/foo.txt")
    assert result == MatchesRegex(
        {
            "Linux": r"/home/[^/]+/path/to/foo\.txt",
            "Darwin": r"/Users/[^/]+/path/to/foo\.txt",
            "Windows": r"[A-Z]:(/|\\)Users(/|\\)[^/\\]+(/|\\)path(/|\\)to(/|\\)foo\.txt",  # noqa: E501
        }[platform.system()],
    )


def test_fileglob(env: Environment, tmp_path: Path) -> None:
    """Test getting all files in a filesystem subtree accoring to a glob pattern."""
    build_file_tree(
        {
            tmp_path / "a.txt": "",
            tmp_path / "b.csv": "",
            tmp_path / "c" / "d.txt": "",
            tmp_path / "c" / "e.json": "",
        },
    )
    with cd(tmp_path):
        result = render(env, "[[ v | fileglob() | sort | join('|') ]]", v="**/*.txt")
        assert result == f"{Path('a.txt')}|{Path('c', 'd.txt')}"


def test_realpath(env: Environment, tmp_path: Path) -> None:
    """Test getting the canonical form of a path."""
    build_file_tree(
        {
            tmp_path / "a" / "b" / "foo.txt": "",
            tmp_path / "a" / "c" / "bar.txt": "",
        },
    )
    result = render(env, "[[ v | realpath ]]", v=f"{tmp_path}/a/c/../b/foo.txt")
    assert result == f"{tmp_path / 'a' / 'b' / 'foo.txt'}"


@pytest.mark.parametrize(
    ("path", "start", "expected"),
    [
        pytest.param(
            "/etc/asdf/foo.txt",
            "/etc",
            "asdf/foo.txt",
            marks=pytest.mark.skipif(
                condition=platform.system() not in {"Linux", "Darwin"},
                reason="relative path on Unix",
            ),
        ),
        pytest.param(
            "C:\\Temp\\asdf\\foo.txt",
            "C:\\Temp",
            "asdf\\foo.txt",
            marks=pytest.mark.skipif(
                condition=platform.system() != "Windows",
                reason="relative path on Windows",
            ),
        ),
    ],
)
def test_relpath(env: Environment, path: str, start: str, expected: str) -> None:
    """Test getting the relative version of a path."""
    result = render(env, "[[ path | relpath(start) ]]", path=path, start=start)
    assert result == expected


def test_splitext(env: Environment) -> None:
    """Test splitting the extension of a path."""
    assert render(env, "[[ v | splitext | join(' + ') ]]", v="foo.txt") == "foo + .txt"


@pytest.mark.parametrize("path", ["C:\\Temp\\asdf\\foo.txt", "C:/Temp/asdf/foo.txt"])
def test_win_basename(env: Environment, path: str) -> None:
    """Test getting the final component of a Windows path."""
    result = render(env, "[[ v | win_basename ]]", v=path)
    assert result == "foo.txt"


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("C:\\Temp\\asdf\\foo.txt", "C:\\Temp\\asdf"),
        ("C:/Temp/asdf/foo.txt", "C:/Temp/asdf"),
    ],
)
def test_win_dirname(env: Environment, path: str, expected: str) -> None:
    """Test getting the directory component of a Windows path."""
    assert render(env, "[[ v | win_dirname ]]", v=path) == expected


@pytest.mark.parametrize(
    ("path", "expected_drive", "expected_path"),
    [
        ("C:\\Temp\\asdf\\foo.txt", "C:", "\\Temp\\asdf\\foo.txt"),
        ("C:/Temp/asdf/foo.txt", "C:", "/Temp/asdf/foo.txt"),
    ],
)
def test_win_splitdrive(
    env: Environment,
    path: str,
    expected_drive: str,
    expected_path: str,
) -> None:
    """Test splitting a Windows path into a drive and path."""
    result = render(env, "[[ v | win_splitdrive | join(' + ') ]]", v=path)
    assert result == f"{expected_drive} + {expected_path}"
