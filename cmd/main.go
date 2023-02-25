package main

import (
	"flag"
	"fmt"
	"os"

	"embed"
	gi "github.com/philhanna/gitignore"
	yaml "sigs.k8s.io/yaml"
)

//go:embed default_config.yaml
var f embed.FS

// Mainline
func main() {
	usage := `usage: gitignore [-h] [-l] [-r] [-q] [-e] [type]

Creates a basic .gitignore file in the current directory

positional arguments:
  filetype       Type of files (['java', 'go', 'py', 'ly', etc.])

options:
  -h, --help     show this help message and exit
  -l, --list     Lists the current .gitignore
  -r, --replace  Replaces the current .gitignore, if it exists
  -q, --quiet    Suppresses the printing of the .gitignore file
  -e, --edit     Edit the file when done
`
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "%s\n", usage)
		return
	}

	opt := new(gi.Options)

	// Get the command line options

	flag.BoolVar(&opt.List, "list", false, "Lists the current .gitignore")
	flag.BoolVar(&opt.Replace, "replace", false, "Replaces the current .gitignore, if it exists")
	flag.BoolVar(&opt.Quiet, "quiet", false, "Suppresses the printing of the .gitignore file")
	flag.BoolVar(&opt.Edit, "edit", false, "Edit the file when done")

	flag.BoolVar(&opt.List, "l", false, "Short form of --list")
	flag.BoolVar(&opt.Replace, "r", false, "Short form of --replace")
	flag.BoolVar(&opt.Quiet, "q", false, "Short form of --quiet")
	flag.BoolVar(&opt.Edit, "e", false, "Short form of --edit")

	flag.Parse()

	// Get the file type, if specified
	if flag.NArg() > 0 {
		opt.Filetype = flag.Arg(0)
	}

	configBytes, err := f.ReadFile("default_config.yaml")
	if err != nil {
		fmt.Fprintf(os.Stderr, "gitignore: Default configuration file not found\n")
		return
	}
	config := gi.Config{}
	yaml.Unmarshal(configBytes, &config)

	// Run the application
	app := gi.NewGitignore(*opt, config)
	err = app.Run()
	if err != nil {
		fmt.Fprintf(os.Stderr, "gitignore: %s\n", err.Error())
	}
}
