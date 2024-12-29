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
````

### hello.txt

<!-- docsub: cat tests/test_readme/hello.txt -->
```text
```

### hello.py

<!-- docsub: cat tests/test_readme/hello.py -->
```python
```

## Get updated README.md

```shell
$ uvx docsub -i README.md
```

<!-- docsub: cat tests/test_readme/RESULT.md -->
````markdown
````

# CLI Reference

<!-- docsub: help python -m docsub -->
```text
```
