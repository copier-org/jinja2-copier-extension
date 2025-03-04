from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from collections.abc import Iterator
    from collections.abc import Mapping

    from jinja2 import Environment


__all__ = ["build_file_tree", "cd", "render"]


def build_file_tree(spec: Mapping[Path, str]) -> None:
    """Build a file tree based on a specification.

    Args:
        spec:
            A mapping from filesystem paths to file contents.
    """
    for path, contents in spec.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            f.write(dedent(contents))


@contextmanager
def cd(path: Path) -> Iterator[None]:
    """Context manager for changing and restoring the current working directory.

    Args:
        path: The path to change to.
    """
    old_path = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)


def render(env: Environment, template: str, /, **context: Any) -> str:
    """Render a string template."""
    return env.from_string(template).render(context)
