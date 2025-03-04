"""Jinja2 filters for hashing."""

from __future__ import annotations

from hashlib import new

__all__ = ["do_hash", "do_md5", "do_sha1"]


def do_hash(data: str, algorithm: str = "sha1") -> str:
    """Hash data using a configurable algorithm.

    Args:
        data: The data to hash.
        algorithm: The algorithm to use. Defaults to `"sha1"`.

    Returns:
        The hashed data.
    """
    hasher = new(algorithm)
    hasher.update(data.encode())
    return hasher.hexdigest()


def do_md5(data: str) -> str:
    """Hash data using the MD5 algorithm.

    Args:
        data: The data to hash.

    Returns:
        The hashed data.
    """
    return do_hash(data, "md5")


def do_sha1(data: str) -> str:
    """Hash data using the SHA1 algorithm.

    Args:
        data: The data to hash.

    Returns:
        The hashed data.
    """
    return do_hash(data, "sha1")
