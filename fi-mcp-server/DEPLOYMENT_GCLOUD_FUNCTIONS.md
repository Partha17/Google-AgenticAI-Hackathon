# Fi MCP Server - Google Cloud Functions Deployment Guide

This guide walks you through deploying the Fi MCP server to Google Cloud Functions, enabling scalable and serverless execution of your financial data MCP server.

## Prerequisites

### 1. Google Cloud Setup
- **Google Cloud Account**: Active GCP account with billing enabled
- **Google Cloud CLI**: Install and configure `gcloud` CLI ([Installation Guide](https://cloud.google.com/sdk/docs/install))
- **Project**: Create or select a GCP project
- **APIs**: Enable required APIs:
  ```bash
  gcloud services enable cloudfunctions.googleapis.com
  gcloud services enable cloudbuild.googleapis.com
  gcloud services enable artifactregistry.googleapis.com
  ```

### 2. Local Development Setup
- **Go**: Version 1.23 or later
- **Docker**: For local testing (optional but recommended)

## Architecture Changes for Cloud Functions

Google Cloud Functions require specific adaptations from the standard HTTP server:

### 1. Entry Point Modification

Create a new file `function.go` for the Cloud Functions entry point:

```go
package main

import (
	"context"
	"embed"
	"fmt"
	"html/template"
	"io/fs"
	"log"
	"net/http"
	"os"

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

var authMiddleware *middlewares.AuthMiddleware
var mcpServer *server.Server

func init() {
	authMiddleware = middlewares.NewAuthMiddleware()
	mcpServer = setupMCPServer()
	
	// Register the Cloud Function
	functions.HTTP("FiMCPFunction", handleRequest)
}

func setupMCPServer() *server.Server {
	s := server.NewMCPServer(
		"Hackathon MCP",
		"0.1.0",
		server.WithInstructions("A financial portfolio management MCP server that provides secure access to users' financial data through Fi Money, a financial hub for all things money. This MCP server enables users to:\n- Access comprehensive net worth analysis with asset/liability breakdowns\n- Retrieve detailed transaction histories for mutual funds and Employee Provident Fund accounts\n- View credit reports with scores, loan details, and account histories, this also contains user's date of birth that can be used for calculating their age\n\nIf the person asks, you can tell about Fi Money that it is money management platform that offers below services in partnership with regulated entities:\n\nAVAILABLE SERVICES:\n- Digital savings account with zero Forex cards\n- Invest in Indian Mutual funds, US Stocks (partnership with licensed brokers), Smart and Fixed Deposits.\n- Instant Personal Loans \n- Faster UPI and Bank Transfers payments\n- Credit score monitoring and reports\n\nIMPORTANT LIMITATIONS:\n- This MCP server retrieves only actual user data via Net worth tracker and based on consent provided by the user  and does not generate hypothetical or estimated financial information\n- In this version of the MCP server, user's historical bank transactions, historical stocks transaction data, salary (unless categorically declared) is not present. Don't assume these data points for any kind of analysis.\n\nCRITICAL INSTRUCTIONS FOR FINANCIAL DATA:\n\n1. DATA BOUNDARIES: Only provide information that exists in the user's Fi Money Net worth tracker. Never estimate, extrapolate, or generate hypothetical financial data.\n\n2. SPENDING ANALYSIS: If user asks about spending patterns, categories, or analysis tell the user we currently don't offer that data through the MCP:\n   - For detailed spending insights, direct them to: \"For comprehensive spending analysis and categorization, please use the Fi Money mobile app which provides detailed spending insights and budgeting tools.\"\n\n3. MISSING DATA HANDLING: If requested data is not available:\n   - Clearly state what data is missing\n   - Explain how user can connect additional accounts in Fi Money app\n   - Never fill gaps with estimated or generic information\n"),
		server.WithToolCapabilities(true),
		server.WithResourceCapabilities(true, true),
		server.WithLogging(),
		server.WithToolHandlerMiddleware(authMiddleware.AuthMiddleware),
	)

	// Register tools from pkg.ToolList
	for _, tool := range pkg.ToolList {
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
		http.NotFound(w, r)
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
		AllowedMobileNumbers: pkg.GetAllowedMobileNumbers(),
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
```

### 2. Update go.mod for Cloud Functions

Add the Functions Framework dependency:

```go
module github.com/epifi/fi-mcp-lite

go 1.23

toolchain go1.24.2

require (
	github.com/GoogleCloudPlatform/functions-framework-go v1.8.1
	github.com/mark3labs/mcp-go v0.33.0
	github.com/samber/lo v1.51.0
)

require (
	github.com/google/uuid v1.6.0 // indirect
	github.com/spf13/cast v1.7.1 // indirect
	github.com/yosida95/uritemplate/v3 v3.0.2 // indirect
	golang.org/x/text v0.22.0 // indirect
)
```

### 3. Update Package Dependencies

Update the `pkg` files to work with embedded filesystems. Modify `pkg/allowed_phone_numbers.go`:

```go
package pkg

import (
	"embed"
	"io/fs"
	"log"
)

//go:embed ../test_data_dir/*
var testDataFiles embed.FS

func GetAllowedMobileNumbers() []string {
	entries, err := fs.ReadDir(testDataFiles, "test_data_dir")
	if err != nil {
		log.Printf("Error reading test data directories: %v", err)
		return []string{}
	}

	var phoneNumbers []string
	for _, entry := range entries {
		if entry.IsDir() {
			phoneNumbers = append(phoneNumbers, entry.Name())
		}
	}
	return phoneNumbers
}
```

## Deployment Configuration

### 1. Create `.gcloudignore` file

```
# Ignore development files
.git/
.gitignore
*.md
node_modules/
venv/
__pycache__/

# Keep only necessary files
!go.mod
!go.sum
!*.go
!static/
!test_data_dir/
```

### 2. Create `cloudbuild.yaml` (Optional - for CI/CD)

```yaml
steps:
  # Build the function
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'functions'
      - 'deploy'
      - 'fi-mcp-function'
      - '--gen2'
      - '--runtime=go123'
      - '--region=${_REGION}'
      - '--source=.'
      - '--entry-point=FiMCPFunction'
      - '--trigger=http'
      - '--allow-unauthenticated'
      - '--memory=512Mi'
      - '--timeout=300s'
      - '--max-instances=10'
      - '--set-env-vars=FI_MCP_PORT=8080'

substitutions:
  _REGION: 'us-central1'

options:
  logging: CLOUD_LOGGING_ONLY
```

### 3. Environment Configuration

Create `.env.yaml` for environment variables:

```yaml
FI_MCP_PORT: "8080"
LOG_LEVEL: "info"
ENVIRONMENT: "production"
```

## Deployment Steps

### 1. Prepare the Project

```bash
# Navigate to the fi-mcp-server directory
cd fi-mcp-server

# Update dependencies
go mod tidy

# Test locally (optional)
export FI_MCP_PORT=8080
go run function.go
```

### 2. Set Up Google Cloud Project

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
export REGION="us-central1"

# Configure gcloud
gcloud config set project $PROJECT_ID
gcloud config set functions/region $REGION

# Authenticate (if not already done)
gcloud auth login
gcloud auth application-default login
```

### 3. Deploy to Cloud Functions

```bash
# Deploy the function
gcloud functions deploy fi-mcp-function \
    --gen2 \
    --runtime=go123 \
    --region=$REGION \
    --source=. \
    --entry-point=FiMCPFunction \
    --trigger=http \
    --allow-unauthenticated \
    --memory=512Mi \
    --timeout=300s \
    --max-instances=10 \
    --env-vars-file=.env.yaml
```

### 4. Alternative: Deploy with Custom Domain (Optional)

```bash
# Deploy with custom domain mapping
gcloud functions deploy fi-mcp-function \
    --gen2 \
    --runtime=go123 \
    --region=$REGION \
    --source=. \
    --entry-point=FiMCPFunction \
    --trigger=http \
    --allow-unauthenticated \
    --memory=1Gi \
    --timeout=300s \
    --max-instances=50 \
    --env-vars-file=.env.yaml \
    --ingress-settings=all

# Map to custom domain (requires domain verification)
gcloud functions add-iam-policy-binding fi-mcp-function \
    --region=$REGION \
    --member="allUsers" \
    --role="roles/cloudfunctions.invoker"
```

## Deployment Scripts

### 1. Create `deploy.sh`

```bash
#!/bin/bash

set -e

# Configuration
PROJECT_ID=${PROJECT_ID:-"your-project-id"}
REGION=${REGION:-"us-central1"}
FUNCTION_NAME="fi-mcp-function"

echo "🚀 Deploying Fi MCP Server to Google Cloud Functions..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Check if authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud. Please run 'gcloud auth login'"
    exit 1
fi

# Set project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Update dependencies
echo "📦 Updating Go dependencies..."
go mod tidy

# Deploy function
echo "🚀 Deploying function..."
gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime=go123 \
    --region=$REGION \
    --source=. \
    --entry-point=FiMCPFunction \
    --trigger=http \
    --allow-unauthenticated \
    --memory=512Mi \
    --timeout=300s \
    --max-instances=10 \
    --env-vars-file=.env.yaml

# Get function URL
FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME --region=$REGION --format="value(serviceConfig.uri)")

echo "✅ Deployment successful!"
echo "🌐 Function URL: $FUNCTION_URL"
echo "📊 MCP Endpoint: $FUNCTION_URL/mcp/stream"
echo "🔐 Login Page: $FUNCTION_URL/mockWebPage?sessionId=your-session-id"

# Test the deployment
echo "🧪 Testing deployment..."
curl -s -o /dev/null -w "%{http_code}" "$FUNCTION_URL" && echo " - Health check passed" || echo " - Health check failed"
```

### 2. Create `test-deployment.sh`

```bash
#!/bin/bash

FUNCTION_URL=$1

if [ -z "$FUNCTION_URL" ]; then
    echo "Usage: $0 <function-url>"
    echo "Example: $0 https://your-region-your-project.cloudfunctions.net/fi-mcp-function"
    exit 1
fi

echo "🧪 Testing Fi MCP Function deployment..."

# Test health endpoint
echo "1. Testing health endpoint..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FUNCTION_URL")
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "404" ]; then
    echo "   ✅ Function is responding (HTTP $HTTP_CODE)"
