#!/bin/bash

set -e

# Configuration
PROJECT_ID=${PROJECT_ID:-"your-project-id"}
REGION=${REGION:-"us-central1"}
SERVICE_NAME="fi-mcp-server"
IMAGE_NAME="gcr.io/$PROJECT_ID/fi-mcp-server"

echo "🚀 Deploying Fi MCP Server to Google Cloud Run..."

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

echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

echo "🔧 Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

echo "🐳 Building Docker image..."
gcloud builds submit --tag $IMAGE_NAME

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 512Mi \
    --timeout 300 \
    --max-instances 10 \
    --port 8080

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo "✅ Deployment successful!"
echo "🌐 Service URL: $SERVICE_URL"
echo "📊 MCP Endpoint: $SERVICE_URL/mcp"
echo "🧪 Test Data: $SERVICE_URL/mcp/test?phone=1111111111"
echo "🔐 Login Page: $SERVICE_URL/mockWebPage?sessionId=test-session"
echo "🔑 Auth Endpoint: $SERVICE_URL/auth"

# Test the deployment
echo "🧪 Testing deployment..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL")
if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ Health check passed (HTTP $HTTP_CODE)"
else
    echo "   ❌ Health check failed (HTTP $HTTP_CODE)"
fi

echo ""
echo "📝 Next steps:"
echo "   1. Test authentication: curl -X POST $SERVICE_URL/auth -H 'Content-Type: application/json' -d '{\"phoneNumber\":\"1111111111\"}'"
echo "   2. Get test data: curl '$SERVICE_URL/mcp/test?phone=1111111111'"
echo "   3. Monitor logs: gcloud run logs tail $SERVICE_NAME --region=$REGION" 