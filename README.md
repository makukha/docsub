# docsub
> Substitute dynamically generated content in Markdown files

[![license](https://img.shields.io/github/license/makukha/docsub.svg)](https://github.com/makukha/docsub/blob/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/docsub.svg#v0.8.2)](https://pypi.python.org/pypi/docsub)
[![python versions](https://img.shields.io/pypi/pyversions/docsub.svg)](https://pypi.org/project/docsub)
[![tests](https://raw.githubusercontent.com/makukha/docsub/v0.8.2/docs/_static/badge-tests.svg)](https://github.com/makukha/docsub)
[![coverage](https://raw.githubusercontent.com/makukha/docsub/v0.8.2/docs/_static/badge-coverage.svg)](https://github.com/makukha/docsub)
[![tested with multipython](https://img.shields.io/badge/tested_with-multipython-x)](https://github.com/makukha/multipython)
[![uses docsub](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/makukha/docsub/refs/heads/main/docs/badge/v1.json)](https://github.com/makukha/docsub)
[![mypy](https://img.shields.io/badge/type_checked-mypy-%231674b1)](http://mypy.readthedocs.io)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/ruff)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> [!WARNING]
> * With `docsub`, every documentation file may become executable.
> * Never use `docsub` to process files from untrusted sources.
> * This project is in experimental state, syntax and functionality may change significantly.
> * If still want to try it, use pinned package version `docsub==0.8.2`


# Features

* Embed **static** files
* Embed **command execution** results
* **Idempotent** substitutions
* **Invisible** non-intrusive markup using comment blocks
* **Plays nicely** with other markups
* **Extensible** with project-local commands
* **Configurable** with config files and env vars


# Use cases

* Manage partially duplicate docs for multiple destinations
* Manage docs for monorepositories
* Embed CLI reference in docs
* Embed dynamically generated content:
  * Project metadata
  * Test reports
  * Models evaluation results

> [!NOTE]
> This file uses docsub itself. Dig into raw markup if interested.

## Docsub is not...

* ...a documentation engine like [Sphinx](https://www.sphinx-doc.org) or [MkDocs](https://www.mkdocs.org)
* ...a full-featured static website generator like [Pelican](https://getpelican.com)
* ...a templating engine like [Jinja](https://jinja.palletsprojects.com)
* ...a replacement for [Bump My Version](https://callowayproject.github.io/bump-my-version)

# Usage

```shell
$ uv run docsub apply -i README.md
```

## From separate files...

<table>
<tr>
<td style="vertical-align:top">

### README.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme_showcase/__input__.md -->
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
<!-- docsub: include tests/test_readme_showcase/info.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
> Long description.
````
<!-- docsub: end #readme -->

### features.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme_showcase/features.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
* Feature 1
* Feature 2
* Feature 3
````
<!-- docsub: end #readme -->

### data.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme_showcase/data.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
| Key 1 | value 1 |
| Key 2 | value 2 |
| Key 3 | value 3 |
````
<!-- docsub: end #readme -->

### func.py
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme_showcase/func.py -->
<!-- docsub: lines after 1 upto -1 -->
````python
def func():
    pass
````
<!-- docsub: end #readme -->

</td>
</tr>
</table>


## Get merged document

***and keep it updated!***

<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme_showcase/__result__.md -->
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


# Installation

## Development dependency

Recommended. The most flexible installation option, allowing [project-local commands](#project-local-commands) to utilize project codebase.

```toml
# pyproject.toml
[dependency-groups]
dev = [
  "docsub==0.8.2",
]
```

## Global installation

Works for simple cases.

```shell
uv tool install docsub==0.8.2
```


# Syntax

The syntax is purposefully verbose. This is fine, you are not supposed to edit it often. But it's searchable and sticks in eye when scrolling down large documents.

Docsub uses line-based substitution syntax based on *directives* and *substitution blocks*.

## Markdown

### Directive

*Markdown directive* is one-line comment:

```text
<!-- docsub: <directive> [directive args] -->
```

There are multiple [directive types](#directives).

### Substitution block

*Markdown substitution block* is a sequence of lines, starting with `begin` directive and ending with `end` directive.

```markdown
<!-- docsub: begin -->
<!-- docsub: help docsub -->
<!-- docsub: include CHANGELOG.md -->
Inner text will be replaced.
<!-- docsub: this whole line is treated as plain text -->
This text will be replaced too.
<!-- docsub: end -->
```

One or many other directives must come at the top of the block, otherwise they are treated as plain text. Blocks without *producing directives* are not allowed. Block's inner text will be replaced upon substitution, unless modifier directives are used, e.g. `lines`.

If docsub substitution block lies inside markdown fenced code block, it is not substituted *(example: fenced code blocks above and below this paragraph, see the raw markup)*. To put dynamic content into a fenced code block, place `begin` and `end` around it and use `lines after N upto -M` *(example: [Usage](#usage) section)*.

For nested blocks, only top level substitution is performed. Use block `#identifier` to distinguish between nesting levels.

```markdown
<!-- docsub: begin #top -->
<!-- docsub: include part.md -->
<!-- docsub: begin -->
<!-- docsub: include nested.md -->
<!-- docsub: end -->
<!-- docsub: end #top -->
```

When substitution block is indented, the indentation is preserved:

<!-- docsub: begin #top -->
<!-- docsub: include tests/test_readme_indent/__result__.md -->
<!-- docsub: lines after 1 upto -1 -->
```markdown
* List item
    <!-- docsub: begin -->
    <!-- docsub: include sublist.md -->
    * Sub-item 1
    * Sub-item 2
    * Sub-item 3
    <!-- docsub: end -->
```
<!-- docsub: end #top -->

# Directives

* *Block delimiters*: `begin`, `end`
* *Producing commands*: `exec`, `help`, `include`, `x`
* *Modifying commands*: `lines`, `strip`

## `begin`
```text
begin [#identifier]
```
Open substitution target block. To distinguish between nesting levels, use block `#identifier`, starting with `#`.

## `end`
```text
end [#identifier]
```
Close substitution target block.

## `exec`
```text
exec <shell commands>
```
Execute `<shell commands>` with `sh -c` and substitute stdout. Allows pipes and other shell functionality. If possible, avoid using this directive.

* `cmd.exec.work_dir` — shell working directory, default `'.'`
* `cmd.exec.env_vars` — dict of additional environment variables, default `{}`

## `help`

```text
help <command> [subcommand...]
help python -m <command> [subcommand...]
```
Display help for CLI utility or Python module. Use this command to document CLI instead of `exec`. Runs `command [subcommand...] --help` or `python -m command [subcommand...] --help` respectively. *Directive args* must be a space-separated sequence of characters `[-._a-zA-Z0-9]`.

* `cmd.help.env_vars` — dict of additional environment variables, default `{}`

## `include`
```text
include path/to/file
```
Literally include file specified by path relative to `base_dir` config option.

* `cmd.include.base_dir` — base directory for relative paths

## `lines`
```text
lines [after N] [upto -M]
```
Upon substitution, keep original target block lines: first `N` and/or last `M`. Only one `lines` command is allowed inside the block.

## `strip`
```text
strip
```
Strip whitespace in substitution result:
* initial and trailing blank lines
* trailing whitespace on every line

## `x`
```text
x <project-command> [args and --options]
```
Execute [project-local](#project-local-commands) command declared in `docsubfile.py` in project root. The naming is inspired by `X-` HTTP headers and `x-` convention for reusable YAML sections.

* `cmd.x.docsubfile` — path to file with project-local commands, absolute or relative to project root (default: `docsubfile.py`)


# Project-local commands

When project root contains file `docsubfile.py` with commands defined as in example below, they can be used in `docsub: x ` directive. Project commands must be defined as [click](https://click.palletsprojects.com) command and gathered under `x` group. There is no need to install `click` separately as docsub depends on it.

If docsub is installed globally and called as `uvx docsub`, project commands in `docsubfile.py` have access to docsub dependencies only: `click`, `loguru`, `rich` (see docsub's pyproject.toml for details).

If docsub is installed as project dev dependency and called as `uv run docsub`, user commands also have access to project modules and dev dependencies. This allows more flexible scenarios.

Project command author can get access to docsub `Environment` object (including command configs) from click context object (see example below). The docsub `Environment` object has some useful methods *(not documented yet)*.

## Example

```shell
$ uv run docsub apply -i sample.md
```

### sample.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme_docsubfile/__result__.md -->
<!-- docsub: lines after 1 upto -1 -->
```markdown
<!-- docsub: begin -->
<!-- docsub: x say-hello Alice Bob -->
Hi there, Alice!
Hi there, Bob!
<!-- docsub: end -->
```
<!-- docsub: end #readme -->

### docsubfile.py
<!-- docsub: begin -->
<!-- docsub: include tests/test_readme_docsubfile/docsubfile.py -->
<!-- docsub: lines after 1 upto -1 -->
```python
from docsub import Environment, click, pass_env

@click.group()
def x() -> None:
    pass

@x.command()
@click.argument('users', nargs=-1)
def say_hello(users: tuple[str, ...]) -> None:
    for user in users:
        click.echo(f'Hi there, {user}!')

@x.command()
@click.argument('users', nargs=-1)
@pass_env
def log_hello(env: Environment, users: tuple[str, ...]) -> None:
    base = env.get_temp_dir('log_hello')
    (base / 'hello.log').write_text(f'said hello to {users}')
```
<!-- docsub: end -->

## Calling project-local commands

Docsub exposes `x` as CLI command, letting project commands to be executed with project settings:

<!-- docsub: begin -->
<!-- docsub: exec uv run docsub -x tests/test_readme_docsubfile/docsubfile.py x say-hello Alice Bob -->
<!-- docsub: lines after 2 upto -1 -->
```shell
$ uv run docsub x say-hello Alice Bob
Hi there, Alice!
Hi there, Bob!
```
<!-- docsub: end -->


# Configuration

Configuration resolution order

* command line options *(to be documented)*
* environment variables *(to be documented)*
* `docsub.toml` config file in current working directory
* `pyproject.toml`, section `[tool.docsub]` *(to be implemented)*
* default config values

## Root settings

* `local_dir` — internal working directory at the project root (default: `.docsub`)

## Command settings

See [Commands](#commands).

## Environment variables

*(to be documented)*

## Command line options

*(to be documented)*

## Complete config example

All config keys are optional.


```toml
local_dir = ".docsub"  # default

[logging]
#level = "DEBUG"  # default: missing, logging disabled

[cmd.exec]
env_vars = {}  # default
work_dir = "."  # default

[cmd.help.env_vars]
COLUMNS = "60"  # more compact

[cmd.include]
base_dir = "."  # default

[cmd.x]
docsubfile = "docsubfile.py"  # default
```

> [!WARNING]
> In future releases config keys will be moved under `[tool.docsub]` root for both `pyproject.toml` and `docsub.toml`, this will be a breaking change.


# Logging

Docsub uses [loguru](https://loguru.readthedocs.io) for logging. Logging is disabled by default. To enable logging, set config option `level` to one of [logging levels](https://loguru.readthedocs.io/en/stable/api/logger.html#levels) supported by loguru.

*(logging is rudimentary at the moment)*


# CLI Reference

<!-- docsub: begin -->
<!-- docsub: help python -m docsub -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ docsub --help
Usage: python -m docsub [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────╮
│ --config-file           -c  PATH                                   │
│ --local-dir             -l  PATH                                   │
│ --cmd-exec-work-dir         PATH                                   │
│ --cmd-exec-env-vars         TEXT                                   │
│ --cmd-help-env-vars         TEXT                                   │
│ --cmd-include-base-dir      PATH                                   │
│ --cmd-x-docsubfile      -x  PATH                                   │
│ --version                         Show the version and exit.       │
│ --help                            Show this message and exit.      │
╰────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────╮
│ apply    Update Markdown files with embedded content.              │
│ x        Project-local commands.                                   │
╰────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## `docsub apply`

<!-- docsub: begin -->
<!-- docsub: help python -m docsub apply -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ docsub apply --help
Usage: python -m docsub apply [OPTIONS] FILES...

Update Markdown files with embedded content.
Read FILES and perform substitutions one by one. If one file depends
on another, place it after that file.

╭─ Options ──────────────────────────────────────────────────────────╮
│ --in-place  -i    Process files in-place                           │
│ --help            Show this message and exit.                      │
╰────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## `docsub x`

<!-- docsub: begin -->
<!-- docsub: help python -m docsub x -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ docsub x --help
Usage: python -m docsub x [OPTIONS] COMMAND [ARGS]...

Project-local commands.

╭─ Options ──────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                            │
╰────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->


# History

This project appeared to maintain docs for [multipython](https://github.com/makukha/multipython) project. You may check it up for usage examples.


# Authors

* [Michael Makukha](https://github.com/makukha)


# License

[MIT License](https://github.com/makukha/docsub/blob/main/LICENSE)


# Changelog

[CHANGELOG.md](https://github.com/makukha/docsub/blob/main/CHANGELOG.md)
