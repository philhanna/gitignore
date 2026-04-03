from .app import Gitignore
from .cli import parse_args
from .config import load_config


def main() -> None:
    options = parse_args()
    config, _ = load_config()
    app = Gitignore(options, config)
    app.run()


if __name__ == "__main__":
    main()
