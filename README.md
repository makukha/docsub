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

````markdown @docsub: cat tests/test_readme/README.md
# Title

```@docsub: cat hello.txt
```

```python @docsub: cat hello.py
existing text is replaced
```
````

### hello.txt

```text @docsub: cat tests/test_readme/hello.txt
Hello world!
```

### hello.py

```python @docsub: cat tests/test_readme/hello.py
def hello():
    print('Hi!')
```

## Get updated README.md

```shell
$ uvx docsub -i README.md
```

````markdown @docsub: cat tests/test_readme/RESULT.md
# Title

```@docsub: cat hello.txt
Hello world!
```

```python @docsub: cat hello.py
def hello():
    print('Hi!')
```
````

# CLI Reference

```text @docsub: help python -m docsub
                                                            
 Usage: python -m docsub [OPTIONS] [FILE]...                
                                                            
 Update documentation files with external content.          
                                                            
╭─ Options ────────────────────────────────────────────────╮
│ --in-place  -i    Overwrite source files.                │
│ --version         Show the version and exit.             │
│ --help            Show this message and exit.            │
╰──────────────────────────────────────────────────────────╯

```
