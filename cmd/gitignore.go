package main

import (
	"flag"
	"fmt"
	"log"
	"os"

	gi "github.com/philhanna/gitignore"
)

// Mainline
func main() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	usage := `usage: gitignore [OPTIONS] [type]

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

	opt := new(gi.Options)

	// Get the command line options
	flag.BoolVar(&opt.ListTypes, "types", false, "Lists supported file types")
	flag.BoolVar(&opt.List, "list", false, "Lists the current .gitignore")
	flag.BoolVar(&opt.Replace, "replace", false, "Replaces the current .gitignore, if it exists")
	flag.BoolVar(&opt.Verbose, "verbose", false, "Provides more details")
	flag.BoolVar(&opt.Edit, "edit", false, "Edit the file when done")

	flag.BoolVar(&opt.ListTypes, "t", false, "Short form of --types")
	flag.BoolVar(&opt.List, "l", false, "Short form of --list")
	flag.BoolVar(&opt.Replace, "r", false, "Short form of --replace")
	flag.BoolVar(&opt.Verbose, "v", false, "Short form of --verbose")
	flag.BoolVar(&opt.Edit, "e", false, "Short form of --edit")

	flag.Parse()

	// Get the file type, if specified
	if flag.NArg() > 0 {
		opt.Filetype = flag.Arg(0)
	}

	// Run the application
	app, err := gi.NewGitignore(*opt)
	if err != nil {
		log.Fatal(err)
	}

	err = app.Run()
	if err != nil {
		log.Fatal(err)
	}
}
