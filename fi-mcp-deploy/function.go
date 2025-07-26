package main

import (
	"context"
	"embed"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"github.com/samber/lo"
)

//go:embed static/*
var staticFiles embed.FS

//go:embed test_data_dir/*
var testDataFiles embed.FS

// ToolInfo holds the name and description of a tool
type ToolInfo struct {
	Name        string
	Description string
}

// ToolList is the list of all tools and their descriptions
var ToolList = []ToolInfo{
	{
		Name:        "fetch_net_worth",
		Description: "Calculate comprehensive net worth using ONLY actual data from accounts users connected on Fi Money including: Bank account balances, Mutual fund investment holdings, Indian Stocks investment holdings, Total US Stocks investment (If investing through Fi Money app), EPF account balances, Credit card debt and loan balances (if credit report connected), Any other assets/liabilities linked to Fi Money platform.",
	},
	{
		Name:        "fetch_credit_report",
		Description: "Retrieve comprehensive credit report including scores, active loans, credit card utilization, payment history, date of birth and recent inquiries from connected credit bureaus.",
	},
	{
		Name:        "fetch_epf_details",
		Description: "Retrieve detailed EPF (Employee Provident Fund) account information including: Account balance and contributions, Employer and employee contribution history, Interest earned and credited amounts.",
	},
	{
		Name:        "fetch_mf_transactions",
		Description: "Retrieve detailed transaction history from accounts connected to Fi Money platform including: Mutual fund transactions.",
	},
	{
		Name:        "fetch_bank_transactions",
		Description: "Retrieve detailed bank transactions for each bank account connected to Fi money platform.",
	},
	{
		Name:        "fetch_stock_transactions",
		Description: "Retrieve detailed indian stock transactions for all connected indian stock accounts to Fi money platform.",
	},
}

// AuthMiddleware handles authentication for the MCP server
type AuthMiddleware struct {
	sessionStore map[string]string
}

func NewAuthMiddleware() *AuthMiddleware {
	return &AuthMiddleware{
		sessionStore: make(map[string]string),
	}
}

var loginRequiredJson = `{"status": "login_required","login_url": "%s","message": "Needs to login first by going to the login url.\nShow the login url as clickable link if client supports it. Otherwise display the URL for users to copy and paste into a browser. \nAsk users to come back and let you know once they are done with login in their browser"}`

func (m *AuthMiddleware) AuthMiddleware(next server.ToolHandlerFunc) server.ToolHandlerFunc {
	return func(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		sessionId := server.ClientSessionFromContext(ctx).SessionID()
		phoneNumber, ok := m.sessionStore[sessionId]
		if !ok {
			loginUrl := m.getLoginUrl(sessionId)
			return mcp.NewToolResultText(fmt.Sprintf(loginRequiredJson, loginUrl)), nil
		}
		if !lo.Contains(GetAllowedMobileNumbers(), phoneNumber) {
			return mcp.NewToolResultError("phone number is not allowed"), nil
		}
		ctx = context.WithValue(ctx, "phone_number", phoneNumber)
		toolName := req.Params.Name
		data, readErr := os.ReadFile("test_data_dir/" + phoneNumber + "/" + toolName + ".json")
		if readErr != nil {
			log.Println("error reading test data file", readErr)
			return mcp.NewToolResultError("error reading test data file"), nil
		}
		return mcp.NewToolResultText(string(data)), nil
	}
}

func (m *AuthMiddleware) getLoginUrl(sessionId string) string {
	// For Cloud Functions, use the function URL if available
	if functionURL := os.Getenv("FUNCTION_URL"); functionURL != "" {
		return fmt.Sprintf("%s/mockWebPage?sessionId=%s", functionURL, sessionId)
	}
	// Fallback to generic URL that the user can update
	return fmt.Sprintf("https://YOUR-FUNCTION-URL/mockWebPage?sessionId=%s", sessionId)
}

func (m *AuthMiddleware) AddSession(sessionId, phoneNumber string) {
	m.sessionStore[sessionId] = phoneNumber
}

// GetAllowedMobileNumbers returns a slice of directory names in test_data_dir
func GetAllowedMobileNumbers() []string {
	dirEntries, err := os.ReadDir("test_data_dir")
	if err != nil {
		return nil
	}
	var numbers []string
	for _, entry := range dirEntries {
		if entry.IsDir() {
			numbers = append(numbers, entry.Name())
		}
	}
	return numbers
}

var authMiddleware *AuthMiddleware
var mcpServer *server.Server

func init() {
	authMiddleware = NewAuthMiddleware()
	mcpServer = setupMCPServer()

	// Register the Cloud Function
	functions.HTTP("FiMCPFunction", handleRequest)
}

