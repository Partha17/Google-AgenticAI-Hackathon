#!/bin/bash

set -e

# Configuration
PROJECT_ID=${PROJECT_ID:-"fi-mcp-server-1753543657"}
REGION=${REGION:-"us-central1"}
SERVICE_NAME="fi-financial-dashboard"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Versioning configuration
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
VERSION="${TIMESTAMP}-${GIT_COMMIT}"
REVISION_NAME="${SERVICE_NAME}-${VERSION}"
# Create a valid tag for Cloud Run (no underscores, lowercase, must start with letter)
TAG_NAME="v$(echo "$VERSION" | tr '_' '-' | tr '[:upper:]' '[:lower:]')"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        log_error "gcloud CLI not found. Please install Google Cloud SDK first."
        exit 1
    fi
    
    # Check authentication
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        log_error "Not authenticated. Please run 'gcloud auth login'"
        exit 1
    fi
    
    # Check if git is available
    if ! command -v git &> /dev/null; then
        log_warning "Git not found. Using timestamp only for versioning."
    fi
    
    log_success "Prerequisites check passed"
}

# Function to enable required APIs
enable_apis() {
    log_info "Enabling required APIs..."
    gcloud services enable \
        cloudbuild.googleapis.com \
        run.googleapis.com \
        containerregistry.googleapis.com \
        artifactregistry.googleapis.com \
        cloudresourcemanager.googleapis.com
    log_success "APIs enabled"
}

# Function to build and tag image
build_image() {
    log_info "Building container image with version $VERSION..."
    
    # Build the image with version tag and build args
    gcloud builds submit \
        --substitutions=_IMAGE_NAME="$IMAGE_NAME",_APP_VERSION="$VERSION",_BUILD_TIMESTAMP="$TIMESTAMP",_GIT_COMMIT="$GIT_COMMIT"
    
    log_success "Image built and tagged as ${IMAGE_NAME}:${VERSION}"
}

# Function to deploy with versioning
deploy_versioned() {
    log_info "Deploying version $VERSION to Cloud Run..."
    
    # Deploy the new revision
    gcloud run deploy $SERVICE_NAME \
        --image "${IMAGE_NAME}:${VERSION}" \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --port 8080 \
        --memory 2Gi \
        --cpu 1 \
        --timeout 300 \
        --max-instances 10 \
        --set-env-vars "LOG_LEVEL=INFO,GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_LOCATION=$REGION,MCP_SERVER_URL=https://fi-mcp-server-bpzxyhr4dq-uc.a.run.app,APP_VERSION=$VERSION" \
        --tag $TAG_NAME
    
    log_success "Deployment completed for version $VERSION"
}

# Function to get service URL
get_service_url() {
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
    echo $SERVICE_URL
}

# Function to test deployment
test_deployment() {
    local url=$1
    log_info "Testing deployment..."
    
    # Wait a bit for the service to be ready
    sleep 10
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$url" || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        log_success "Health check passed"
        return 0
    else
        log_warning "Health check returned HTTP $HTTP_CODE (may take a few minutes to fully start)"
        return 1
    fi
}

# Function to list all revisions
list_revisions() {
    log_info "Listing all revisions for $SERVICE_NAME..."
    gcloud run revisions list --service=$SERVICE_NAME --region=$REGION --format="table(metadata.name,status.conditions[0].status,metadata.creationTimestamp,spec.template.metadata.annotations.run.googleapis.com/execution-environment)"
}

# Function to rollback to a specific revision
rollback_to_revision() {
    local revision_name=$1
    log_info "Rolling back to revision: $revision_name"
    
    # Get the image from the specified revision
    local image_url=$(gcloud run revisions describe $revision_name --region=$REGION --format="value(spec.template.spec.containers[0].image)")
    
    # Deploy using that image
    gcloud run deploy $SERVICE_NAME \
        --image "$image_url" \
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
    
    log_success "Rollback completed to revision: $revision_name"
}

# Function to show deployment history
show_deployment_history() {
    log_info "Deployment history for $SERVICE_NAME:"
    echo ""
    gcloud run revisions list --service=$SERVICE_NAME --region=$REGION --format="table(metadata.name,status.conditions[0].status,metadata.creationTimestamp,spec.template.metadata.annotations.run.googleapis.com/execution-environment)" --sort-by=~metadata.creationTimestamp
}

