"""Entry point for ``python -m gitignore`` invocation.

Wires together argument parsing, configuration loading, and the main
application class, then hands control to :meth:`~gitignore.app.Gitignore.run`.
"""

from .app import Gitignore
from .cli import parse_args
from .config import load_config


def main() -> None:
    """Parse arguments, load config, and run the application.

    This function is also registered as the ``gitignore`` console-script
    entry point in ``pyproject.toml``, so it is called for both
    ``python -m gitignore`` and the installed ``gitignore`` command.

    The ``is_local`` flag returned by :func:`~gitignore.config.load_config`
    is intentionally discarded here; it exists for callers (e.g. tests) that
    want to know which config source was used.
    """
    options = parse_args()
    config, _ = load_config()
    app = Gitignore(options, config)
    app.run()


if __name__ == "__main__":
    main()
