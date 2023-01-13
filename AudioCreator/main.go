package main

import (
	"bufio"
	"log"
	"os"
	"strings"
	"sync"

	htgotts "github.com/hegedustibor/htgo-tts"
	"github.com/hegedustibor/htgo-tts/handlers"
	"github.com/hegedustibor/htgo-tts/voices"
)

func check(e error) {
	if e != nil {
		log.Fatal(e)
	}
}

func readFile(filename string) []string {
	readFile, err := os.Open(filename)
	check(err)

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)
	var fileLines []string

	for fileScanner.Scan() {
		fileLines = append(fileLines, fileScanner.Text())
	}
	readFile.Close()

	return fileLines
}

func dirExitsCreate(path string) {
	os.MkdirAll(path, os.ModePerm)
}

func fileExists(path string) bool {

	_, err := os.Stat(path)
	if err == nil {
		return true
	} else {
		return false
	}

}

func createAudioFile(root string, folder string, filename string, text string) {

	var speech htgotts.Speech

	if root == "English" {
		speech = htgotts.Speech{
			Folder:   folder,
			Language: voices.English,
			Handler:  &handlers.MPlayer{},
		}
	} else if root == "French" {
		speech = htgotts.Speech{
			Folder:   folder,
			Language: voices.French,
			Handler:  &handlers.MPlayer{},
		}
	}
	speech.CreateSpeechFile(text, filename)
}

func main() {
	var wg sync.WaitGroup

	config := strings.Split(readFile("config.csv")[1], ";")
	createFilesFile := config[len(config)-1]

	fileData := readFile(createFilesFile)[1:]

	// create root folder
	root := strings.Split(fileData[0], ";")[1]
	dirExitsCreate(root)

	for i := range fileData {

		dataVec := strings.Split(fileData[i], ";")
		dataVec = append(dataVec[0:1], dataVec[2:]...)

		folder := root + "/" + dataVec[1]
		dirExitsCreate(folder)

		filename := dataVec[2]
		text := dataVec[0]

		if !fileExists(folder + "/" + filename) {

			wg.Add(1)
			go func(i int) {
				createAudioFile(root, folder, strings.ReplaceAll(filename, ".mp3", ""), text)
				wg.Done()
			}(i)

		}

	}

	wg.Wait()
}

// go build -ldflags "-s -w -H=windowsgui"
