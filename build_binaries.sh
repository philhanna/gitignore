#! /bin/bash
GOOS=linux GOARCH=amd64 go build -o bin/gitignore-amd64-linux cmd/gitignore.go
GOOS=windows GOARCH=amd64 go build -o bin/gitignore-amd64.exe cmd/gitignore.go
GOOS=darwin GOARCH=amd64 go build -o bin/gitignore-amd64-darwin cmd/gitignore.go
