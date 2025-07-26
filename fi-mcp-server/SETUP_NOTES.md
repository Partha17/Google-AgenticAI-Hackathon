# Setup Notes for Cloud Functions Deployment

## Quick Fix for Dependency Issues

After creating the `function.go` file, you need to update dependencies and fix imports:

1. **Update Go modules:**
   ```bash
   cd fi-mcp-server
   go mod tidy
   ```

2. **Alternative approach (if function.go conflicts with main.go):**
   
   Instead of using `function.go` alongside `main.go`, you can rename the files:
   
   ```bash
   # Rename existing main.go for local development
   mv main.go main_local.go
   
   # Rename function.go to main.go for Cloud Functions
   mv function.go main.go
   ```

3. **For local development vs Cloud Functions:**
   
   You can maintain two entry points:
   - `main_local.go` - for local development with `go run main_local.go`
   - `main.go` - for Cloud Functions deployment
   
   Switch between them as needed:
   ```bash
   # For local development
   cp main_local.go main.go
   go run main.go
   
   # For Cloud Functions deployment
   cp function.go main.go
   ./deploy.sh
   ```

4. **Quick deployment without conflicts:**
   
   Create a separate branch for Cloud Functions:
   ```bash
   git checkout -b cloud-functions-deploy
   mv main.go main_local.go
   mv function.go main.go
   git add -A
   git commit -m "Prepare for Cloud Functions deployment"
   ```

## Files Created

The deployment package includes:

- `DEPLOYMENT_GCLOUD_FUNCTIONS.md` - Complete deployment guide
- `function.go` - Cloud Functions entry point (rename to main.go for deployment)
- `.env.yaml` - Environment configuration
- `.gcloudignore` - Deployment ignore file
- `deploy.sh` - Automated deployment script
- `test-deployment.sh` - Deployment testing script
- `cloudbuild.yaml` - CI/CD configuration

## Quick Start

1. Set your GCP project ID:
   ```bash
   export PROJECT_ID="your-actual-project-id"
   ```

2. Make deploy script executable:
   ```bash
   chmod +x deploy.sh test-deployment.sh
   ```

3. Deploy:
   ```bash
   ./deploy.sh
   ```

The deployment guide contains complete instructions for production setup, monitoring, and troubleshooting. 