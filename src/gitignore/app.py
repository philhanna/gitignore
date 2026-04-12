"""Core application logic for the gitignore tool.

Provides the :class:`Gitignore` class that orchestrates file creation,
listing, and editing based on parsed CLI options and loaded configuration.
"""

import subprocess
import sys
from pathlib import Path

from .cli import Options
from .config import Config

GITIGNORE_FILE = ".gitignore"
# Patterns written to every new .gitignore regardless of filetype selection.
DEFAULT_PATTERNS = ["*.swp"]


class Gitignore:
    """Orchestrates .gitignore file creation and management.

    Combines user-supplied :class:`~gitignore.cli.Options` with the loaded
    :class:`~gitignore.config.Config` to create, display, or edit a
    ``.gitignore`` file in the current working directory.
    """

    def __init__(self, options: Options, config: Config):
        """Initialise with parsed CLI options and loaded configuration.

        Args:
            options: Flags and positional arguments from the command line.
            config:  Editor preference and filetype pattern mappings loaded
                     from the YAML config file.
        """
        self.options = options
        self.config = config

    def run(self) -> None:
        """Dispatch to sub-operations according to the active options.

        The precedence rules are:
        * ``--types`` lists supported filetypes and **skips** file creation.
        * ``--list`` prints the current ``.gitignore`` and can coexist with
          either the types listing or file creation.
        * When no ``--types`` flag is present, a new ``.gitignore`` is always
          created (subject to the ``--replace`` guard in :meth:`create`).
        * ``--verbose`` after creation is equivalent to ``--list``.
        * ``--edit`` opens the file in the configured editor after creation.
        """
        if self.options.list_types:
            self.list_types()
        if self.options.list_file:
            self.list_file()
        # --types is the only flag that suppresses file creation; --list alone
        # still proceeds to create/overwrite the file.
        if not self.options.list_types:
            self.create()
            if self.options.verbose:
                self.list_file()
            if self.options.edit:
                self.edit_file()

    def create(self) -> None:
        """Write a new ``.gitignore`` to the current directory.

        Starts with :data:`DEFAULT_PATTERNS` and, if the user specified a
        filetype, appends the corresponding patterns from the config.  Exits
        with an error message if the file already exists and ``--replace``
        was not supplied.

        Raises:
            SystemExit: When ``.gitignore`` already exists and ``options.replace``
                        is ``False``.
        """
        path = Path(GITIGNORE_FILE)
        if path.exists() and not self.options.replace:
            print(f"{GITIGNORE_FILE} already exists; use -r to replace", file=sys.stderr)
            sys.exit(1)
        # Copy DEFAULT_PATTERNS into a new list so the module-level constant
        # is never mutated across repeated calls (e.g. in tests).
        lines = list(DEFAULT_PATTERNS)
        if self.options.filetype:
            # Silently produce an empty filetype section for unknown keys rather
            # than crashing, so callers can still get a bare .gitignore.
            lines.extend(self.config.file_types.get(self.options.filetype, []))
        path.write_text("\n".join(lines) + "\n")

    def edit_file(self) -> None:
        """Open ``.gitignore`` in the configured editor.

        Blocks until the editor process exits.  The editor command is taken
        from :attr:`~gitignore.config.Config.editor` (e.g. ``"vim"``).
        """
        subprocess.run([self.config.editor, GITIGNORE_FILE])

    def list_file(self) -> None:
        """Print the contents of the current ``.gitignore`` to stdout.

        Does nothing if the file does not exist, so this method is safe to
        call unconditionally (e.g. for ``--verbose`` output after creation).
        """
        path = Path(GITIGNORE_FILE)
        if path.exists():
            # end="" avoids adding an extra blank line because the file itself
            # already ends with a newline written by create().
            print(path.read_text(), end="")

    def list_types(self) -> None:
        """Print all configured filetypes with their pattern counts.

        Output is alphabetically sorted and columnar — the filetype name is
        left-justified to the width of the longest name for readability.

        Example output::

            go    (5 entries)
            java  (8 entries)
            py    (6 entries)
        """
        # Pre-compute column width once rather than recalculating per row.
        max_len = max(len(k) for k in self.config.file_types)
        for name in sorted(self.config.file_types):
            entries = self.config.file_types[name]
            print(f"{name.ljust(max_len)}  ({len(entries)} entries)")
