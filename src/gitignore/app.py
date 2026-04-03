import subprocess
import sys
from pathlib import Path

from .cli import Options
from .config import Config

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
            lines.extend(self.config.file_types.get(self.options.filetype, []))
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