# Function to clean up old revisions (keep last 10)
cleanup_old_revisions() {
    log_info "Cleaning up old revisions (keeping last 10)..."
    
    # Get all revisions sorted by creation time (newest first)
    local revisions=$(gcloud run revisions list --service=$SERVICE_NAME --region=$REGION --format="value(metadata.name)" --sort-by=~metadata.creationTimestamp)
    
    # Count total revisions
    local total_revisions=$(echo "$revisions" | wc -l)
    
    if [ "$total_revisions" -gt 10 ]; then
        # Skip the first 10 (newest) and delete the rest
        local to_delete=$(echo "$revisions" | tail -n +11)
        
        for revision in $to_delete; do
            log_info "Deleting old revision: $revision"
            gcloud run revisions delete $revision --region=$REGION --quiet
        done
        
        log_success "Cleanup completed. Kept 10 most recent revisions."
    else
        log_info "No cleanup needed. Only $total_revisions revisions exist."
    fi
}

# Main deployment function
main_deploy() {
    echo "🚀 Deploying Fi Financial AI Dashboard to Google Cloud Run with Versioning"
    echo "Project: $PROJECT_ID"
    echo "Region: $REGION"
    echo "Service: $SERVICE_NAME"
    echo "Version: $VERSION"
    echo ""
    
    # Set project
    log_info "Setting project to $PROJECT_ID..."
    gcloud config set project $PROJECT_ID
    
    # Run deployment steps
    check_prerequisites
    enable_apis
    build_image
    deploy_versioned
    
    # Get service URL and test
    SERVICE_URL=$(get_service_url)
    log_success "Deployment successful!"
    echo "🌐 Service URL: $SERVICE_URL"
    echo "📊 Dashboard: $SERVICE_URL"
    
    # Test the deployment
    if test_deployment "$SERVICE_URL"; then
        log_success "Deployment is healthy!"
    else
        log_warning "Deployment may still be starting up..."
    fi
    
    # Show deployment info
    echo ""
    echo "📝 Deployment Information:"
    echo "   Version: $VERSION"
    echo "   Image: ${IMAGE_NAME}:${VERSION}"
    echo "   Revision: $REVISION_NAME"
    echo ""
    echo "🔄 Rollback Commands:"
    echo "   List revisions: ./deploy-cloud-run-versioned.sh list"
    echo "   Rollback: ./deploy-cloud-run-versioned.sh rollback <revision-name>"
    echo "   History: ./deploy-cloud-run-versioned.sh history"
    echo "   Cleanup: ./deploy-cloud-run-versioned.sh cleanup"
    echo ""
    echo "📊 Monitoring:"
    echo "   Logs: gcloud logs tail $SERVICE_NAME --region=$REGION"
    echo "   Metrics: gcloud run services describe $SERVICE_NAME --region=$REGION"
}

# Command line argument handling
case "${1:-deploy}" in
    "deploy")
        main_deploy
        ;;
    "list")
        list_revisions
        ;;
    "rollback")
        if [ -z "$2" ]; then
            log_error "Please provide a revision name to rollback to"
            echo "Usage: $0 rollback <revision-name>"
            echo "Use '$0 list' to see available revisions"
            exit 1
        fi
        rollback_to_revision "$2"
        ;;
    "history")
        show_deployment_history
        ;;
    "cleanup")
        cleanup_old_revisions
        ;;
    "test")
        SERVICE_URL=$(get_service_url)
        test_deployment "$SERVICE_URL"
        ;;
    *)
        echo "Usage: $0 [deploy|list|rollback|history|cleanup|test]"
        echo ""
        echo "Commands:"
        echo "  deploy    - Deploy new version (default)"
        echo "  list      - List all revisions"
        echo "  rollback  - Rollback to specific revision"
        echo "  history   - Show deployment history"
        echo "  cleanup   - Clean up old revisions (keep last 10)"
        echo "  test      - Test current deployment"
        exit 1
        ;;
esac 