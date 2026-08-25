package main

import "strings"

type RopeNode struct {
	weight  int
	content string
	left    *RopeNode
	right   *RopeNode
}

func (r *RopeNode) IsLeaf() bool { return len(r.content) > 0 }

func (r *RopeNode) GetDirectLeafSum() int {
	res := r.weight
	if r.right != nil {
		res += r.right.weight
	}
	return res
}

func (r *RopeNode) GetContent() string {
	if r.IsLeaf() {
		return r.content
	}
	var sb strings.Builder
	if r.left != nil {
		sb.Write([]byte(r.left.GetContent()))
	}
	if r.right != nil {
		sb.Write([]byte(r.right.GetContent()))
	}
	return sb.String()
}

func main() {
	root := RopeNode{}

	print(root.GetContent())

}
