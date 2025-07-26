#!/bin/bash

set -e

# Configuration
PROJECT_ID=${PROJECT_ID:-"fi-mcp-server-1753543657"}
REGION=${REGION:-"us-central1"}
SERVICE_NAME="fi-financial-dashboard"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying Fi Financial AI Dashboard to Google Cloud Run"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"

# Check if gcloud is installed and authenticated
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install Google Cloud SDK first."
    exit 1
fi

# Check authentication
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated. Please run 'gcloud auth login'"
    exit 1
fi

# Set project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com \
    artifactregistry.googleapis.com

# Build the container image
echo "🔨 Building container image..."
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars "LOG_LEVEL=INFO,GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_LOCATION=$REGION"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo "✅ Deployment successful!"
echo "🌐 Service URL: $SERVICE_URL"
echo "📊 Dashboard: $SERVICE_URL"

# Test the deployment
echo "🧪 Testing deployment..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL" || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ Health check passed"
else
    echo "   ⚠️  Health check returned HTTP $HTTP_CODE (may take a few minutes to fully start)"
fi

echo ""
echo "📝 Next steps:"
echo "   1. Set up your Google API key in environment variables"
echo "   2. Configure any additional environment variables needed"
echo "   3. Monitor logs: gcloud logs tail $SERVICE_NAME --region=$REGION"
echo "   4. Access your financial dashboard at: $SERVICE_URL" 