# gitignore.config
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
        data = (
            importlib.resources.files("gitignore")
            .joinpath(CONFIG_FILENAME)
            .read_text()
        )
        is_local = False
    raw = yaml.safe_load(data)
    return Config(editor=raw["editor"], file_types=raw["filetypes"]), is_local
