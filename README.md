# docsub
> Mutable Markdown docs made easy.

> [!WARNING]
> This project is on its very early stage, syntax and functionality may change significantly. Use specific package version: `docsub==0.4.0`


# Features

* Idempotent substitutions
* Rich set of commands (to be done)
* Plugin system (to be done)
* Supports Markdown

> [!NOTE]
> This file itself uses docsub to substitute example from `tests` folder. Inspect raw markup if interested.


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

### description.md
<!-- docsub: begin #readme -->
<!-- docsub: include tests/test_readme/description.md -->
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
<!-- docsub: command1 -->
<!-- docsub: commandN -->
Inner text will be replaced.
<!-- docsub: this whole line is treated as plain text -->
This text will be replaced too.
<!-- docsub: end -->
```

Each block starts with `begin` and ends with `end`. One or many commands come at the top of the block, otherwise they are treated as plain text. Blocks without *substitution commands* are not allowed. Block's inner text will be replaced upon substitution, unless modifier command `lines` is used.

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

* Target block delimiters: `begin`, `end`
* *Substitution commands*: `exec`, `help`, `include`
* *Modifier commands*: `lines`

## begin
```text
begin [#identifier]
```
Open substitution target block. To distinguish with nested blocks, use `#identifier` starting with `#`.

## end
```text
end [#identifier]
```
Close substitution target block.

## exec
```text
exec arbitrary commands
```
Execute `arbitrary commands` with `sh -c` and substitute stdout. Allows pipes and other shell functionality. If possible, avoid using this command.

## help

```text
help command [subcommand...]
help python -m command [subcommand...]
```
Display help for CLI utility or Python module. Use this command to document CLI instead of `exec`. Runs `command args --help` or `python -m command args --help` respectively. `command [subcommands...]` can only be a space-separated sequence of `[-._a-zA-Z0-9]` characters.

## include
```text
include path/to/file
```
Literally include file specified by path relative to `workdir` config option.

## lines
```text
lines [after N] [upto -M]
```
Upon substitution, keep original target block lines: first `N` and/or last `M`. Only one `lines` command is allowed inside the block.


# CLI Reference

<!-- docsub after line 1: help python -m docsub -->
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


# Changelog

Check repository [CHANGELOG.md](https://github.com/makukha/multipython/tree/main/CHANGELOG.md)
