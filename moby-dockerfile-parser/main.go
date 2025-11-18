package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/moby/buildkit/frontend/dockerfile/parser"
)

func consumeChild(node *parser.Node) {
	if node == nil {
		return
	}
	fmt.Printf("Instruction: %s\n", node.Value)
	fmt.Printf("Params: %v\n", node.Flags)
	fmt.Printf("Special properties: %v\n", node.Attributes)

	node = node.Next
	var sb strings.Builder
	for node != nil {
		sb.WriteString(fmt.Sprintf(" %s ", node.Value))
		node = node.Next
	}
	fmt.Printf("Content: %s\n", sb.String())
}

func consume(node *parser.Node, prefix string) {
	if node == nil {
		return
	}
	fmt.Printf("%s %v %d (children %d)", prefix, node.Value, len(node.Value), len(node.Children))
	for _, c := range node.Children {
		consumeChild(c)
	}
	return
	consume(node.Next, prefix)
}

func main() {
	r, _ := os.Open("./aiflow.Dockerfile")
	res, _ := parser.Parse(r)
	for _, warning := range res.Warnings {
		fmt.Println(warning)
	}
	consume(res.AST, "")
}
