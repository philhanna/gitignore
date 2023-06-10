package gitignore

import (
	_ "embed"
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test_exists(t *testing.T) {
	tests := []struct {
		name string
		filename string
		want bool
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
