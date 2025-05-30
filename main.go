package main

import (
	"flag"
	"fmt"
	"os"
)

type unix_file struct {
	name             string
	location         string
	size             int64
	permissions      string
	lastModifiedDate string
}

func bitwisePermission(bits int) string {
	var permission string
	if bits&4 != 0 {
		permission += "r"
	} else {
		permission += "-"
	}
	if bits&2 != 0 {
		permission += "w"
	} else {
		permission += "-"
	}
	if bits&1 != 0 {
		permission += "x"
	} else {
		permission += "-"
	}
	return permission
}

var files []unix_file

func getFilesFromDir(path string) []unix_file {
	dir_content, err := os.ReadDir(path)
	if err != nil {
		panic(err)
	}
	for _, object := range dir_content {
		if object.IsDir() {
			getFilesFromDir(path + "/" + object.Name())
			continue
		}
		objectInfo, err := object.Info()
		if err != nil {
			panic(err)
		}
		file := unix_file{
			name:             objectInfo.Name(),
			location:         path + "/" + objectInfo.Name(),
			size:             objectInfo.Size(),
			permissions:      bitwisePermission(int(objectInfo.Mode())),
			lastModifiedDate: objectInfo.ModTime().Format("2006-01-02T15:04:05"),
		}
		files = append(files, file)
	}
	return files
}

func main() {
	dir := flag.String("directory", "", "directory to list files")
	flag.Parse()

	if *dir == "" {
		fmt.Fprintln(os.Stderr, "Error: missing parameter --directory")
		flag.Usage()
		os.Exit(1)
	}
	fmt.Println(getFilesFromDir(*dir))
}