func setupMCPServer() *server.Server {
	s := server.NewMCPServer(
		"Fi MCP Server",
		"1.0.0",
		server.WithInstructions("A financial portfolio management MCP server that provides secure access to users' financial data through Fi Money, a financial hub for all things money. This MCP server enables users to:\n- Access comprehensive net worth analysis with asset/liability breakdowns\n- Retrieve detailed transaction histories for mutual funds and Employee Provident Fund accounts\n- View credit reports with scores, loan details, and account histories, this also contains user's date of birth that can be used for calculating their age\n\nIf the person asks, you can tell about Fi Money that it is money management platform that offers below services in partnership with regulated entities:\n\nAVAILABLE SERVICES:\n- Digital savings account with zero Forex cards\n- Invest in Indian Mutual funds, US Stocks (partnership with licensed brokers), Smart and Fixed Deposits.\n- Instant Personal Loans \n- Faster UPI and Bank Transfers payments\n- Credit score monitoring and reports\n\nIMPORTANT LIMITATIONS:\n- This MCP server retrieves only actual user data via Net worth tracker and based on consent provided by the user  and does not generate hypothetical or estimated financial information\n- In this version of the MCP server, user's historical bank transactions, historical stocks transaction data, salary (unless categorically declared) is not present. Don't assume these data points for any kind of analysis.\n\nCRITICAL INSTRUCTIONS FOR FINANCIAL DATA:\n\n1. DATA BOUNDARIES: Only provide information that exists in the user's Fi Money Net worth tracker. Never estimate, extrapolate, or generate hypothetical financial data.\n\n2. SPENDING ANALYSIS: If user asks about spending patterns, categories, or analysis tell the user we currently don't offer that data through the MCP:\n   - For detailed spending insights, direct them to: \"For comprehensive spending analysis and categorization, please use the Fi Money mobile app which provides detailed spending insights and budgeting tools.\"\n\n3. MISSING DATA HANDLING: If requested data is not available:\n   - Clearly state what data is missing\n   - Explain how user can connect additional accounts in Fi Money app\n   - Never fill gaps with estimated or generic information\n"),
		server.WithToolCapabilities(true),
		server.WithResourceCapabilities(true, true),
		server.WithLogging(),
		server.WithToolHandlerMiddleware(authMiddleware.AuthMiddleware),
	)

	// Register tools from ToolList
	for _, tool := range ToolList {
		s.AddTool(mcp.NewTool(tool.Name, mcp.WithDescription(tool.Description)), dummyHandler)
	}

	return s
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
	// Handle static file requests
	if r.URL.Path == "/static/" || strings.HasPrefix(r.URL.Path, "/static/") {
		handleStaticFiles(w, r)
		return
	}

	// Handle MCP stream requests
	if strings.HasPrefix(r.URL.Path, "/mcp/") {
		streamableServer := server.NewStreamableHTTPServer(mcpServer,
			server.WithEndpointPath("/stream"),
		)
		streamableServer.ServeHTTP(w, r)
		return
	}

	// Handle auth endpoints
	switch r.URL.Path {
	case "/mockWebPage":
		webPageHandler(w, r)
	case "/login":
		loginHandler(w, r)
	default:
		// Root handler - provide basic info about the MCP server
		if r.URL.Path == "/" || r.URL.Path == "" {
			w.Header().Set("Content-Type", "application/json")
			functionURL := r.Header.Get("X-Forwarded-Proto") + "://" + r.Host
			response := fmt.Sprintf(`{
				"status": "ok",
				"service": "Fi MCP Server",
				"version": "1.0.0",
				"description": "Financial data MCP server for Fi Money platform",
				"endpoints": {
					"mcp_stream": "%s/mcp/stream",
					"login_page": "%s/mockWebPage?sessionId=YOUR_SESSION_ID",
					"login_endpoint": "%s/login"
				},
				"allowed_phone_numbers": %d,
				"instructions": "Use the MCP stream endpoint to connect via MCP client. Authentication required via login page."
			}`, functionURL, functionURL, functionURL, len(GetAllowedMobileNumbers()))
			fmt.Fprint(w, response)
		} else {
			http.NotFound(w, r)
		}
	}
}

func handleStaticFiles(w http.ResponseWriter, r *http.Request) {
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

func dummyHandler(_ context.Context, _ mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	return mcp.NewToolResultText("dummy handler"), nil
}

func webPageHandler(w http.ResponseWriter, r *http.Request) {
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
		AllowedMobileNumbers: GetAllowedMobileNumbers(),
	}

	err = tmpl.Execute(w, data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
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

	authMiddleware.AddSession(sessionId, phoneNumber)

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
