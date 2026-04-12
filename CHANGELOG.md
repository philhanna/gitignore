# Change log for gitignore
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning].
The format is based on [Keep a Changelog].
	
## [Unreleased]

## [v2.1.0] - 2026-04-11
- Added comprehensive docstrings to all classes, methods, and functions in `src/`
- Added inline comments for non-obvious logic throughout `src/`
- Expanded README installation instructions with clone, venv, and `pip install -e .` steps

## [v2.0.0] - 2026-03-23
- Converted project from Go to Python
- Replaced `go.mod` with `pyproject.toml`
- Replaced `flag` package with `argparse`
- Replaced `github.com/ghodss/yaml` with `PyYAML`
- Replaced manual config-directory detection with `platformdirs`
- Bundled default `config.yaml` into package via `importlib.resources`
- Replaced Go tests (testify) with pytest
- Removed pre-built binaries; install via `pip` or `pipx`

## [v1.3.0] - 2023-06-10
- Added the `--types` option to list file types
- Fixed problem of finding configuration YAML file
- Switched to a different version of YAML
  
## [v1.2.0] - 2023-03-26
- Changed the location and name of the configuration file (see `README.md`)

## [v1.1.1] - 2023-02-27

### Fixed
- issue #5 - Invalid local user configuration .yaml is not being checked
 
## [v1.1.0] - 2023-02-24

### Added
- Added ability to use local configuration `.yaml` file
- Added this change log

### Changed
- Made `--quiet` the default. Replaced `--quiet` option with `--verbose`

## [v1.0.0] - 2023-02-24
- Preliminary Go version

[Semantic Versioning]: http://semver.org
[Keep a Changelog]: http://keepachangelog.com
[Unreleased]: https://github.com/philhanna/gitignore/compare/v2.1.0..HEAD
[v2.1.0]: https://github.com/philhanna/gitignore/compare/v2.0.0..v2.1.0
[v2.0.0]: https://github.com/philhanna/gitignore/compare/v1.3.0..v2.0.0
[v1.3.0]: https://github.com/philhanna/gitignore/compare/v1.2.0..v1.3.0
[v1.2.0]: https://github.com/philhanna/gitignore/compare/v1.1.1..v1.2.0
[v1.1.1]: https://github.com/philhanna/gitignore/compare/v1.1.0..v1.1.1
[v1.1.0]: https://github.com/philhanna/gitignore/compare/v1.0.0..v1.1.0
[v1.0.0]: https://github.com/philhanna/gitignore/compare/91591ad..v1.0.0
