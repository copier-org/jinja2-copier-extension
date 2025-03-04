"""Jinja2 extensions."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from warnings import warn

from jinja2.ext import Extension

from ._filters.base64 import do_b64decode
from ._filters.base64 import do_b64encode
from ._filters.datetime import do_strftime
from ._filters.datetime import do_to_datetime
from ._filters.hash import do_hash
from ._filters.hash import do_md5
from ._filters.hash import do_sha1
from ._filters.json import do_from_json
from ._filters.json import do_to_json
from ._filters.json import do_to_nice_json
from ._filters.path import do_basename
from ._filters.path import do_dirname
from ._filters.path import do_expanduser
from ._filters.path import do_expandvars
from ._filters.path import do_fileglob
from ._filters.path import do_realpath
from ._filters.path import do_relpath
from ._filters.path import do_splitext
from ._filters.path import do_win_basename
from ._filters.path import do_win_dirname
from ._filters.path import do_win_splitdrive
from ._filters.random import do_random
from ._filters.random import do_random_mac
from ._filters.random import do_shuffle
from ._filters.regex import do_regex_escape
from ._filters.regex import do_regex_findall
from ._filters.regex import do_regex_replace
from ._filters.regex import do_regex_search
from ._filters.shell import do_quote
from ._filters.types import do_bool
from ._filters.types import do_type_debug
from ._filters.utils import do_extract
from ._filters.utils import do_flatten
from ._filters.utils import do_groupby
from ._filters.utils import do_mandatory
from ._filters.utils import do_ternary
from ._filters.uuid import do_to_uuid
from ._filters.yaml import do_from_yaml
from ._filters.yaml import do_from_yaml_all
from ._filters.yaml import do_to_nice_yaml
from ._filters.yaml import do_to_yaml

if TYPE_CHECKING:
    from collections.abc import Mapping

    from jinja2 import Environment


# NOTE: mypy disallows `Callable[[Any, ...], Any]`
_filters: Mapping[str, Callable[..., Any]] = {
    "ans_groupby": do_groupby,
    "ans_random": do_random,
    "b64decode": do_b64decode,
    "b64encode": do_b64encode,
    "basename": do_basename,
    "bool": do_bool,
    "checksum": do_sha1,
    "dirname": do_dirname,
    "expanduser": do_expanduser,
    "expandvars": do_expandvars,
    "extract": do_extract,
    "fileglob": do_fileglob,
    "flatten": do_flatten,
    "from_json": do_from_json,
    "from_yaml": do_from_yaml,
    "from_yaml_all": do_from_yaml_all,
    "hash": do_hash,
    "mandatory": do_mandatory,
    "md5": do_md5,
    "quote": do_quote,
    "random_mac": do_random_mac,
    "realpath": do_realpath,
    "regex_escape": do_regex_escape,
    "regex_findall": do_regex_findall,
    "regex_replace": do_regex_replace,
    "regex_search": do_regex_search,
    "relpath": do_relpath,
    "sha1": do_sha1,
    "shuffle": do_shuffle,
    "splitext": do_splitext,
    "strftime": do_strftime,
    "ternary": do_ternary,
    "to_datetime": do_to_datetime,
    "to_json": do_to_json,
    "to_nice_json": do_to_nice_json,
    "to_nice_yaml": do_to_nice_yaml,
    "to_uuid": do_to_uuid,
    "to_yaml": do_to_yaml,
    "type_debug": do_type_debug,
    "win_basename": do_win_basename,
    "win_dirname": do_win_dirname,
    "win_splitdrive": do_win_splitdrive,
}


class CopierExtension(Extension):
    """Jinja2 extension for Copier."""

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        for k, v in _filters.items():
            if k in environment.filters:
                warn(
                    f'A filter named "{k}" already exists in the Jinja2 environment',
                    category=RuntimeWarning,
                    stacklevel=2,
                )
            else:
                environment.filters[k] = v
