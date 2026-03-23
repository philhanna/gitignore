# Plan: Convert gitignore from Go to Python

## Overview

Convert the `gitignore` CLI tool from Go to Python, preserving all existing
functionality. The Go project has three logical units — options, config, and
application logic — which map cleanly to Python modules.

---

## Target Directory Structure

```
gitignore/
├── docs/
│   └── plans/
│       └── fromGo.md
├── src/
│   └── gitignore/
│       ├── __init__.py          # gitignore
│       ├── __main__.py          # Entry point: python -m gitignore
│       ├── cli.py               # Argument parsing (replaces options.go + cmd/gitignore.go)
│       ├── config.py            # Config loading (replaces config.go)
│       └── app.py               # Application logic (replaces gitignore.go)
├── tests/
│   ├── __init__.py              # tests
│   ├── conftest.py              # Shared fixtures
│   ├── test_config.py           # Replaces config_test.go
│   └── test_app.py              # Replaces logic from gitignore.go
├── testdata/
│   ├── empty                    # Keep as-is
│   └── regular.txt              # Keep as-is
├── config.yaml                  # Keep as-is (sample/default config)
├── pyproject.toml               # Replaces go.mod
└── README.md                    # Update for Python
```

---

## Module Mapping: Go → Python

| Go file              | Python file                          | Notes                                      |
|----------------------|--------------------------------------|--------------------------------------------|
| `options.go`         | `src/gitignore/cli.py`               | `argparse` instead of `flag`               |
| `cmd/gitignore.go`   | `src/gitignore/__main__.py` + `cli.py` | Entry point + flag wiring                |
| `config.go`          | `src/gitignore/config.py`            | `PyYAML` + `platformdirs`                  |
| `gitignore.go`       | `src/gitignore/app.py`               | Core logic unchanged in structure          |
| `config_test.go`     | `tests/test_config.py`               | pytest                                     |
| *(new)*              | `tests/test_app.py`                  | Tests for `app.py` logic                   |

---

## Step-by-Step Implementation Plan

### Step 1 — Project scaffolding

Create the `src/gitignore/` and `tests/` directories with empty `__init__.py`
files (each with the correct dotted-package comment per project conventions).

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "gitignore"
version = "1.3.0"
description = "Creates a basic .gitignore file in the current directory"
requires-python = ">=3.11"
dependencies = [
    "platformdirs",
    "PyYAML",
]

[project.scripts]
gitignore = "gitignore.__main__:main"

[tool.setuptools.packages.find]
where = ["src"]
```

---

### Step 2 — `config.py` (replaces `config.go`)

**Responsibilities:** load YAML config from the user's config directory, or
fall back to the bundled `config.yaml`.

**Key decisions:**
- Use `platformdirs.user_config_dir("gitignore")` to find the platform-correct
  config directory (replaces the manual `$HOME/.config` / `AppData` logic).
- Embed the default config via `importlib.resources` (replaces Go's
  `//go:embed`).
- Return a `Config` dataclass with fields `editor: str` and
  `file_types: dict[str, list[str]]`.

```python
# src/gitignore/config.py
from dataclasses import dataclass
from pathlib import Path
import importlib.resources
import platformdirs
import yaml

CONFIG_FILENAME = "config.yaml"

@dataclass
class Config:
    editor: str
    file_types: dict[str, list[str]]

def load_config() -> tuple[Config, bool]:
    """Return (Config, is_local). is_local=True when a user config was found."""
    config_path = Path(platformdirs.user_config_dir("gitignore")) / CONFIG_FILENAME
    if config_path.exists():
        data = config_path.read_text()
        is_local = True
    else:
        data = importlib.resources.files("gitignore").joinpath(CONFIG_FILENAME).read_text()
        is_local = False
    raw = yaml.safe_load(data)
    return Config(editor=raw["editor"], file_types=raw["filetypes"]), is_local
```

The bundled `config.yaml` should be moved into `src/gitignore/config.yaml` so
`importlib.resources` can locate it, and declared as package data in
`pyproject.toml`:

```toml
[tool.setuptools.package-data]
gitignore = ["config.yaml"]
```

---

### Step 3 — `cli.py` (replaces `options.go` + `cmd/gitignore.go`)

**Responsibilities:** define and parse command-line arguments.

