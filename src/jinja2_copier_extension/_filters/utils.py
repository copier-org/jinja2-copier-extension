"""Jinja2 filters for miscelleaneous use."""

from __future__ import annotations

from functools import reduce
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar

from jinja2 import Undefined
from jinja2 import UndefinedError
from jinja2 import pass_environment
from jinja2.filters import sync_do_groupby

from jinja2_copier_extension._utils import MISSING
from jinja2_copier_extension._utils import is_sequence

if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Sequence

    from jinja2 import Environment

__all__ = ["do_extract", "do_flatten", "do_groupby", "do_mandatory", "do_ternary"]

_T = TypeVar("_T")


@pass_environment
def do_extract(
    environment: Environment,
    key: Any,
    container: Any,
    morekeys: Any | Sequence[Any] | None = None,
) -> Any | Undefined:
    """Extract a value from a container.

    Args:
        environment: A Jinja2 environment instance.
        key: A key to extract a value from a container.
        container: A container from which to extract a value.
        morekeys: Additional keys for extracting a nested value.

    Returns:
        The extracted value. `Undefined` if no value exists for the key.
    """
    keys: list[Any]
    if morekeys is None:
        keys = [key]
    elif is_sequence(morekeys):
        keys = [key, *morekeys]
    else:
        keys = [key, morekeys]
    return reduce(environment.getitem, keys, container)


def do_flatten(seq: Sequence[Any], levels: int | None = None) -> list[Any]:
    """Flatten nested sequences, filter out `None` values.

    Args:
       seq: A sequence of values to flatten.
       levels: The number of levels to flatten. Defaults to `None`, which
           means flatten all levels.

    Returns:
       A flattened list of values.
    """
    if levels is not None:
        if levels < 1:
            return list(seq)
        levels -= 1
    result: list[Any] = []
    for item in seq:
        if is_sequence(item):
            result.extend(do_flatten(item, levels))
        elif item is not None:
            result.append(item)
    return result


@pass_environment
def do_groupby(
    environment: Environment,
    value: Iterable[_T],
    attribute: str | int,
) -> list[tuple[str | int, list[_T]]]:
    """Group a sequence of objects by an attribute.

    Args:
        environment: A Jinja2 environment instance.
        value: A sequence of objects to group.
        attribute: The attribute to group by.

    Returns:
        A list of tuples, where each tuple contains the attribute value and a
        list of objects with that attribute value.
    """
    return list(map(tuple, sync_do_groupby(environment, value, attribute)))


def do_mandatory(value: _T, msg: str | None = None) -> _T:
    """Require a value to be defined.

    Args:
        value: A value that must be defined.
        msg: An error message to raise if the value is undefined. Defaults to
            "Mandatory variable `<variable>` is undefined".

    Returns:
        The provided value.

    Raises:
        UndefinedError: If `value` is undefined.
    """
    if isinstance(value, Undefined):
        if msg is None:
            # See https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Undefined._undefined_name
            var = value._undefined_name or "<unknown>"  # noqa: SLF001
            msg = f"Mandatory variable `{var}` is undefined"
        raise UndefinedError(msg)
    return value


def do_ternary(
    condition: bool | None,  # noqa: FBT001
    true_val: Any,
    false_val: Any,
    none_val: Any = MISSING,
) -> Any:
    """Return a true/false/none value depending on a condition.

    If `condition` is `None` and `none_val` is `MISSING`, then `false_val` is returned.

    Args:
        condition: A boolean condition (or `None`).
        true_val: The value to return if the condition is true.
        false_val: The value to return if the condition is false.
        none_val: The value to return if the condition is `None`. Defaults to
            `MISSING`.

    Returns:
        The value of `true_val`, `false_val`, or `none_val` depending on `condition`.
    """
    if condition is None:
        return false_val if none_val is MISSING else none_val
    if condition:
        return true_val
    return false_val
