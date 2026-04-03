from dataclasses import dataclass
from pathlib import Path

import importlib.resources
import platformdirs
import yaml

CONFIG_FILENAME = "config.yaml"


@dataclass
class Config:
    """Application configuration loaded from a YAML file.

    Attributes:
        editor: Name or path of the editor binary used to open .gitignore
            (e.g. ``"vim"``).
        file_types: Mapping from filetype key (e.g. ``"py"``, ``"go"``) to the
            list of glob patterns that should be written for that filetype.
    """

    editor: str
    file_types: dict[str, list[str]]


def load_config() -> tuple[Config, bool]:
    """Load and return the application configuration.

    Looks for a user-supplied config file at the platform-appropriate config
    directory (e.g. ``~/.config/gitignore/config.yaml`` on Linux).  Falls back
    to the bundled ``config.yaml`` shipped with the package when no user config
    is present.

    Returns:
        A two-tuple ``(config, is_local)`` where *config* is the parsed
        :class:`Config` and *is_local* is ``True`` when a user config file was
        found, ``False`` when the bundled default was used.
    """
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
