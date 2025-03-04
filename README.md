# Copier's built-in Jinja2 Extension

[![Tests](https://img.shields.io/github/actions/workflow/status/copier-org/jinja2-copier-extension/tests.yml?branch=main&label=Tests&labelColor=333&logo=github&style=flat-square)](https://github.com/copier-org/jinja2-copier-extension/actions?query=branch%3Amain)
[![Python versions](https://img.shields.io/pypi/pyversions/jinja2-copier-extension?label=Python&logo=python&logoColor=%23959DA5&style=flat-square)](https://pypi.org/project/jinja2-copier-extension)
[![PyPI](https://img.shields.io/pypi/v/jinja2-copier-extension?label=PyPI&logo=pypi&logoColor=%23959DA5&style=flat-square)](https://pypi.org/project/jinja2-copier-extension)
[![Formatter & Linter: Ruff](https://img.shields.io/badge/-Ruff-261230.svg?labelColor=grey&logo=ruff&logoColor=D7FF64&style=flat-square)](https://github.com/charliermarsh/ruff)
[![Type-checker: mypy](https://img.shields.io/badge/mypy-strict-2A6DB2.svg?style=flat-square)](http://mypy-lang.org)

[Copier][copier]'s built-in [Jinja2 extension][jinja-extensions], inspired by Ansible, outsourced for you.

## Installation

* With [`pip`][pip]:

    ```shell
    pip install jinja2-copier-extension
    ```

* With [`uv`][uv]:

    ```shell
    uv add jinja2-copier-extension
    ```

* With [`poetry`][poetry]:

    ```shell
    poetry add jinja2-copier-extension
    ```

* With [`pdm`][pdm]:

    ```shell
    pdm add jinja2-copier-extension
    ```

* With [`pipx`][pipx] (injected into the `pipx`-managed virtual env of a package):

    ```shell
    pipx inject PACKAGE jinja2-copier-extension
    ```

* With [`uvx`][uvx] (injected into the `uvx`-managed virtual env of a package):

    ```shell
    uvx --with jinja2-copier-extension PACKAGE
    ```

## Usage

Register the extension in your [Jinja2][jinja] environment to use the provided [filters](#filters):

```python
from jinja2 import Environment

env = Environment(extensions=["jinja2_copier_extension.CopierExtension"])

# Example:
template = env.from_string("The current time is {{ '%H:%M' | strftime }}")
result = template.render()
print(result)
```

## Filters

The extension provides the following [Jinja2][jinja] filters:

### Base64

#### `b64decode(value: str, encoding: str = "utf-8") → str`

Decode a Base64 encoded string.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'aGVsbG8gd29ybGQ=' | b64decode }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"hello world"
```

</summary>
</details>

#### `b64encode(value: str, encoding: str = "utf-8") → str`

Encode a Base64 encoded string.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'hello world' | b64encode }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"YSBzdHJpbmc="
```

</summary>
</details>

### Date/Time

#### `strftime(format: str, second: float | None = None) → str`

Convert a Unix timestamp to a date/time string according to a date/time format.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ '%H:%M:%S' | strftime }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"02:03:04"
```

</summary>
</details>

#### `to_datetime(string: str, format: str = "%Y-%m-%d %H:%M:%S") → datetime`

Convert a string containing date/time information to a [`datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects) object.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ '2016-08-14 20:00:12' | to_datetime }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
datetime.datetime(2016, 8, 14, 20, 0, 12)
```

</summary>
</details>

### Hashing

#### `hash(data: str, algorithm: str = "sha1") → str`

Hash data using a configurable algorithm.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'hello world' | hash }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"
```

</summary>
</details>

#### `md5(data: str) → str`

Hash data using the MD5 algorithm.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'hello world' | md5 }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"5eb63bbbe01eeed093cb22bb8f5acdc3"
```

</summary>
</details>

#### `sha1(data: str) → str`

Hash data using the SHA1 algorithm.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'hello world' | sha1 }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"
```

</summary>
</details>

### JSON

#### `from_json(data: str, /, **kwargs: Any) → Any`

Deserialize JSON data.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{% filter from_json %}
{
  "name": "Jane",
  "age": 30
}
{% endfilter %}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
{"name": "Jane", "age": 30}
```

</summary>
</details>

#### `to_json(obj: Any, /, **kwargs: Any) → str`

Serialize an object as JSON.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ {'name': 'Jane', 'age': 30} | to_json }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```json
{"name": "Jane", "age": 30}
```

</summary>
</details>

#### `to_nice_json(obj: Any, /, **kwargs: Any) → str`

Serialize an object as JSON with nice formatting.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ {'name': 'Jane', 'age': 30} | to_nice_json }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```json
{
    "age": 30,
    "name": "Jane"
}
```

</summary>
</details>

### Filesystem

#### `basename(path: str) → str`

Get the final component of a path.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ '/etc/asdf/foo.txt' | basename }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"foo.txt"
```

</summary>
</details>

#### `dirname(path: str) → str`

Get the directory component of a path.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ '/etc/asdf/foo.txt' | basename }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"/etc/asdf"
```

</summary>
</details>

#### `expanduser(path: str) → str`

Expand a path with the `~` and `~user` constructions.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ '~/path/to/foo.txt' | expanduser }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"/home/<user>/path/to/foo.txt"    # Linux
"/Users/<user>/path/to/foo.txt"   # macOS
"C:/Users/<user>/path/to/foo.txt" # Windows
```

</summary>
</details>

#### `expandvars(path: str) → str`

Expand a path with the shell variables of form `$var` and `${var}`.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ '$HOME/path/to/foo.txt' | expandvars }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"/home/<user>/path/to/foo.txt"    # Linux
"/Users/<user>/path/to/foo.txt"   # macOS
"C:/Users/<user>/path/to/foo.txt" # Windows
```

</summary>
</details>

#### `fileglob(pattern: str) → list[str]`

Get all files in a filesystem subtree accoring to a glob pattern.

**Example:**

<details open>
<summary>Filesystem</summary>

```text
📁 .
├── 📄 a.txt
├── 📄 b.csv
└── 📁 c
    ├── 📄 d.txt
    └── 📄 e.json
```

</summary>
</details>

<details open>
<summary>Template</summary>

```jinja
{{ '**/*.txt' | fileglob() | sort }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
["a.txt", "c/d.txt"]
```

</summary>
</details>

#### `realpath(path: str) → str`

Get the canonical form of a path.

**Example:**

<details open>
<summary>Filesystem</summary>

```text
📁 .
└── 📁 a
    ├── 📁 b
    │   └── 📄 foo.txt
    └── 📁 c
        └── 📄 bar.txt
```

</summary>
</details>

<details open>
<summary>Template</summary>

```jinja
{{ 'a/c/../b/foo.txt' | realpath }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"<cwd>/a/b/foo.txt"
```

</summary>
</details>

#### `splitext(path: str) → tuple[str, str]`

Split the extension of a path.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'foo.txt' | splitext }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
("foo", ".txt")
```

</summary>
</details>

#### `win_basename(path: str) → str`

Get the final component of a Windows path.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'C:/Temp/asdf/foo.txt' | win_basename }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"foo.txt"
```

</summary>
</details>

#### `win_dirname(path: str) → str`

Get the directory component of a Windows path.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'C:/Temp/asdf/foo.txt' | win_dirname }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"C:/Temp/asdf"
```

</summary>
</details>

#### `win_splitdrive(path: str) → tuple[str, str]`

Split a Windows path into a drive and path.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'C:/Temp/asdf/foo.txt' | win_splitdrive }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
("C:", "/Temp/asdf/foo.txt")
```

</summary>
</details>

### Random

#### `shuffle[T](seq: Sequence[T], seed: str | None = None) → list[T]`

Shuffle a sequence of elements.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ [1, 2, 3] | shuffle(seed=123) }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
[2, 1, 3]
```

</summary>
</details>

#### `ans_random[T](stop: int | Sequence[T], start: int = 0, step: int = 0, seed: str | None = None) → int | T`

Generate a random integer in a range or choose a random element from a sequence.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 100 | ans_random(seed='123') }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
93
```

</summary>
</details>

#### `random_mac(prefix: str, seed: str | None = None) → str`

Generate a random MAC address given a prefix.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ '52:54' | random_mac(seed='123') }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"52:54:25:a4:fc:1f"
```

</summary>
</details>

### Regular expressions

#### `regex_escape(pattern: str, re_type: Literal["python", "posix_basic"] = "python") → str`

Escape special characters in a regex pattern string.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ '^a.*b(.+)\c?$' | regex_escape }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
r"\^a\.\*b\(\.\+\)\\c\?\$"
```

</summary>
</details>

#### `regex_findall(string: str, regex: str, multiline: bool = False, ignorecase: bool = False) → list[str] | list[tuple[str, ...]]`

Extract non-overlapping regex matches using `re.findall`.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'foo bar' | regex_findall('[a-z]+') }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
["foo", "bar"]
```

</summary>
</details>

#### `regex_replace(string: str, pattern: str, replacement: str, ignorecase: bool = False, multiline: bool = False) → str`

Substitute non-overlapping regex matches using `re.sub`.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'copier' | regex_replace('^(.*)ier$', '\\1y') }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"copy"
```

</summary>
</details>

#### `regex_search(string: str, pattern: str, *args: str, ignorecase: bool = False, multiline: bool = False) → str | list[str] | None`

Search a string for a regex match using `re.search`.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'foo/bar' | regex_search('[a-z]+') }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"foo"
```

</summary>
</details>

### Shell

#### `quote(value: str) → str`

Shell-escape a string.

**Example:**

<details open>
<summary>Template</summary>

```jinja
echo {{ 'hello world' | quote }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"echo 'hello world'"
```

</summary>
</details>

### Types

#### `bool(value: Any) → bool`

Parse anything to boolean.

1. Cast to number. Then: `0 → False`; anything else `→ True`.
1. Find [YAML booleans](https://yaml.org/type/bool.html), [YAML nulls](https://yaml.org/type/null.html) or `"none"` in it and use it appropriately.
1. Cast to boolean using standard Python `bool(value)`.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'yes' | bool }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
True
```

</summary>
</details>

#### `type_debug(obj: object) → str`

Get the type name of an object.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 123 | type_debug }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"int"
```

</summary>
</details>

### Utilities

#### `ans_groupby[V](value: Iterable[V], attribute: str | int) → list[tuple[str | int, list[V]]]`

Group a sequence of objects by an attribute.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ [{'name': 'Jane', 'age': 30}, {'name': 'Alice', 'age': 30}, {'name': 'John', 'age': 20}] | ans_groupby('age') }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
[(20, [{"name": "John", "age": 20}]), (30, [{"name": "Jane", "age": 30}, {"name": "Alice", "age": 30}])]
```

</summary>
</details>

#### `extract(key: Any, container: Any, morekeys: Any | Sequence[Any] | None = None) → Any | Undefined`

Extract a value from a container.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'k' | extract({'k': 'v'}) }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"v"
```

