# gitignore

## Overview

Creates a basic .gitignore file in the current directory, with
configurable sets of ignore lines for different file types in
the project.

## Usage
```
usage: gitignore [-h] [-t] [-l] [-r] [-v] [-e] [filetype]

Creates a basic .gitignore file in the current directory

positional arguments:
  filetype       Type of files (e.g. go, java, py)

options:
  -h, --help     Show this help message and exit
  -t, --types    List supported file types
  -l, --list     List the current .gitignore
  -r, --replace  Replace the current .gitignore, if it exists
  -v, --verbose  Provides more details
  -e, --edit     Edit the file when done

Rules are configured in config.yaml
```

## Installation

```
pipx install .
```

Or, into the current environment:

```
pip install .
```

## Configuration

The application uses a configurable `.yaml` file for file types
and the preferred text editor for the generated `.gitignore`.
There is a default config bundled with the application, but the user
can override it by creating a file named `config.yaml`
in a `gitignore` subdirectory of their configuration directory,
e.g.,
- `$HOME/.config/gitignore/config.yaml` on Unix
- `C:\Users\YourUser\AppData\Roaming\gitignore\config.yaml` on Windows

The configuration file must include entries for `editor` and `filetypes`.
The `filetypes` entry contains one or more file type names (such as
java, go, py, etc.)  For each of those names, there should be a list
of lines to be used in the generated `.gitignore` file.

Here is a sample:

```yaml
editor: vim
filetypes:
  java:
    - "*.swp"
    - build/
    - doc/
    - "*.class"
    - .classpath
    - .project
  go:
    - "*.swp"
  py:
    - "*.swp"
    - "*.pyc"
    - "*.pyo"
    - __pycache__
    - .idea/
    - venv/
    - build/
    - dist/
    - "*.egg-info/"
```

## References
- [Github repository](https://github.com/philhanna/gitignore)
- [.gitignore documentation](https://git-scm.com/docs/gitignore)
- [Wikipedia article on YAML](https://en.wikipedia.org/wiki/YAML)
- [YAML 1.2.0 specification](https://yaml.org/spec/1.2.0/)
