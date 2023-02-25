# gitignore
[![Go Report Card](https://goreportcard.com/badge/github.com/philhanna/gitignore)][idGoReportCard]
[![PkgGoDev](https://pkg.go.dev/badge/github.com/philhanna/gitignore)][idPkgGoDev]

## Overview

Creates a basic .gitignore file in the current directory, with
configurable sets of ignore lines for different file types in
the project.

## Usage
```
usage: gitignore [-h] [-l] [-r] [-q] [-e] [type]

Creates a basic .gitignore file in the current directory

positional arguments:
  filetype       Type of files (e.g. go, java, py)

options:
  -h, --help     Show this help message and exits
  -l, --list     Lists the current .gitignore
  -r, --replace  Replaces the current .gitignore, if it exists
  -v, --verbose  Provides more details
  -e, --edit     Edit the file when done
```

## Installation

### Binary executables
There are pre-built binary executables for Linux, Windows, and MacOS in
the `bin` directory.  Copy the appropriate one for your operating system
to a directory in your path, and rename it as desired.

### From source
If you have Go installed, you can install the application with this:
```
go install cmd/gitignore.go
```



## Configuration

The application usage a configurable `.yaml` file for file types
(and the preferred text editor for the generated `.gitignore`).
There is a sample included with the application, but the user
can specify their own by creating a file named `.gitignore.yaml`
in their home directory.

The configuration file must include entries for `editor` and `filetypes`.
The `filetypes` entry contains one or more file type names (such as
java, go, py, etc.)  For each of those names, there should be an array
of lines to be used in the generated `.gitignore` file.

Here is a sample:

```
editor: vim
filetypes:
  java:
  - "*.swp"
  - build/
  - doc/
  - "*.class"
  - .classpath
  - .project
  go:
  - "*.swp"
  py:
  - "*.swp"
  - "*.pyc"
  - "*.pyo"
  - __pycache__
  - .idea/
  - venv/
  - build/
  - dist/
  - "*.egg-info/"

```

## References
- [Github repository](https://github.com/philhanna/gitignore)
- [.gitignore documentation](https://git-scm.com/docs/gitignore)
- [Wikipedia article on YAML](https://en.wikipedia.org/wiki/YAML)
- [YAML 1.2.0 specification](https://yaml.org/spec/1.2.0/)

[idGoReportCard]: https://goreportcard.com/report/github.com/philhanna/gitignore
[idPkgGoDev]: https://pkg.go.dev/github.com/philhanna/gitignore
