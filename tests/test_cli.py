import pytest

from gitignore.cli import Options, parse_args


def test_parse_args_defaults():
    opts = parse_args([])
    assert opts == Options(
        list_types=False,
        list_file=False,
        replace=False,
        edit=False,
        verbose=False,
        filetype=None,
    )


def test_parse_args_with_filetype_and_flags():
    opts = parse_args(["py", "-t", "-l", "-r", "-v", "-e"])
    assert opts.filetype == "py"
    assert opts.list_types is True
    assert opts.list_file is True
    assert opts.replace is True
    assert opts.verbose is True
    assert opts.edit is True
