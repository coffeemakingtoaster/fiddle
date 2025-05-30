package main

import (
	"fmt"
	"os"
	"os/exec"

	"gopkg.in/yaml.v3"
)

type Sets struct {
	Sets []Set `yaml:"sets"`
}

type Set struct {
	Name string `yaml:"name"`
	Code string `yaml:"code"`
}

func run(code string) {
	code = "from lib.wrapper import *\n" + code
	cmd := exec.Command("python3", "-c", code)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		panic(err)
	}
}

func main() {

	fmt.Println("Starting...")

	yamlFile, err := os.ReadFile("./test.yaml")
	if err != nil {
		panic(err)
	}

	var sets Sets

	err = yaml.Unmarshal(yamlFile, &sets)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Loaded %d sets\n", len(sets.Sets))

	for _, v := range sets.Sets {
		fmt.Printf("Name: %s\n", v.Name)
		run(v.Code)
	}
}
