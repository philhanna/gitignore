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


def test_run_with_types_only(tmp_path, capsys, sample_config):
    import os

    os.chdir(tmp_path)
    app = Gitignore(make_options(list_types=True), sample_config)
    app.run()

    out = capsys.readouterr().out
    assert "go" in out
    assert "py" in out
    assert not (tmp_path / GITIGNORE_FILE).exists()


def test_run_with_list_file_prints_existing_file(tmp_path, capsys, sample_config):
    import os

    os.chdir(tmp_path)
    (tmp_path / GITIGNORE_FILE).write_text("existing\n")

    app = Gitignore(make_options(list_file=True, replace=True), sample_config)
    app.run()

    out = capsys.readouterr().out
    assert "existing" in out
    assert "*.swp" in (tmp_path / GITIGNORE_FILE).read_text()


def test_run_with_verbose_outputs_file(tmp_path, capsys, sample_config):
    import os

    os.chdir(tmp_path)
    app = Gitignore(make_options(verbose=True), sample_config)
    app.run()

    out = capsys.readouterr().out
    assert "*.swp" in out


def test_run_with_edit_calls_editor(monkeypatch, tmp_path, sample_config):
    import os

    os.chdir(tmp_path)
    called = {"edit": False}

    def fake_edit(self):
        called["edit"] = True

    monkeypatch.setattr(Gitignore, "edit_file", fake_edit)
    app = Gitignore(make_options(edit=True), sample_config)
    app.run()

    assert called["edit"] is True


def test_edit_file_invokes_subprocess(monkeypatch, tmp_path, sample_config):
    import os

    os.chdir(tmp_path)
    (tmp_path / GITIGNORE_FILE).write_text("existing\n")

    captured = {}

    def fake_run(cmd):
        captured["cmd"] = cmd

    monkeypatch.setattr("gitignore.app.subprocess.run", fake_run)
    app = Gitignore(make_options(), sample_config)
    app.edit_file()

    assert captured["cmd"] == ["vim", GITIGNORE_FILE]


def test_create_unknown_filetype_writes_default_only(tmp_path, sample_config):
    import os

    os.chdir(tmp_path)
    app = Gitignore(make_options(filetype="rust"), sample_config)
    app.create()

    assert (tmp_path / GITIGNORE_FILE).read_text() == "*.swp\n"


def test_list_file_no_file_prints_nothing(tmp_path, capsys, sample_config):
    import os

    os.chdir(tmp_path)
    app = Gitignore(make_options(), sample_config)
    app.list_file()

    assert capsys.readouterr().out == ""
