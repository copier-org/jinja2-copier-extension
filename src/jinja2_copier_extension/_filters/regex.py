"""Jinja2 filters for regular expressions."""

from __future__ import annotations

import re
from typing import Literal

__all__ = ["do_regex_escape", "do_regex_findall", "do_regex_replace", "do_regex_search"]


_REGEX_ESCAPE_POSIX_BASIC_PATTERN = re.compile(r"([\[\]\.\^\$\*\\])")


def do_regex_escape(
    pattern: str,
    re_type: Literal["python", "posix_basic"] = "python",
) -> str:
    """Escape special characters in a regex pattern string.

    Args:
        pattern: A regex pattern string.
        re_type: A regex pattern type. Defaults to `"python"`.

    Returns:
        The escaped regex pattern string.
    """
    if re_type == "python":
        return re.escape(pattern)
    if re_type == "posix_basic":
        return _REGEX_ESCAPE_POSIX_BASIC_PATTERN.sub(r"\\\1", pattern)
    raise NotImplementedError(f"Unsupported regex type: {re_type}")  # noqa: EM102


def do_regex_findall(
    string: str,
    # TODO(sisp): Rename argument to `pattern` for consistency with other filters.
    regex: str,
    # TODO(sisp): Require flags to be keyword-only arguments.
    multiline: bool = False,  # noqa: FBT001 FBT002
    ignorecase: bool = False,  # noqa: FBT001 FBT002
) -> list[str] | list[tuple[str, ...]]:
    """Extract non-overlapping regex matches using `re.findall`.

    Args:
        string: A string from which to extract matches.
        regex: A regex pattern string.
        multiline: Whether to match the pattern for each line.
        ignorecase: Whether to perform case-insensitive matching.

    Returns:
        A list of strings or string tuples containing the matches.
    """
    flags = _get_flags(ignorecase=ignorecase, multiline=multiline)
    return re.findall(regex, string, flags=flags)


def do_regex_replace(
    string: str,
    pattern: str,
    replacement: str,
    # TODO(sisp): Require flags to be keyword-only arguments.
    ignorecase: bool = False,  # noqa: FBT001 FBT002
    multiline: bool = False,  # noqa: FBT001 FBT002
) -> str:
    """Substitute non-overlapping regex matches using `re.sub`.

    Args:
        string: A string wherein to replace matching substrings.
        pattern: A regex pattern string.
        replacement: A string to replace matching substrings with.
        ignorecase: Whether to perform case-insensitive matching.
        multiline: Whether to match the pattern for each line.

    Returns:
        The string wherein matched substrings have been replaced.
    """
    flags = _get_flags(ignorecase=ignorecase, multiline=multiline)
    return re.sub(pattern, replacement, string, flags=flags)


def do_regex_search(
    string: str,
    pattern: str,
    *args: str,
    ignorecase: bool = False,
    multiline: bool = False,
) -> str | list[str] | None:
    r"""Search a string for a regex match using `re.search`.

    Args:
        string: A string to search.
        pattern: A regex pattern string.
        *args: An optional list of backreferences (`\\g<name>` or `\\number`) to return.
        ignorecase: Whether to perform case-insensitive matching.
        multiline: Whether to match the pattern for each line.

    Returns:
        A string (if the regex matches) or a list of strings (one for each backreference
        match) or `None` (if there is no match).

    Raises:
        ValueError: If the backreference format is invalid.
    """
    groups: list[str | int] = []
    for arg in args:
        if match := re.match(r"^\\g<(\S+)>$", arg):
            groups.append(match.group(1))
        elif match := re.match(r"^\\(\d+)$", arg):
            groups.append(int(match.group(1)))
        else:
            msg = "Invalid backref format"
            raise ValueError(msg)

    flags = _get_flags(ignorecase=ignorecase, multiline=multiline)
    return (match := re.search(pattern, string, flags=flags)) and (
        list(result) if isinstance((result := match.group(*groups)), tuple) else result
    )


def _get_flags(*, ignorecase: bool = False, multiline: bool = False) -> int:
    flags = 0
    if ignorecase:
        flags |= re.IGNORECASE
    if multiline:
        flags |= re.MULTILINE
    return flags
