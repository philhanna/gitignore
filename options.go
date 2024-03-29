package gitignore

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// Options holds the command line options
type Options struct {
	ListTypes bool
	List      bool
	Replace   bool
	Edit      bool
	Verbose   bool
	Filetype  string
}

func init() {

	const usage = `usage: gitignore [OPTIONS] [filetype]

Creates a basic .gitignore file in the current directory

positional arguments:
  filetype       Type of files (e.g. go, java, py)

options:
  -h, --help     Show this help message and exits
  -t, --types    Lists supported file types
  -l, --list     Lists the current .gitignore
  -r, --replace  Replaces the current .gitignore, if it exists
  -v, --verbose  Provides more details
  -e, --edit     Edit the file when done

Rules are configured in %s
`
	const PACKAGE_NAME = "gitignore"
	const CONFIG_FILE = "config.yaml"
	configDir, _ := os.UserConfigDir()
	fullName := filepath.Join(configDir, PACKAGE_NAME, CONFIG_FILE)
	fullUsage := fmt.Sprintf(usage, fullName)
	flag.Usage = func() {
		fmt.Fprintln(os.Stderr, fullUsage)
		return
	}
}
