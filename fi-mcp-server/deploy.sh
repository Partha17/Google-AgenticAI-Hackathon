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

# Check if PROJECT_ID is set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo "❌ Please set PROJECT_ID environment variable to your actual GCP project ID"
    echo "   Example: export PROJECT_ID=my-gcp-project"
    exit 1
fi

# Set project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com

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
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FUNCTION_URL")
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "404" ]; then
    echo "   ✅ Health check passed (HTTP $HTTP_CODE)"
else
    echo "   ❌ Health check failed (HTTP $HTTP_CODE)"
fi

echo ""
echo "📝 Next steps:"
echo "   1. Test the MCP endpoint with a client"
echo "   2. Use one of the test phone numbers for authentication"
echo "   3. Monitor logs: gcloud functions logs tail $FUNCTION_NAME --region=$REGION" 