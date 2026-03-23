# tests.test_config
from pathlib import Path

import pytest
import yaml

from gitignore.config import CONFIG_FILENAME, Config, load_config


def test_load_config_returns_config():
    config, _ = load_config()
    assert isinstance(config, Config)
    assert config.editor
    assert config.file_types


def test_load_config_is_local_false(monkeypatch):
    monkeypatch.setattr("platformdirs.user_config_dir", lambda _: "/nonexistent/path")
    _, is_local = load_config()
    assert is_local is False


def test_load_config_is_local_true(monkeypatch, tmp_path):
    config_dir = tmp_path / "gitignore"
    config_dir.mkdir()
    config_file = config_dir / CONFIG_FILENAME
    config_file.write_text(
        yaml.dump({"editor": "nano", "filetypes": {"py": ["*.pyc"]}})
    )
    monkeypatch.setattr("platformdirs.user_config_dir", lambda _: str(config_dir))
    config, is_local = load_config()
    assert is_local is True
    assert config.editor == "nano"
    assert config.file_types == {"py": ["*.pyc"]}