</summary>
</details>

#### `flatten(seq: Sequence[Any], levels: int | None = None) → list[Any]`

Flatten nested sequences, filter out `None` values.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ [1, [None, [2, None, [3]]]] | flatten }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
[1, 2, 3]
```

</summary>
</details>

#### `mandatory[T](value: T, msg: str | None = None) → T`

Require a value to be defined.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'foo' | mandatory }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"foo"
```

</summary>
</details>

#### `ternary(condition: bool | None, true_val: Any, false_val: Any, none_val: Any = MISSING) → Any`

Return a true/false/none value depending on a condition.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'true' | ternary('t', 'f') }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"t"
```

</summary>
</details>

### UUID

#### `to_uuid(name: str) → str`

Generate a UUID v5 string from a name.

The UUID namespace is the DNS namespace `https://github.com/copier-org/copier`.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ 'foo' | to_uuid }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
"faf9357a-ee2a-58ed-94fd-cc8661984561"
```

</summary>
</details>

### YAML

#### `from_yaml(value: str) → Any`

Deserialize YAML data.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{% filter from_yaml %}
name: Jane
age: 30
{% endfilter %}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
{"name": "Jane", "age": 30}
```

</summary>
</details>

#### `from_yaml_all(value: str) → Iterator[Any]`

Deserialize multi-document YAML data.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{% filter from_yaml | list %}
name: Jane
age: 30
---
name: John
age: 20
{% endfilter %}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```python
[{"name": "Jane", "age": 30}, {"name": "John", "age": 20}]
```