else
    echo "   ❌ Function not responding (HTTP $HTTP_CODE)"
    exit 1
fi

# Test MCP endpoint
echo "2. Testing MCP endpoint..."
MCP_RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "Mcp-Session-Id: test-session-123" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
    "$FUNCTION_URL/mcp/stream")

if echo "$MCP_RESPONSE" | grep -q "tools"; then
    echo "   ✅ MCP endpoint is working"
else
    echo "   ❌ MCP endpoint not working"
    echo "   Response: $MCP_RESPONSE"
fi

# Test static files
echo "3. Testing static files..."
STATIC_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FUNCTION_URL/static/fi_qr.png")
if [ "$STATIC_CODE" = "200" ]; then
    echo "   ✅ Static files are served correctly"
else
    echo "   ❌ Static files not accessible (HTTP $STATIC_CODE)"
fi

echo "🎉 Deployment test completed!"
```

## Configuration Options

### Resource Configuration

For different workloads, adjust these parameters:

```bash
# Development/Testing
--memory=256Mi
--timeout=60s
--max-instances=5

# Production - Light Load
--memory=512Mi
--timeout=300s
--max-instances=10

# Production - Heavy Load
--memory=1Gi
--timeout=540s
--max-instances=100
--min-instances=1
```

### Security Configuration

```bash
# Private function (requires authentication)
gcloud functions deploy fi-mcp-function \
    --trigger=http \
    --no-allow-unauthenticated

