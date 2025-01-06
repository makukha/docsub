# docsub 🩻
> Mutable Markdown docs made easy.

> [!WARNING]
> This project is on its very early stage, syntax and functionality may change significantly. Even if not scared, use specific package version, e.g. `docsub==0.4.0`

> [!WARNING]
> With `docsub`, every documentation file becomes executable. Never use `docsub` to process files from untrusted sources.


# Features

* Short but powerful set of commands
* Idempotent substitutions
* Supports Markdown

> [!NOTE]
> This file itself uses docsub to substitute README examples from `tests` folder. Dig into raw markup if interested.


# Use cases

* Markdown docs with CLI usage examples
* Markdown docs with datasets rendered as tables
* Synchronized docs for multiple targets: GitHub README, PyPI README, documentation website.

# Non-use cases

* Not a replacement for [Bump My Version](https://callowayproject.github.io/bump-my-version)
* Not a full-featured documentation engine like [Sphinx](https://www.sphinx-doc.org)
* Not a full-featured templating language like [Jinja](https://jinja.palletsprojects.com).


# Installation

```shell
uv tool install docsub==0.4.0
```

# Basic usage

```shell
$ uvx docsub -i README.md
```

<table>
<tr>
<td style="vertical-align:top">

## Before

### README.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/README.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
````
<!-- docsub: end #readme -->

### info.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/info.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
````
<!-- docsub: end #readme -->

### features.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/features.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
````
<!-- docsub: end #readme -->

### data.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/data.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
````
<!-- docsub: end #readme -->

### func.py
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/func.py -->
<!-- docsub: lines after 1 upto -1 -->
````python
````
<!-- docsub: end #readme -->

</td>
<td style="vertical-align:top">

## After

### README.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/__result__.md -->
<!-- docsub: lines after 1 upto -1 -->
````markdown
````
<!-- docsub: end #readme -->

</td>
</tr>
</table>


# Substitution block

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


# Commands

* Block delimiters: `begin`, `end`
* *Producing commands*: `exec`, `help`, `include`
* *Modifying commands*: `lines`, `strip`

## `begin`
```text
begin [#identifier]
```
Open substitution target block. To distinguish with nested blocks, use `#identifier` starting with `#`.

## `end`
```text
end [#identifier]
```
Close substitution target block.

## `exec`
```text
exec arbitrary commands
```
Execute `arbitrary commands` with `sh -c` and substitute stdout. Allows pipes and other shell functionality. If possible, avoid using this command.

Config options:

* `workdir` — shell working directory, default `'.'`
* `env` — additional environment variables dict, default `{}`

## `help`

```text
help command [subcommand...]
help python -m command [subcommand...]
```
Display help for CLI utility or Python module. Use this command to document CLI instead of `exec`. Runs `command args --help` or `python -m command args --help` respectively. `command [subcommands...]` can only be a space-separated sequence of `[-._a-zA-Z0-9]` characters.

Config options:

* `env` — additional environment variables dict, default `{}`

## `include`
```text
include path/to/file
```
Literally include file specified by path relative to `workdir` config option.

Config options:

* `basedir` — base directory for relative paths

## `lines`
```text
lines [after N] [upto -M]
```
Upon substitution, keep original target block lines: first `N` and/or last `M`. Only one `lines` command is allowed inside the block.

## `strip`
```text
strip
```
Strip trailing whitespaces on every line of substitution result; strip initial and trailing blank lines of substitution result.


# Configuration

Configuration resolution order

* environment variables *(to be implemented)*
* `.docsub.toml` config file in current working directory
* `pyproject.toml`, section `[tool.docsub]` *(to be implemented)*
* default config values

### Structure

All config keys are optional.


```toml
[tool.docsub]

[command.exec]
env = {}  # default
workdir = "."  # default

[command.help]
env = { COLUMNS = "60" }

[command.include]
basedir = "."  # default
```

## Environment variables

*(to be implemented)*


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


# History

This project appeared to maintain docs for [multipython](https://github.com/makukha/multipython) project. You may check it up for usage examples.


# Authors

* [Michael Makukha](https://github.com/makukha)


# License

[MIT License](https://github.com/makukha/caseutil/blob/main/LICENSE)


# Changelog

Check repository [CHANGELOG.md](https://github.com/makukha/multipython/tree/main/CHANGELOG.md)