</summary>
</details>

#### `to_yaml(value: Any, /, **kwargs: Any) → str`

Serialize data as YAML.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ [{'name': 'Jane', 'age': 30}] | to_yaml }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```yaml
- name: Jane
  age: 30'
```

</summary>
</details>

#### `to_nice_yaml(value: Any, /, **kwargs: Any) → str`

Serialize data as YAML with nice formatting.

**Example:**

<details open>
<summary>Template</summary>

```jinja
{{ [{'name': 'Jane', 'age': 30}] | to_nice_yaml }}
```

</summary>
</details>

<details open>
<summary>Output</summary>

```yaml
-   name: Jane
    age: 30
```

</summary>
</details>

## Contributions

Contributions are always welcome via filing [issues](https://github.com/copier-org/jinja2-copier-extension/issues) or submitting [pull requests](https://github.com/copier-org/jinja2-copier-extension/pulls). Please check the [contribution guide][contribution-guide] for more details.

[contribution-guide]: https://github.com/copier-org/jinja2-copier-extension/blob/main/CONTRIBUTING.md
[copier]: https://github.com/copier-org/copier
[jinja]: https://jinja.palletsprojects.com
[jinja-extensions]: https://jinja.palletsprojects.com/en/latest/extensions/
[pdm]: https://pdm.fming.dev
[pip]: https://pip.pypa.io
[pipx]: https://pypa.github.io/pipx
[poetry]: https://python-poetry.org
[uv]: https://docs.astral.sh/uv/
[uvx]: https://docs.astral.sh/uv/guides/tools/#running-tools