# Add IAM bindings for specific users
gcloud functions add-iam-policy-binding fi-mcp-function \
    --region=$REGION \
    --member="user:user@example.com" \
    --role="roles/cloudfunctions.invoker"
```

## Monitoring and Troubleshooting

### 1. View Logs

```bash
# Real-time logs
gcloud functions logs tail fi-mcp-function --region=$REGION

# Historical logs
gcloud functions logs read fi-mcp-function --region=$REGION --limit=50
```

### 2. Function Metrics

```bash
# Get function info
gcloud functions describe fi-mcp-function --region=$REGION

# View metrics in Cloud Console
echo "Visit: https://console.cloud.google.com/functions/details/$REGION/fi-mcp-function"
```

### 3. Common Issues and Solutions

#### Issue: Function timeout
```bash
# Increase timeout
gcloud functions deploy fi-mcp-function \
    --timeout=540s \
    --update-only
```

#### Issue: Memory errors
```bash
# Increase memory
gcloud functions deploy fi-mcp-function \
    --memory=1Gi \
    --update-only
```

#### Issue: Cold start performance
```bash
# Set minimum instances
gcloud functions deploy fi-mcp-function \
    --min-instances=1 \
    --update-only
```

### 4. Enable Detailed Monitoring

```bash
# Enable Cloud Monitoring
gcloud services enable monitoring.googleapis.com

