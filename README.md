# docsub
> Update documentation files with external content.

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

## Give README.md

````markdown <- cat tests/test_readme/README.md
# Title

```<- cat hello.txt
```

```python <- cat hello.py
existing text is replaced
```
````

### hello.txt

```text <- cat tests/test_readme/hello.txt
Hello world!
```

### hello.py

```python <- cat tests/test_readme/hello.py
def hello():
    print('Hi!')
```

## Get updated README.md

```shell
$ uvx docsub -i README.md
```

````markdown <- cat tests/test_readme/RESULT.md
# Title

```<- cat hello.txt
Hello world!
```

```python <- cat hello.py
def hello():
    print('Hi!')
```
````

# CLI Reference

Yes, I eat my own dog food.

```text <- help python -m docsub
                                                            
 Usage: python -m docsub [OPTIONS] [FILE]...                
                                                            
 Update documentation files with external content.          
                                                            
╭─ Options ────────────────────────────────────────────────╮
│ --in-place  -i    Overwrite source files.                │
│ --version         Show the version and exit.             │
│ --help            Show this message and exit.            │
╰──────────────────────────────────────────────────────────╯

```
