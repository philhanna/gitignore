import subprocess
import sys
from pathlib import Path

from .cli import Options
from .config import Config

GITIGNORE_FILE = ".gitignore"


class Gitignore:
    """Main application class for generating and managing .gitignore files.

    Combines editor-level defaults with per-filetype patterns from the
    configuration and dispatches to subcommands based on parsed CLI options.
    """

    def __init__(self, options: Options, config: Config):
        """Initialise the application with parsed options and loaded config.

        Args:
            options: Parsed command-line options controlling which actions to perform.
            config: Loaded configuration containing editor and filetype pattern data.
        """
        self.options = options
        self.config = config

    def run(self) -> None:
        """Execute the appropriate subcommand(s) based on the parsed options.

        Handles the following actions in order:
        - List available filetypes if ``--list-types`` was requested.
        - Print the current .gitignore contents if ``--list-file`` was requested.
        - Create a new .gitignore (unless ``--list-types`` was given); optionally
          print the result (``--verbose``) and open it in the configured editor
          (``--edit``).
        """
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
        """Write a new .gitignore file in the current directory.

        Writes filetype-specific patterns from the config when a filetype was
        specified on the command line.

        Exits with status 1 if the file already exists and ``--replace`` was
        not given.
        """
        path = Path(GITIGNORE_FILE)
        if path.exists() and not self.options.replace:
            print(f"{GITIGNORE_FILE} already exists; use -r to replace", file=sys.stderr)
            sys.exit(1)
        lines = []
        if self.options.filetype:
            lines.extend(self.config.file_types.get(self.options.filetype, []))
        path.write_text("\n".join(lines) + "\n")

    def edit_file(self) -> None:
        """Open the .gitignore file in the editor specified by the config."""
        subprocess.run([self.config.editor, GITIGNORE_FILE])

    def list_file(self) -> None:
        """Print the contents of the .gitignore file to stdout.

        Does nothing if the file does not exist.
        """
        path = Path(GITIGNORE_FILE)
        if path.exists():
            print(path.read_text(), end="")

    def list_types(self) -> None:
        """Print all available filetype names and their pattern counts to stdout.

        Output is sorted alphabetically and aligned so pattern counts are
        visually grouped.  Example::

            go    (2 entries)
            java  (5 entries)
            py    (8 entries)
        """
        max_len = max(len(k) for k in self.config.file_types)
        for name in sorted(self.config.file_types):
            entries = self.config.file_types[name]
            print(f"{name.ljust(max_len)}  ({len(entries)} entries)")
