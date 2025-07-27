package main

import (
	"embed"
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"strings"
)

//go:embed static/*
var staticFiles embed.FS

//go:embed test_data_dir/*
var testDataFiles embed.FS

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	http.HandleFunc("/", handleRequest)

	log.Printf("🚀 Fi MCP Server starting on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
	log.Printf("Request: %s %s", r.Method, r.URL.Path)

	switch {
	case strings.HasPrefix(r.URL.Path, "/auth"):
		handleAuth(w, r)
	case strings.HasPrefix(r.URL.Path, "/mcp"):
		handleMCPRequest(w, r)
	case strings.HasPrefix(r.URL.Path, "/mockWebPage"):
		handleMockWebPage(w, r)
	default:
		handleRoot(w, r)
	}
}

func handleAuth(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var authReq struct {
		PhoneNumber string `json:"phoneNumber"`
	}

	if err := json.NewDecoder(r.Body).Decode(&authReq); err != nil {
		log.Printf("Error decoding auth request: %v", err)
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Simple phone number validation
	allowedNumbers := map[string]bool{
		"1010101010": true, "1111111111": true, "1212121212": true,
		"1313131313": true, "1414141414": true, "2020202020": true,
		"2121212121": true, "2222222222": true, "2525252525": true,
		"3333333333": true, "4444444444": true, "5555555555": true,
		"6666666666": true, "7777777777": true, "8888888888": true,
		"9999999999": true,
	}

	phoneNumber := strings.TrimSpace(authReq.PhoneNumber)
	response := map[string]interface{}{
		"success": allowedNumbers[phoneNumber],
	}

	if response["success"].(bool) {
		response["token"] = fmt.Sprintf("token_%s", phoneNumber)
		response["sessionId"] = fmt.Sprintf("session_%s", phoneNumber)
		w.WriteHeader(http.StatusOK)
		log.Printf("✅ Authentication successful for %s", phoneNumber)
	} else {
		response["error"] = "Phone number not authorized"
		w.WriteHeader(http.StatusUnauthorized)
		log.Printf("❌ Authentication failed for %s", phoneNumber)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func handleMCPRequest(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	// Read test data for demonstration
	if r.URL.Path == "/mcp/test" {
		phoneNumber := r.URL.Query().Get("phone")
		if phoneNumber != "" {
			dataPath := fmt.Sprintf("test_data_dir/%s/fetch_net_worth.json", phoneNumber)
			if data, err := testDataFiles.ReadFile(dataPath); err == nil {
				w.Write(data)
				return
			}
		}
	}

	response := map[string]interface{}{
		"status":  "MCP endpoint ready",
		"server":  "Fi MCP Server",
		"version": "0.1.0",
		"endpoints": map[string]string{
			"test_data": "/mcp/test?phone=1111111111",
			"auth":      "/auth",
		},
	}
	json.NewEncoder(w).Encode(response)
}

func handleMockWebPage(w http.ResponseWriter, r *http.Request) {
	sessionID := r.URL.Query().Get("sessionId")
	if sessionID == "" {
		sessionID = "default-session"
	}

	// Load login template
	tmplData, err := staticFiles.ReadFile("static/login.html")
	if err != nil {
		log.Printf("Error reading login template: %v", err)
		http.Error(w, "Template not found", http.StatusInternalServerError)
		return
	}

	tmpl, err := template.New("login").Parse(string(tmplData))
	if err != nil {
		log.Printf("Error parsing template: %v", err)
		http.Error(w, "Template error", http.StatusInternalServerError)
		return
	}

	data := struct {
		SessionID string
	}{
		SessionID: sessionID,
	}

	w.Header().Set("Content-Type", "text/html")
	err = tmpl.Execute(w, data)
	if err != nil {
		log.Printf("Error executing template: %v", err)
		http.Error(w, "Template execution error", http.StatusInternalServerError)
	}
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	response := map[string]interface{}{
		"message": "Fi MCP Server",
		"version": "0.1.0",
		"status":  "running",
		"endpoints": map[string]string{
			"auth":       "/auth",
			"mcp":        "/mcp",
			"mcp_test":   "/mcp/test?phone=1111111111",
			"mock_login": "/mockWebPage?sessionId=your-session-id",
		},
		"deployment": "Google Cloud Run",
	}

	json.NewEncoder(w).Encode(response)
}
