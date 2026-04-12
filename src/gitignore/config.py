"""Configuration loading for the gitignore tool.

Defines the :class:`Config` dataclass and the :func:`load_config` factory
that resolves configuration from the user's platform-specific config directory
or, as a fallback, from the package's bundled ``config.yaml``.
"""

from dataclasses import dataclass
from pathlib import Path

import importlib.resources
import platformdirs
import yaml

CONFIG_FILENAME = "config.yaml"


@dataclass
class Config:
    """Resolved runtime configuration.

    Attributes:
        editor:     Shell command used to open ``.gitignore`` for editing
                    (e.g. ``"vim"``, ``"nano"``).  Sourced from the ``editor``
                    key in the YAML config.
        file_types: Mapping from filetype name (e.g. ``"py"``) to the list of
                    glob patterns that should be appended to ``.gitignore``
                    when that type is requested.  Sourced from the
                    ``filetypes`` key in the YAML config.
    """

    editor: str
    file_types: dict[str, list[str]]


def load_config() -> tuple[Config, bool]:
    """Load configuration and return it together with a provenance flag.

    Resolution order:
    1. **User config** — ``<user_config_dir>/gitignore/config.yaml`` as
       determined by :func:`platformdirs.user_config_dir`.  On Linux this is
       typically ``~/.config/gitignore/config.yaml``.
    2. **Bundled default** — ``config.yaml`` shipped inside the
       ``gitignore`` package, accessed via :mod:`importlib.resources` so it
       works correctly from a wheel or zip import.

    Args:
        (none)

    Returns:
        A ``(Config, is_local)`` tuple where *is_local* is ``True`` when a
        user-supplied config file was found and used, or ``False`` when the
        bundled default was used instead.
    """
    config_path = Path(platformdirs.user_config_dir("gitignore")) / CONFIG_FILENAME
    if config_path.exists():
        data = config_path.read_text()
        is_local = True
    else:
        # Fall back to the config.yaml bundled with the package.  Using
        # importlib.resources (rather than __file__-relative paths) ensures
        # this works when the package is installed as a zip/wheel.
        data = (
            importlib.resources.files("gitignore")
            .joinpath(CONFIG_FILENAME)
            .read_text()
        )
        is_local = False
    raw = yaml.safe_load(data)
    return Config(editor=raw["editor"], file_types=raw["filetypes"]), is_local
