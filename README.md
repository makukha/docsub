# docsub
> Embed text and data into Markdown files

[![license](https://img.shields.io/github/license/makukha/docsub.svg)](https://github.com/makukha/docsub/blob/main/LICENSE)
[![versions](https://img.shields.io/pypi/pyversions/docsub.svg)](https://pypi.org/project/tox-multipython)
[![pypi](https://img.shields.io/pypi/v/docsub.svg#v0.5.0)](https://pypi.python.org/pypi/docsub)
[![uses docsub](https://img.shields.io/badge/uses-docsub-royalblue)
](https://github.com/makukha/docsub)

> [!WARNING]
> * With `docsub`, every documentation file may become executable.
> * Never use `docsub` to process files from untrusted sources.
> * This project is in research stage, syntax and functionality may change significantly.
> * If still want to try it, use pinned package version `docsub==0.5.0`


# Features

* Insert static files and dynamic results
* Invisible markup inside comment blocks
* Idempotent substitutions
* Configurable
* Plays nicely with other markups

> [!NOTE]
> This file uses [docsub]() itself. Dig into raw markup if interested.

## Planned features

* More commands
* Backup target files
* Dependency discovery
* Extensibility by end user
* Detailed logging


# Use cases

* Synchronized docs for multiple targets: GitHub README, PyPI README, Sphinx docs, etc.
* Embed dynamically generated data as tables
* CLI usage examples

## Non-use cases

* Not a documentation engine like [Sphinx](https://www.sphinx-doc.org) or [MkDocs](https://www.mkdocs.org).
* Not a templating engine like [Jinja](https://jinja.palletsprojects.com).
* Not a replacement for [Bump My Version](https://callowayproject.github.io/bump-my-version)


# Installation

```shell
uv tool install docsub==0.5.0
```

# Basic usage

```shell
$ uvx docsub -i README.md
```

## Get this

<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/__result__.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
# Title
<!-- docsub: begin -->
<!-- docsub: include info.md -->
<!-- docsub: include features.md -->
> Long description.
* Feature 1
* Feature 2
* Feature 3
<!-- docsub: end -->

## Table
<!-- docsub: begin -->
<!-- docsub: include data.md -->
<!-- docsub: lines after 2 -->
| Col 1 | Col 2 |
|-------|-------|
| Key 1 | value 1 |
| Key 2 | value 2 |
| Key 3 | value 3 |
<!-- docsub: end -->

## Code
<!-- docsub: begin #code -->
<!-- docsub: include func.py -->
<!-- docsub: lines after 1 upto -1 -->
```python
def func():
    pass
```
<!-- docsub: end #code -->
````
<!-- docsub: end #readme -->

## From these

<table>
<tr>
<td style="vertical-align:top">

### README.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/README.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
# Title
<!-- docsub: begin -->
<!-- docsub: include info.md -->
<!-- docsub: include features.md -->
...
<!-- docsub: end -->

## Table
<!-- docsub: begin -->
<!-- docsub: include data.md -->
<!-- docsub: lines after 2 -->
| Col 1 | Col 2 |
|-------|-------|
...
<!-- docsub: end -->

## Code
<!-- docsub: begin #code -->
<!-- docsub: include func.py -->
<!-- docsub: lines after 1 upto -1 -->
```python
...
```
<!-- docsub: end #code -->
````
<!-- docsub: end #readme -->

</td>
<td style="vertical-align:top">

### info.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/info.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
> Long description.
````
<!-- docsub: end #readme -->

### features.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/features.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
* Feature 1
* Feature 2
* Feature 3
````
<!-- docsub: end #readme -->

### data.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/data.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
| Key 1 | value 1 |
| Key 2 | value 2 |
| Key 3 | value 3 |
````
<!-- docsub: end #readme -->

### func.py
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/func.py -->
<!-- docsub: lines after 1 upto -1 -->
````python
def func():
    pass
````
<!-- docsub: end #readme -->

</td>
</tr>
</table>


# CLI Reference

<!-- docsub: begin -->
<!-- docsub: help python -m docsub -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ docsub --help
Usage: python -m docsub [OPTIONS] [FILE]...

Update documentation files with external content.

╭─ Options ────────────────────────────────────────────────╮
│ --in-place  -i    Overwrite source files.                │
│ --version         Show the version and exit.             │
│ --help            Show this message and exit.            │
╰──────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->


# Syntax reference

## Substitution block

```markdown
<!-- docsub: begin -->
<!-- docsub: help docsub -->
<!-- docsub: include CHANGELOG.md -->
Inner text will be replaced.
<!-- docsub: this whole line is treated as plain text -->
This text will be replaced too.
<!-- docsub: end -->
```

Each block starts with `begin` and ends with `end`. One or many commands come at the top of the block, otherwise they are treated as plain text. Blocks without *producing commands* are not allowed. Block's inner text will be replaced upon substitution, unless modifier command `lines` is used.

If docsub substitution block leis inside markdown fenced Code block, it is not substituted (examples: fenced code blocks right above and below). To put dynamic content int fenced code block, place `begin` and `end` around it and use `lines after 1 upto -1` (example: Basic usage section).

For nested blocks, only top level substitution is performed. Use block `#identifier` to distinguish nesting levels.

```markdown
<!-- docsub: begin #top -->
<!-- docsub: include part.md -->
<!-- docsub: begin -->
<!-- docsub: include nested.md -->
<!-- docsub: end -->
<!-- docsub: end #top -->
```

## Commands

* Block delimiters: `begin`, `end`
* *Producing commands*: `exec`, `help`, `include`
* *Modifying commands*: `lines`, `strip`

### `begin`
```text
begin [#identifier]
```
Open substitution target block. To distinguish with nested blocks, use `#identifier` starting with `#`.

### `end`
```text
end [#identifier]
```
Close substitution target block.

### `exec`
```text
exec arbitrary commands
```
Execute `arbitrary commands` with `sh -c` and substitute stdout. Allows pipes and other shell functionality. If possible, avoid using this command.

Config options:

* `workdir` — shell working directory, default `'.'`
* `env` — additional environment variables dict, default `{}`

### `help`

```text
help command [subcommand...]
help python -m command [subcommand...]
```
Display help for CLI utility or Python module. Use this command to document CLI instead of `exec`. Runs `command args --help` or `python -m command args --help` respectively. `command [subcommands...]` can only be a space-separated sequence of `[-._a-zA-Z0-9]` characters.

Config options:

* `env` — additional environment variables dict, default `{}`

### `include`
```text
include path/to/file
```
Literally include file specified by path relative to `workdir` config option.

Config options:

* `basedir` — base directory for relative paths

### `lines`
```text
lines [after N] [upto -M]
```
Upon substitution, keep original target block lines: first `N` and/or last `M`. Only one `lines` command is allowed inside the block.

### `strip`
```text
strip
```
Strip trailing whitespaces on every line of substitution result; strip initial and trailing blank lines of substitution result.


# Configuration

Configuration resolution order

* environment variables *(to be documented)*
* `.docsub.toml` config file in current working directory
* `pyproject.toml`, section `[tool.docsub]` *(to be implemented)*
* default config values

## Environment variables

*(to be documented)*

## Example

All config keys are optional.


```toml
[command.exec]
env = {}  # default
workdir = "."  # default

[command.help]
env = { COLUMNS = "60" }

[command.include]
basedir = "."  # default

[logging]
# level = "DEBUG"  # default: missing value
```

> [!WARNING]
> In future releases config keys will be moved under `[tool.docsub]` root, this will be a breaking change.


# Logging

Docsub uses [loguru](https://loguru.readthedocs.io) for logging. Logging is disabled by default. To enable logging, set config option `log_level` to one of [logging levels](https://loguru.readthedocs.io/en/stable/api/logger.html#levels) supported by loguru.

*(logging is rudimentary at the moment)*


# History

This project appeared to maintain docs for [multipython](https://github.com/makukha/multipython) project. You may check it up for usage examples.


# Authors

* [Michael Makukha](https://github.com/makukha)


# License

[MIT License](https://github.com/makukha/caseutil/blob/main/LICENSE)


# Changelog

Check repository [CHANGELOG.md](https://github.com/makukha/multipython/tree/main/CHANGELOG.md)
