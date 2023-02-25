package gitignore

import (
	"errors"
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
func (self Gitignore) Run() error {

	// List the file if requested.
	if self.opt.List {
		if exists(FILENAME) {
			self.ListFile()
		}
		return nil
	}

	// Create the file if it does not exist, or if it exists and the
	// replace option was specified.
	if exists(FILENAME) {
		if self.opt.Replace {
			err := self.Create()
			if err != nil {
				return err
			}
		} else {
			if !self.opt.Quiet {
				fmt.Printf("Not replacing existing %s\n", FILENAME)
				fmt.Printf("Use -r flag to replace\n")
				fmt.Printf("Try -h for help\n")
			}
		}
	} else {
		err := self.Create()
		if err != nil {
			return err
		}
	}

	// List the contents of the file.
	if !self.opt.Quiet && !self.opt.Edit {
		self.ListFile()
	}

	// Bring it up in an editor if the edit option was specified.
	if self.opt.Edit {
		self.EditFile()
	}

	return nil
}

// Create creates the .gitignore file
func (self Gitignore) Create() error {
	if !self.opt.Quiet {
		fmt.Printf("Creating new %s\n", FILENAME)
	}

	// Create the file
	fp, _ := os.Create(FILENAME)
	defer fp.Close()

	// See if a filetype was specified (e.g., "java", "py", etc.) If
	// not, just use the defaults
	filetype := self.opt.Filetype
	if filetype == "" {
		for _, line := range getDefaults() {
			fmt.Fprintf(fp, line)
		}
		return nil
	}

	// If a filetype *was* specified, see if it is one of the configured
	// types
	lines, ok := self.config.Filetypes[filetype]
	if !ok {
		errmsg := fmt.Sprintf("%q is not a recognized file type\n", filetype)
		return errors.New(errmsg)
	}

	// If it was a configured type, use the lines from the configuration
	for _, line := range lines {
		fmt.Fprintln(fp, line)
	}
	return nil
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
