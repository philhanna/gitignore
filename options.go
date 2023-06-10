package gitignore

import (
	"flag"
	"fmt"
	"os"
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

	const usage = `usage: gitignore [OPTIONS] [type]

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
`
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "%s\n", usage)
		return
	}
}
