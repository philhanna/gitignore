package gitignore

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