```python
# src/gitignore/cli.py
import argparse
from dataclasses import dataclass

@dataclass
class Options:
    list_types: bool
    list_file: bool
    replace: bool
    edit: bool
    verbose: bool
    filetype: str | None

def parse_args(argv=None) -> Options:
    parser = argparse.ArgumentParser(
        prog="gitignore",
        description="Creates a basic .gitignore file in the current directory",
    )
    parser.add_argument("filetype", nargs="?", help="Type of files (e.g. go, java, py)")
    parser.add_argument("-t", "--types",   dest="list_types", action="store_true", help="List supported file types")
    parser.add_argument("-l", "--list",    dest="list_file",  action="store_true", help="List the current .gitignore")
    parser.add_argument("-r", "--replace", dest="replace",    action="store_true", help="Replace existing .gitignore")
    parser.add_argument("-v", "--verbose", dest="verbose",    action="store_true", help="Verbose output")
    parser.add_argument("-e", "--edit",    dest="edit",       action="store_true", help="Edit file when done")
    ns = parser.parse_args(argv)
    return Options(
        list_types=ns.list_types,
        list_file=ns.list_file,
        replace=ns.replace,
        edit=ns.edit,
        verbose=ns.verbose,
        filetype=ns.filetype,
    )
```

---

### Step 4 — `app.py` (replaces `gitignore.go`)

**Responsibilities:** orchestrate the tool's behaviour given parsed options and
loaded config.

```python
# src/gitignore/app.py
import subprocess
import sys
from pathlib import Path
from .config import Config
from .cli import Options

GITIGNORE_FILE = ".gitignore"
DEFAULT_PATTERNS = ["*.swp"]

class Gitignore:
    def __init__(self, options: Options, config: Config):
        self.options = options
        self.config = config

    def run(self) -> None:
        if self.options.list_types:
            self.list_types()
        if self.options.list_file:
            self.list_file()
        if not self.options.list_types:
            self.create()
            if self.options.verbose:
                self.list_file()
            if self.options.edit:
                self.edit_file()

    def create(self) -> None:
        path = Path(GITIGNORE_FILE)
        if path.exists() and not self.options.replace:
            print(f"{GITIGNORE_FILE} already exists; use -r to replace", file=sys.stderr)
            sys.exit(1)
        lines = list(DEFAULT_PATTERNS)
        if self.options.filetype:
            ft_lines = self.config.file_types.get(self.options.filetype, [])
            lines.extend(ft_lines)
        path.write_text("\n".join(lines) + "\n")

    def edit_file(self) -> None:
        subprocess.run([self.config.editor, GITIGNORE_FILE])

    def list_file(self) -> None:
        path = Path(GITIGNORE_FILE)
        if path.exists():
            print(path.read_text(), end="")

    def list_types(self) -> None:
        max_len = max(len(k) for k in self.config.file_types)
        for name in sorted(self.config.file_types):
            entries = self.config.file_types[name]
            print(f"{name.ljust(max_len)}  ({len(entries)} entries)")
```

---

### Step 5 — `__main__.py` (entry point)

```python
# src/gitignore/__main__.py
import sys
from .cli import parse_args
from .config import load_config
from .app import Gitignore

def main() -> None:
    options = parse_args()
    config, _ = load_config()
    app = Gitignore(options, config)
    app.run()

if __name__ == "__main__":
    main()
```

---

### Step 6 — Tests

**`tests/test_config.py`** (mirrors `config_test.go`):
- `test_load_config_returns_config` — verify editor and file_types are populated
- `test_load_config_is_local_false` — when no user config exists, `is_local` is False
- `test_load_config_is_local_true` — when a user config exists, `is_local` is True
  (use `tmp_path` + monkeypatch `platformdirs.user_config_dir`)

**`tests/test_app.py`**:
- `test_create_new_file` — creates `.gitignore` with defaults when no filetype given
- `test_create_with_filetype` — includes filetype patterns
- `test_create_refuses_if_exists` — exits if file exists and `--replace` not set
- `test_create_replaces_if_flag_set` — replaces file when `--replace` set
- `test_list_types_output` — captures stdout, checks sorted type names appear
- `test_list_file_output` — captures stdout of `list_file()`

All tests use `tmp_path` for filesystem isolation and `capsys` for output
capture.

---

### Step 7 — Remove Go artefacts

Once the Python implementation is complete and all tests pass:

- Delete: `go.mod`, `go.sum`, `build_binaries.sh`, `cmd/`, `bin/`
- Delete Go source files: `options.go`, `config.go`, `gitignore.go`,
  `config_test.go`
- Move `config.yaml` into `src/gitignore/config.yaml`
- Update `README.md` for Python installation (`pip install .` or `pipx install .`)

---

## Dependency Summary

| Dependency      | Purpose                                     | Go equivalent            |
|-----------------|---------------------------------------------|--------------------------|
| `PyYAML`        | Parse YAML config                           | `github.com/ghodss/yaml` |
| `platformdirs`  | Cross-platform config directory             | Manual `os` detection    |
| `pytest`        | Test runner                                 | `testing` + `testify`    |

No third-party dependency is needed for argument parsing (`argparse` is stdlib),
subprocess execution (`subprocess` is stdlib), or file I/O (`pathlib` is stdlib).
