"""Jinja2 filters for filesystem paths."""

from __future__ import annotations

import ntpath
import os.path
from pathlib import Path

__all__ = [
    "do_basename",
    "do_dirname",
    "do_expanduser",
    "do_expandvars",
    "do_fileglob",
    "do_realpath",
    "do_relpath",
    "do_splitext",
    "do_win_basename",
    "do_win_dirname",
    "do_win_splitdrive",
]


def do_basename(path: str) -> str:
    """Get the final component of a path.

    Args:
        path: A path.

    Returns:
        The final component of the path.
    """
    return os.path.basename(path)  # noqa: PTH119


def do_dirname(path: str) -> str:
    """Get the directory component of a path.

    Args:
        path: A path.

    Returns:
        The directory component of the path.
    """
    return os.path.dirname(path)  # noqa: PTH120


def do_expanduser(path: str) -> str:
    """Expand a path with the `~` and `~user` constructions.

    Args:
        path: A path.

    Returns:
        The expanded path.
    """
    return os.path.expanduser(path)  # noqa: PTH111


def do_expandvars(path: str) -> str:
    """Expand a path with the shell variables of form `$var` and `${var}`.

    Args:
        path: A path.

    Returns:
        The expanded path.
    """
    return os.path.expandvars(path)


def do_fileglob(pattern: str) -> list[str]:
    """Get all files in a filesystem subtree accoring to a glob pattern.

    Args:
        pattern: A glob pattern.

    Returns:
        The list of files matching the glob pattern.
    """
    return [str(path) for path in Path().glob(pattern) if path.is_file()]


def do_realpath(path: str) -> str:
    """Get the canonical form of a path.

    Args:
        path: A path.

    Returns:
        The canonical path.
    """
    return os.path.realpath(path)


def do_relpath(path: str, start: str) -> str:
    """Get the relative version of a path.

    Args:
        path: A path.
        start: A reference path.

    Returns:
        The path `path` relative to `start`.
    """
    return os.path.relpath(path, start)


def do_splitext(path: str) -> tuple[str, str]:
    """Split the extension of a path.

    Args:
        path: A path.

    Returns:
        A tuple `(root, ext)` or `(root,)`.
    """
    return os.path.splitext(path)  # noqa: PTH122


def do_win_basename(path: str) -> str:
    """Get the final component of a Windows path.

    Args:
        path: A Windows path.

    Returns:
        The final component of the Windows path.
    """
    return ntpath.basename(path)


def do_win_dirname(path: str) -> str:
    """Get the directory component of a Windows path.

    Args:
        path: A Windows path.

    Returns:
        The directory component of the Windows path.
    """
    return ntpath.dirname(path)


def do_win_splitdrive(path: str) -> tuple[str, str]:
    """Split a Windows path into a drive and path.

    Args:
        path: A Windows path.

    Returns:
        A tuple `(drive, path)`.
    """
    return ntpath.splitdrive(path)
