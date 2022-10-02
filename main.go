package main

import (
	"fmt"
	"io/fs"
	"io/ioutil"
	"os"
	"time"
)

type fileObject struct {
	location         string
	size             uint64
	permissions      fs.FileMode
	lastModifiedDate string
}

var stored []string
var objectFiles []fileObject

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage:", "program", "base directory path")
		os.Exit(1)
	}

	dir := os.Args[1]
	files := returnAllFilesFromBaseDir(dir)

	for _, file := range files {
		var object fileObject

		fileInfo, err := os.Stat(file)
		if err != nil {
			panic(err)
		}

		object.location = file
		object.size = uint64(fileInfo.Size())
		object.permissions = fileInfo.Mode()
		object.lastModifiedDate = fileInfo.ModTime().Format(time.RFC822)

		objectFiles = append(objectFiles, object)
	}

	for _, fileInfo := range objectFiles {
		fmt.Println(fileInfo)
	}
}

func returnAllFilesFromBaseDir(baseDirPath string) []string {
	content, err := ioutil.ReadDir(baseDirPath)
	if err != nil {
		panic(err)
	}

	for _, file := range content {
		if file.IsDir() {
			returnAllFilesFromBaseDir(baseDirPath + "/" + file.Name())
			continue
		}

		stored = append(stored, baseDirPath+"/"+file.Name())
	}

	return stored
}
