package gitignore

import (
	"embed"
	"os"
	"path/filepath"

	"sigs.k8s.io/yaml"
)

//go:embed sample_config.yaml
var embeddedFS embed.FS

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// Config keeps track of the editor and file types
type Config struct {
	Editor    string              `json:"editor"`
	FileTypes map[string][]string `json:"filetypes"`
}

// ---------------------------------------------------------------------
// Constructor
// ---------------------------------------------------------------------

// NewConfig creates a new Config object
func NewConfig() Config {
	configData := GetConfigData()
	config := new(Config)
	yaml.Unmarshal(configData, config)
	return *config
}

// ---------------------------------------------------------------------
// Functions
// ---------------------------------------------------------------------

// Returns true if the specified file exists
func exists(filename string) bool {
	_, err := os.Stat(filename)
	if err != nil {
		return false
	}
	return true
}

// GetConfigData loads the configuration yaml data, either from the
// user's ~/.gitignore.yaml file or the default configuration.
func GetConfigData() []byte {
	var data []byte

	// See if the user has a local configuration file. If not, use the
	// sample one.
	home, _ := os.UserHomeDir()
	configFile := filepath.Join(home, ".gitignore.yaml")

	switch {
	case exists(configFile):
		data, _ = os.ReadFile(configFile)
	default:
		data, _ = embeddedFS.ReadFile("sample_config.yaml")
	}

	return data
}
