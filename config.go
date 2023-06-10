package gitignore

import (
	_ "embed"
	"errors"
	"fmt"
	"os"
	"path/filepath"

	"sigs.k8s.io/yaml"
)

//go:embed config.yaml
var SAMPLE_CONFIG string

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
func NewConfig() (Config, error) {
	configData, isLocal := GetConfigData()
	config := new(Config)
	err := yaml.Unmarshal(configData, &config)
	if err != nil {
		var errmsg string
		switch isLocal {
		case true:
			errmsg = fmt.Sprintf("Invalid yaml in local config.yaml: %s", err)
		case false:
			errmsg = fmt.Sprintf("Invalid yaml in sample config.yaml: %s", err)
		}
		return Config{}, errors.New(errmsg)
	}
	return *config, nil
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
// user's config.yaml file or the default configuration. The
// boolean return value is true if the configuration is local, false if
// it came from the sample configuration.
func GetConfigData() ([]byte, bool) {
	var data []byte

	// See if the user has a local configuration file. If not, use the
	// sample one.

	cfgdir, _ := os.UserConfigDir()
	configFile := filepath.Join(cfgdir, "gitignore", "config.yaml")

	var isLocal bool
	switch {
	case exists(configFile):
		isLocal = true
		data, _ = os.ReadFile(configFile)
	default:
		isLocal = false
		data = []byte(SAMPLE_CONFIG)
	}

	return data, isLocal
}
