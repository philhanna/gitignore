# tests.test_app
import pytest

from gitignore.app import DEFAULT_PATTERNS, GITIGNORE_FILE, Gitignore
from gitignore.cli import Options


def make_options(**kwargs):
    defaults = dict(
        list_types=False,
        list_file=False,
        replace=False,
        edit=False,
        verbose=False,
        filetype=None,
    )
    defaults.update(kwargs)
    return Options(**defaults)


def test_create_new_file(tmp_path, sample_config):
    (tmp_path / GITIGNORE_FILE).unlink(missing_ok=True)
    app = Gitignore(make_options(), sample_config)
    import os
    os.chdir(tmp_path)
    app.create()
    content = (tmp_path / GITIGNORE_FILE).read_text()
    for pattern in DEFAULT_PATTERNS:
        assert pattern in content


def test_create_with_filetype(tmp_path, sample_config):
    import os
    os.chdir(tmp_path)
    app = Gitignore(make_options(filetype="py"), sample_config)
    app.create()
    content = (tmp_path / GITIGNORE_FILE).read_text()
    assert "*.pyc" in content
    assert "__pycache__" in content


def test_create_refuses_if_exists(tmp_path, sample_config):
    import os
    os.chdir(tmp_path)
    (tmp_path / GITIGNORE_FILE).write_text("existing\n")
    app = Gitignore(make_options(), sample_config)
    with pytest.raises(SystemExit):
        app.create()


def test_create_replaces_if_flag_set(tmp_path, sample_config):
    import os
    os.chdir(tmp_path)
    (tmp_path / GITIGNORE_FILE).write_text("old content\n")
    app = Gitignore(make_options(replace=True), sample_config)
    app.create()
    content = (tmp_path / GITIGNORE_FILE).read_text()
    assert "old content" not in content
    assert "*.swp" in content


def test_list_types_output(capsys, sample_config):
    app = Gitignore(make_options(), sample_config)
    app.list_types()
    out = capsys.readouterr().out
    assert "go" in out
    assert "py" in out
    assert "java" in out


def test_list_file_output(tmp_path, capsys, sample_config):
    import os
    os.chdir(tmp_path)
    (tmp_path / GITIGNORE_FILE).write_text("*.swp\n*.pyc\n")
    app = Gitignore(make_options(), sample_config)
    app.list_file()
    out = capsys.readouterr().out
    assert "*.swp" in out
    assert "*.pyc" in out
