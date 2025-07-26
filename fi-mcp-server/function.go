package main

import (
	"context"
	"embed"
	"html/template"
	"net/http"
	"strings"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"

	"github.com/epifi/fi-mcp-lite/middlewares"
	"github.com/epifi/fi-mcp-lite/pkg"
)

//go:embed static/*
var staticFiles embed.FS

//go:embed test_data_dir/*
var testDataFiles embed.FS

var authMiddlewareFunc *middlewares.AuthMiddleware
var mcpServerFunc *server.Server

func init() {
	authMiddlewareFunc = middlewares.NewAuthMiddleware()
	mcpServerFunc = setupMCPServerFunc()

	// Register the Cloud Function
	functions.HTTP("FiMCPFunction", handleFunctionRequest)
}

func setupMCPServerFunc() *server.Server {
	s := server.NewMCPServer(
		"Hackathon MCP",
		"0.1.0",
		server.WithInstructions("A financial portfolio management MCP server that provides secure access to users' financial data through Fi Money, a financial hub for all things money. This MCP server enables users to:\n- Access comprehensive net worth analysis with asset/liability breakdowns\n- Retrieve detailed transaction histories for mutual funds and Employee Provident Fund accounts\n- View credit reports with scores, loan details, and account histories, this also contains user's date of birth that can be used for calculating their age\n\nIf the person asks, you can tell about Fi Money that it is money management platform that offers below services in partnership with regulated entities:\n\nAVAILABLE SERVICES:\n- Digital savings account with zero Forex cards\n- Invest in Indian Mutual funds, US Stocks (partnership with licensed brokers), Smart and Fixed Deposits.\n- Instant Personal Loans \n- Faster UPI and Bank Transfers payments\n- Credit score monitoring and reports\n\nIMPORTANT LIMITATIONS:\n- This MCP server retrieves only actual user data via Net worth tracker and based on consent provided by the user  and does not generate hypothetical or estimated financial information\n- In this version of the MCP server, user's historical bank transactions, historical stocks transaction data, salary (unless categorically declared) is not present. Don't assume these data points for any kind of analysis.\n\nCRITICAL INSTRUCTIONS FOR FINANCIAL DATA:\n\n1. DATA BOUNDARIES: Only provide information that exists in the user's Fi Money Net worth tracker. Never estimate, extrapolate, or generate hypothetical financial data.\n\n2. SPENDING ANALYSIS: If user asks about spending patterns, categories, or analysis tell the user we currently don't offer that data through the MCP:\n   - For detailed spending insights, direct them to: \"For comprehensive spending analysis and categorization, please use the Fi Money mobile app which provides detailed spending insights and budgeting tools.\"\n\n3. MISSING DATA HANDLING: If requested data is not available:\n   - Clearly state what data is missing\n   - Explain how user can connect additional accounts in Fi Money app\n   - Never fill gaps with estimated or generic information\n"),
		server.WithToolCapabilities(true),
		server.WithResourceCapabilities(true, true),
		server.WithLogging(),
		server.WithToolHandlerMiddleware(authMiddlewareFunc.AuthMiddleware),
	)

	// Register tools from pkg.ToolList
	for _, tool := range pkg.ToolList {
		s.AddTool(mcp.NewTool(tool.Name, mcp.WithDescription(tool.Description)), dummyHandlerFunc)
	}

	return s
}

func handleFunctionRequest(w http.ResponseWriter, r *http.Request) {
	// Handle static file requests
	if r.URL.Path == "/static/" || strings.HasPrefix(r.URL.Path, "/static/") {
		handleStaticFilesFunc(w, r)
		return
	}

	// Handle MCP stream requests
	if strings.HasPrefix(r.URL.Path, "/mcp/") {
		streamableServer := server.NewStreamableHTTPServer(mcpServerFunc,
			server.WithEndpointPath("/stream"),
		)
		streamableServer.ServeHTTP(w, r)
		return
	}

	// Handle auth endpoints
	switch r.URL.Path {
	case "/mockWebPage":
		webPageHandlerFunc(w, r)
	case "/login":
		loginHandlerFunc(w, r)
	default:
		http.NotFound(w, r)
	}
}

func handleStaticFilesFunc(w http.ResponseWriter, r *http.Request) {
	// Remove /static/ prefix
	path := strings.TrimPrefix(r.URL.Path, "/static/")

	// Read file from embedded filesystem
	content, err := staticFiles.ReadFile("static/" + path)
	if err != nil {
		http.NotFound(w, r)
		return
	}

	// Set content type based on file extension
	if strings.HasSuffix(path, ".html") {
		w.Header().Set("Content-Type", "text/html")
	} else if strings.HasSuffix(path, ".png") {
		w.Header().Set("Content-Type", "image/png")
	} else if strings.HasSuffix(path, ".css") {
		w.Header().Set("Content-Type", "text/css")
	} else if strings.HasSuffix(path, ".js") {
		w.Header().Set("Content-Type", "application/javascript")
	}

	w.Write(content)
}

func dummyHandlerFunc(_ context.Context, _ mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	return mcp.NewToolResultText("dummy handler"), nil
}

func webPageHandlerFunc(w http.ResponseWriter, r *http.Request) {
	sessionId := r.URL.Query().Get("sessionId")
	if sessionId == "" {
		http.Error(w, "sessionId is required", http.StatusBadRequest)
		return
	}

	// Read template from embedded filesystem
	templateContent, err := staticFiles.ReadFile("static/login.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	tmpl, err := template.New("login").Parse(string(templateContent))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	data := struct {
		SessionId            string
		AllowedMobileNumbers []string
	}{
		SessionId:            sessionId,
		AllowedMobileNumbers: pkg.GetAllowedMobileNumbers(),
	}

	err = tmpl.Execute(w, data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func loginHandlerFunc(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	sessionId := r.FormValue("sessionId")
	phoneNumber := r.FormValue("phoneNumber")

	if sessionId == "" || phoneNumber == "" {
		http.Error(w, "sessionId and phoneNumber are required", http.StatusBadRequest)
		return
	}

	authMiddlewareFunc.AddSession(sessionId, phoneNumber)

	// Read template from embedded filesystem
	templateContent, err := staticFiles.ReadFile("static/login_successful.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	tmpl, err := template.New("success").Parse(string(templateContent))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	err = tmpl.Execute(w, nil)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}
