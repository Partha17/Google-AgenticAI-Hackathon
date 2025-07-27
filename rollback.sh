#!/bin/bash

# Quick rollback script for Fi Financial Dashboard
# Usage: ./rollback.sh [revision-name]

set -e

PROJECT_ID=${PROJECT_ID:-"fi-mcp-server-1753543657"}
REGION=${REGION:-"us-central1"}
SERVICE_NAME="fi-financial-dashboard"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔄 Fi Financial Dashboard Rollback Tool${NC}"
echo ""

if [ -z "$1" ]; then
    echo -e "${YELLOW}Available revisions:${NC}"
    echo ""
    gcloud run revisions list --service=$SERVICE_NAME --region=$REGION \
        --format="table(metadata.name,status.conditions[0].status,metadata.creationTimestamp)" \
        --sort-by=~metadata.creationTimestamp
    
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./rollback.sh <revision-name>"
    echo ""
    echo -e "${YELLOW}Example:${NC}"
    echo "  ./rollback.sh fi-financial-dashboard-20241227-143022-ad61d10"
    exit 1
fi

REVISION_NAME=$1

echo -e "${BLUE}Rolling back to revision: ${YELLOW}$REVISION_NAME${NC}"
echo ""

# Verify the revision exists
if ! gcloud run revisions describe $REVISION_NAME --region=$REGION >/dev/null 2>&1; then
    echo -e "${RED}❌ Revision '$REVISION_NAME' not found!${NC}"
    echo ""
    echo -e "${YELLOW}Available revisions:${NC}"
    gcloud run revisions list --service=$SERVICE_NAME --region=$REGION \
        --format="table(metadata.name,status.conditions[0].status,metadata.creationTimestamp)" \
        --sort-by=~metadata.creationTimestamp
    exit 1
fi

# Get the image from the specified revision
echo -e "${BLUE}Getting image from revision...${NC}"
IMAGE_URL=$(gcloud run revisions describe $REVISION_NAME --region=$REGION --format="value(spec.template.spec.containers[0].image)")

echo -e "${BLUE}Image: ${YELLOW}$IMAGE_URL${NC}"
echo ""

# Confirm rollback
echo -e "${YELLOW}⚠️  Are you sure you want to rollback to this revision? (y/N)${NC}"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Rollback cancelled.${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}🔄 Starting rollback...${NC}"

# Deploy using that image
gcloud run deploy $SERVICE_NAME \
    --image "$IMAGE_URL" \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars "LOG_LEVEL=INFO,GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_LOCATION=$REGION,MCP_SERVER_URL=https://fi-mcp-server-bpzxyhr4dq-uc.a.run.app" \
    --tag "rollback-$(date +%Y%m%d-%H%M%S)"

echo ""
echo -e "${GREEN}✅ Rollback completed successfully!${NC}"
echo ""

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
echo -e "${BLUE}🌐 Service URL: ${YELLOW}$SERVICE_URL${NC}"
echo ""

# Test the deployment
echo -e "${BLUE}🧪 Testing deployment...${NC}"
sleep 10
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL" || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${YELLOW}⚠️  Health check returned HTTP $HTTP_CODE (may take a few minutes to fully start)${NC}"
fi

echo ""
echo -e "${BLUE}📊 Monitoring commands:${NC}"
echo "  Logs: gcloud logs tail $SERVICE_NAME --region=$REGION"
echo "  Status: gcloud run services describe $SERVICE_NAME --region=$REGION" 