package gitignore

import (
	"fmt"
	"os"
	"os/exec"
)

const FILENAME = ".gitignore"

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// Config keeps track of the editor and file types
type Config struct {
	Editor    string              `json:"editor"`
	Filetypes map[string][]string `json:"filetypes"`
}

// Options holds the command line options
type Options struct {
	List     bool
	Replace  bool
	Edit     bool
	Quiet    bool
	Filetype string
}

type Gitignore struct {
	opt    Options
	config Config
}

// ---------------------------------------------------------------------
// Constructor
// ---------------------------------------------------------------------

// NewGitignore creates a new Gitignore struct
func NewGitignore(options Options, config Config) Gitignore {
	p := new(Gitignore)
	p.opt = options
	p.config = config
	return *p
}

// ---------------------------------------------------------------------
// Methods
// ---------------------------------------------------------------------

// Run runs the application
func (self Gitignore) Run() {

	// List the file if requested.
	if self.opt.List {
		if exists(FILENAME) {
			self.ListFile()
		}
		return
	}

	// Create the file if it does not exist, or if it exists and the
	// replace option was specified.
	if exists(FILENAME) {
		if self.opt.Replace {
			self.Create()
		} else {
			if !self.opt.Quiet {
				fmt.Printf("Not replacing existing %s\n", FILENAME)
				fmt.Printf("Use -r flag to replace\n")
				fmt.Printf("Try -h for help\n")
			}
		}
	} else {
		self.Create()
	}

	// List the contents of the file.
	if !self.opt.Quiet && !self.opt.Edit {
		self.ListFile()
	}

	// Bring it up in an editor if the edit option was specified.
	if self.opt.Edit {
		self.EditFile()
	}

	return
}

// Create creates the .gitignore file
func (self Gitignore) Create() {
	if !self.opt.Quiet {
		fmt.Printf("Creating new %s\n", FILENAME)
	}
	
	// Create the file
	fp, _ := os.Create(FILENAME)
	defer fp.Close()
	filetype := self.opt.Filetype
	lines, ok := self.config.Filetypes[filetype]
	if !ok {
		lines = getDefaults()
	}
	for _, line := range lines {
		fmt.Fprintln(fp, line)
	}
}

// EditFile brings up the configured editor on the .gitignore file
func (self Gitignore) EditFile() {
	cmd := exec.Command(self.config.Editor, FILENAME)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		fmt.Fprintf(os.Stderr, "gitignore: %v\n", err)
	}
}

// ListFile prints the .gitignore file
func (self Gitignore) ListFile() {
	data, _ := os.ReadFile(".gitignore")
	fmt.Println(string(data))
}

// ---------------------------------------------------------------------
// Functions
// ---------------------------------------------------------------------

// exists returns true if the specified file exists
func exists(filename string) bool {
	_, err := os.Stat(filename)
	if err != nil {
		return false
	}
	return true
}

// getDefaults returns the default .gitignore data
func getDefaults() []string {
	defaults := []string{
		"*.swp",
	}
	return defaults
}
