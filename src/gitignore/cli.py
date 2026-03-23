# gitignore.cli
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
