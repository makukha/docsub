# docsub
> Update documentation files from external content.

# Features

* Markdown files:
  * Fenced code blocks
* Readable shell-like rule syntax
* Idempotent

# Installation

```shell
uv tool install docsub
```

# Basic usage

This file itself uses docsub to substitute examples from test folder!

## Given README.md

<!-- docsub: cat tests/test_readme/README.md -->
````markdown
# Title

<!-- docsub: cat hello.txt -->
```
```

<!-- docsub: cat hello.py -->
```python
# existing text will be replaced
```
````

### hello.txt

<!-- docsub: cat tests/test_readme/hello.txt -->
```text
Hello world!
```

### hello.py

<!-- docsub: cat tests/test_readme/hello.py -->
```python
def hello():
    print('Hi!')
```

## Get updated README.md

```shell
$ uvx docsub -i README.md
```

<!-- docsub: cat tests/test_readme/RESULT.md -->
````markdown
# Title

<!-- docsub: cat hello.txt -->
```
Hello world!
```

<!-- docsub: cat hello.py -->
```python
def hello():
    print('Hi!')
```
````

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
