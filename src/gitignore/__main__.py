from .app import Gitignore
from .cli import parse_args
from .config import load_config


def main() -> None:
    """Entry point for the gitignore command-line tool.

    Parses command-line arguments, loads the user configuration, constructs
    the application, and runs the requested subcommand(s).
    """
    options = parse_args()
    config, _ = load_config()
    app = Gitignore(options, config)
    app.run()


if __name__ == "__main__":
    main()
