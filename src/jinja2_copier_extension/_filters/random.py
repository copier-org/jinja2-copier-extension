"""Jinja2 filters for random functions."""

from __future__ import annotations

import re
from random import Random
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import overload

if TYPE_CHECKING:
    from collections.abc import Sequence


__all__ = ["do_random", "do_random_mac", "do_shuffle"]

_T = TypeVar("_T")


def do_shuffle(seq: Sequence[_T], seed: str | None = None) -> list[_T]:
    """Shuffle a sequence of elements.

    Args:
        seq: A sequence of elements.
        seed: A pseudo-random number generator seed.

    Returns:
        The shuffled sequence of elements as a list.
    """
    seq = list(seq)
    Random(seed).shuffle(seq)  # noqa: S311
    return seq


@overload
def do_random(
    stop: int,
    start: int = 0,
    step: int = 1,
    seed: str | None = None,
) -> int: ...


@overload
def do_random(
    stop: Sequence[_T],
    start: None = None,
    step: None = None,
    seed: str | None = None,
) -> _T: ...


def do_random(
    stop: int | Sequence[_T],
    start: int | None = None,
    step: int | None = None,
    seed: str | None = None,
) -> int | _T:
    """Generate a random integer in a range or choose a random element from a sequence.

    Args:
        stop: An exclusive upper bound.
        start: An inclusive lower bound.
        step: A step size.
        seed: A pseudo-random number generator seed.

    Returns:
        A random integer in the specified range.

    Raises:
        ValueError: If `stop` is a sequence and `start` or `step` are not `None`.
    """
    rng = Random(seed)  # noqa: S311

    if isinstance(stop, int):
        if start is None:
            start = 0
        if step is None:
            step = 1
        return rng.randrange(start, stop, step)

    for arg_name, arg_value in [("start", start), ("step", step)]:
        if arg_value is not None:
            msg = f'"{arg_name}" can only be used when "stop" is an integer'
            raise ValueError(msg)
    return rng.choice(stop)


MAC_LENGTH = 6


def do_random_mac(prefix: str, seed: str | None = None) -> str:
    """Generate a random MAC address given a prefix.

    Args:
        prefix: A MAC address prefix of max. 5 parts.
        seed: A pseudo-random number generator seed.

    Returns:
        A random MAC address.

    Raises:
        ValueError: If `prefix` has more than 5 parts or any of the parts is not a
            hexadecimal bytes.
    """
    parts = [] if prefix == "" else prefix.lower().strip(":").split(":")
    if len(parts) >= MAC_LENGTH:
        msg = f'Invalid MAC address prefix "{prefix}": too many parts'
        raise ValueError(msg)
    for part in parts:
        if not re.match(r"[a-f0-9]{2}", part):
            msg = (
                f'Invalid MAC address prefix "{prefix}": '
                f'"{part}" is not a hexadecimal byte'
            )
            raise ValueError(msg)
    rng = Random(seed)  # noqa: S311
    return ":".join(
        parts + [f"{rng.randint(0, 255):02x}" for _ in range(MAC_LENGTH - len(parts))],
    )
