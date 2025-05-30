package main

import "C"

//export get_context
func get_context() *C.char {
	return C.CString("context")
}

func main() {}
