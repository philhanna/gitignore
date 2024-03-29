package gitignore

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"sort"
	"strings"
)

const FILENAME = ".gitignore"

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// Gitignore holds the application data
type Gitignore struct {
	opt    Options
	config Config
}

// ---------------------------------------------------------------------
// Constructor
// ---------------------------------------------------------------------

// NewGitignore creates a new Gitignore struct
func NewGitignore(options Options) (Gitignore, error) {
	p := new(Gitignore)
	p.opt = options
	config, err := NewConfig()
	if err != nil {
		return Gitignore{}, err
	}
	p.config = config
	return *p, nil
}

// ---------------------------------------------------------------------
// Methods
// ---------------------------------------------------------------------

// Run runs the application
func (self Gitignore) Run() error {

	// List the supported types if requested
	if self.opt.ListTypes {
		self.ListTypes()
		return nil
	}

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
			if err := self.Create(); err != nil {
				return err
			}
		} else {
			if self.opt.Verbose {
				fmt.Printf("Not replacing existing %s\n", FILENAME)
				fmt.Printf("Use -r flag to replace\n")
				fmt.Printf("Try -h for help\n")
			}
		}
	} else {
		if err := self.Create(); err != nil {
			return err
		}
	}

	// List the contents of the file.
	if self.opt.Verbose && !self.opt.Edit {
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

	// Use the appropriate lines
	var lines []string

	filetype := self.opt.Filetype
	switch {
	case filetype != "":

		// If a file type was specified (e.g., "java", "py", "go"), see if it
		// is one of the configured types
		var ok bool
		lines, ok = self.config.FileTypes[filetype]
		if !ok {
			return fmt.Errorf("%q is not a recognized file type\n", filetype)
		}

	default:
		lines = GetDefaults()
	}

	// Write the file
	if self.opt.Verbose {
		fmt.Printf("Creating %s\n", FILENAME)
	}
	fp, _ := os.Create(FILENAME)
	defer fp.Close()
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
		log.Fatal(err)
	}
}

// ListFile prints the .gitignore file
func (self Gitignore) ListFile() {
	data, _ := os.ReadFile(".gitignore")
	fmt.Println(string(data))
}

// ListTypes prints the list of supported file types in alphabetical
// order
func (self Gitignore) ListTypes() {

	ftMap := self.config.FileTypes

	// Sort the list
	keys := make([]string, 0)
	for key := range ftMap {
		keys = append(keys, key)
	}
	sort.Strings(keys)

	// Print the list
	widest := 0
	for _, key := range keys {
		if len(key) > widest {
			widest = len(key)
		}
	}
	for _, key := range keys {
		padded := padString(key, widest)
		fmt.Printf("%s (%d entries)\n", padded, len(ftMap[key]))
	}
}

// ---------------------------------------------------------------------
// Functions
// ---------------------------------------------------------------------

// GetDefaults returns the default .gitignore data
func GetDefaults() []string {
	defaults := []string{
		"*.swp",
	}
	return defaults
}

// padString appends spaces to the right of a string
func padString(s string, length int) string {
	padding := length - len(s)
	if padding <= 0 {
		return s // No padding needed
	}
	return s + strings.Repeat(" ", padding)
}
