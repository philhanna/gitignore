package gitignore

import (
	_ "embed"
	"os"
	"path/filepath"
	"testing"

	"github.com/ghodss/yaml"
	"github.com/stretchr/testify/assert"
)

func Test_exists(t *testing.T) {
	tests := []struct {
		name     string
		filename string
		want     bool
	}{
		{"Directory", "testdata", true},
		{"Empty file", "testdata/empty", true},
		{"Regular file", "testdata/regular.txt", true},
		{"Non-existent file", "testdata/nothing", false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			want := tt.want
			have := exists(tt.filename)
			assert.Equal(t, want, have)
		})
	}
}

func TestGetConfigData(t *testing.T) {
	data, isLocal := GetConfigData()
	cfgdir, _ := os.UserConfigDir()
	configFile := filepath.Join(cfgdir, "gitignore", "config.yaml")
	if exists(configFile) {
		assert.True(t, isLocal)
	} else {
		assert.False(t, isLocal)
	}
	var o any
	err := yaml.Unmarshal(data, &o)
	assert.Nil(t, err)
}

func TestNewConfig(t *testing.T) {
	p, err := NewConfig()
	assert.Nil(t, err)
	assert.NotEqual(t, "", p.Editor)
	assert.NotZero(t, len(p.FileTypes))
}
