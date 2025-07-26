package main

import (
	"fmt"
	"net/http"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

func init() {
	functions.HTTP("FiMCPFunction", helloHTTP)
}

func helloHTTP(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Hello, Fi MCP Server!")
}