# Create uptime check
gcloud alpha monitoring uptime create-http \
    --display-name="Fi MCP Function Health" \
    --hostname="your-region-your-project.cloudfunctions.net" \
    --path="/fi-mcp-function"
```

## Cost Optimization

### 1. Optimize Resource Usage

- **Memory**: Start with 256Mi, increase only if needed
- **Timeout**: Set to the minimum required (default: 60s)
- **Max instances**: Limit based on expected load
- **Min instances**: Use 0 for cost savings (accept cold starts)

### 2. Use Cloud Scheduler for Keep-Alive (Optional)

```bash
# Create a job to ping the function every 5 minutes
gcloud scheduler jobs create http fi-mcp-keepalive \
    --schedule="*/5 * * * *" \
    --uri="https://your-region-your-project.cloudfunctions.net/fi-mcp-function" \
    --http-method=GET \
    --description="Keep Fi MCP function warm"
```

## Security Best Practices

### 1. Environment Variables

Store sensitive data in Secret Manager:

```bash
# Create secret
echo -n "your-secret-value" | gcloud secrets create fi-mcp-secret --data-file=-

# Deploy with secret
gcloud functions deploy fi-mcp-function \
    --set-secrets="SECRET_KEY=fi-mcp-secret:latest"
```

### 2. VPC Configuration (Optional)

For additional security, deploy in a VPC:

```bash
gcloud functions deploy fi-mcp-function \
    --vpc-connector=projects/$PROJECT_ID/locations/$REGION/connectors/your-connector \
    --egress-settings=private-ranges-only
```

### 3. Custom Service Account

```bash
# Create service account
gcloud iam service-accounts create fi-mcp-sa \
    --description="Fi MCP Function Service Account"

# Deploy with custom service account
gcloud functions deploy fi-mcp-function \
    --service-account="fi-mcp-sa@$PROJECT_ID.iam.gserviceaccount.com"
```

## Maintenance and Updates

### 1. Update Function

```bash
# Update code only
gcloud functions deploy fi-mcp-function \
    --source=. \
    --update-only

# Update environment variables
gcloud functions deploy fi-mcp-function \
    --update-env-vars="NEW_VAR=value" \
    --update-only
```

### 2. Rollback

```bash
# List function versions
gcloud functions versions list --filter="name~fi-mcp-function"

# Rollback to previous version
gcloud functions deploy fi-mcp-function \
    --source-url="gs://gcf-sources-bucket/path-to-previous-version.zip"
```

### 3. Blue-Green Deployment

```bash
# Deploy new version with traffic split
gcloud functions deploy fi-mcp-function-v2 \
    --source=. \
    --trigger=http

# Update traffic allocation
gcloud functions set-traffic fi-mcp-function \
    --splits="v1=50,v2=50"
```

## Conclusion

This guide provides a complete deployment strategy for the Fi MCP server on Google Cloud Functions. The serverless approach offers:

- **Scalability**: Automatic scaling based on demand
- **Cost-effectiveness**: Pay only for actual usage
- **Maintenance**: Reduced operational overhead
- **Security**: Built-in security features

For production deployments, consider implementing:
- CI/CD pipelines with Cloud Build
- Comprehensive monitoring and alerting
- Multi-region deployment for high availability
- Custom domain mapping for branded URLs

For support and troubleshooting, refer to the [Google Cloud Functions documentation](https://cloud.google.com/functions/docs) and monitor the function logs regularly. 