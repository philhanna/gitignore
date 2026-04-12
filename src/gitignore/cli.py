"""Command-line argument parsing for the gitignore tool.

Defines the :class:`Options` dataclass that carries parsed flags and the
:func:`parse_args` factory that populates it from ``sys.argv`` (or a
caller-supplied list, useful for testing).
"""

import argparse
from dataclasses import dataclass


@dataclass
class Options:
    """Parsed command-line options for a single invocation.

    Attributes:
        list_types: ``True`` when ``-t``/``--types`` was passed; print all
                    supported filetypes and skip file creation.
        list_file:  ``True`` when ``-l``/``--list`` was passed; print the
                    current ``.gitignore`` contents.
        replace:    ``True`` when ``-r``/``--replace`` was passed; overwrite
                    an existing ``.gitignore`` without prompting.
        edit:       ``True`` when ``-e``/``--edit`` was passed; open the file
                    in the configured editor after writing it.
        verbose:    ``True`` when ``-v``/``--verbose`` was passed; print the
                    file contents after creation (equivalent to ``--list``).
        filetype:   Optional positional argument naming the language/toolchain
                    whose patterns should be included (e.g. ``"py"``, ``"go"``).
                    ``None`` when omitted.
    """

    list_types: bool
    list_file: bool
    replace: bool
    edit: bool
    verbose: bool
    filetype: str | None


def parse_args(argv=None) -> Options:
    """Parse command-line arguments and return an :class:`Options` instance.

    Args:
        argv: Argument list to parse.  Defaults to ``None``, which causes
              :mod:`argparse` to read from ``sys.argv[1:]``.  Pass an explicit
              list (e.g. ``["py", "-v"]``) for testing.

    Returns:
        Populated :class:`Options` dataclass.
    """
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
    # Unpack the Namespace into our typed dataclass so callers never need to
    # import argparse or deal with attribute-access on a plain Namespace.
    return Options(
        list_types=ns.list_types,
        list_file=ns.list_file,
        replace=ns.replace,
        edit=ns.edit,
        verbose=ns.verbose,
        filetype=ns.filetype,
    )
