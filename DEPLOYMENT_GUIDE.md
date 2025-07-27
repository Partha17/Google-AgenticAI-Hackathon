# 🚀 Fi Financial Dashboard - Versioned Deployment Guide

This guide explains how to deploy the Fi Financial Dashboard to Google Cloud Run with versioning and rollback capabilities.

## 📋 Prerequisites

1. **Google Cloud SDK** installed and configured
2. **gcloud CLI** authenticated with your project
3. **Git** repository with your code
4. **Docker** (optional, Cloud Build will handle containerization)

## 🔧 Configuration

### Environment Variables
Set these environment variables or modify the scripts:

```bash
export PROJECT_ID="fi-mcp-server-1753543657"
export REGION="us-central1"
export SERVICE_NAME="fi-financial-dashboard"
```

### Google Cloud APIs Required
The deployment script will automatically enable these APIs:
- `cloudbuild.googleapis.com`
- `run.googleapis.com`
- `containerregistry.googleapis.com`
- `artifactregistry.googleapis.com`
- `cloudresourcemanager.googleapis.com`

## 🚀 Deployment Commands

### 1. Deploy New Version
```bash
# Deploy with automatic versioning
./deploy-cloud-run-versioned.sh deploy

# Or simply (deploy is the default)
./deploy-cloud-run-versioned.sh
```

### 2. List All Revisions
```bash
./deploy-cloud-run-versioned.sh list
```

### 3. Show Deployment History
```bash
./deploy-cloud-run-versioned.sh history
```

### 4. Test Current Deployment
```bash
./deploy-cloud-run-versioned.sh test
```

### 5. Clean Up Old Revisions
```bash
# Keeps the last 10 revisions, deletes older ones
./deploy-cloud-run-versioned.sh cleanup
```

## 🔄 Rollback Operations

### Using the Main Script
```bash
# Rollback to a specific revision
./deploy-cloud-run-versioned.sh rollback <revision-name>

# Example:
./deploy-cloud-run-versioned.sh rollback fi-financial-dashboard-20241227-143022-ad61d10
```

### Using the Quick Rollback Script
```bash
# Show available revisions and rollback
./rollback.sh

# Rollback to specific revision
./rollback.sh <revision-name>
```

## 📊 Versioning System

### Version Format
Versions are automatically generated using the format:
```
YYYYMMDD-HHMMSS-<git-commit-hash>
```

Example: `20241227-143022-ad61d10`

### Version Information
Each deployment includes:
- **Timestamp**: When the deployment was created
- **Git Commit**: Short hash of the current commit
- **Build Info**: Embedded in the container image
- **Environment Variables**: `APP_VERSION`, `BUILD_TIMESTAMP`, `GIT_COMMIT`

### Image Tags
- **Versioned**: `gcr.io/PROJECT_ID/SERVICE_NAME:VERSION`
- **Latest**: `gcr.io/PROJECT_ID/SERVICE_NAME:latest`
- **Rollback**: `gcr.io/PROJECT_ID/SERVICE_NAME:rollback-TIMESTAMP`

## 🔍 Monitoring and Debugging

### View Logs
```bash
# Real-time logs
gcloud logs tail $SERVICE_NAME --region=$REGION

# Recent logs
gcloud logs read $SERVICE_NAME --region=$REGION --limit=50
```

### Service Status
```bash
# Service details
gcloud run services describe $SERVICE_NAME --region=$REGION

# Service URL
gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)"
```

### Revision Details
```bash
# List all revisions
gcloud run revisions list --service=$SERVICE_NAME --region=$REGION

# Get specific revision details
gcloud run revisions describe <revision-name> --region=$REGION
```

## 🛠️ Advanced Operations

### Manual Rollback Process
If you need to manually rollback:

1. **List available revisions**:
   ```bash
   gcloud run revisions list --service=$SERVICE_NAME --region=$REGION
   ```

2. **Get the image from the target revision**:
   ```bash
   gcloud run revisions describe <revision-name> --region=$REGION --format="value(spec.template.spec.containers[0].image)"
   ```

3. **Deploy using that image**:
   ```bash
   gcloud run deploy $SERVICE_NAME \
     --image "<image-url>" \
     --platform managed \
     --region $REGION \
     --allow-unauthenticated \
     --port 8080 \
     --memory 2Gi \
     --cpu 1 \
     --timeout 300 \
     --max-instances 10
   ```

### Environment Variable Management
To update environment variables:

```bash
gcloud run services update $SERVICE_NAME \
  --region=$REGION \
  --set-env-vars "NEW_VAR=value,ANOTHER_VAR=value"
```

### Scaling Configuration
To update scaling settings:

```bash
gcloud run services update $SERVICE_NAME \
  --region=$REGION \
  --max-instances=20 \
  --memory=4Gi \
  --cpu=2
```

## 🔒 Security Considerations

### Authentication
- The service is deployed with `--allow-unauthenticated` for public access
- For private access, remove this flag and configure IAM permissions

### Environment Variables
- Sensitive data should be stored in Google Secret Manager
- Use environment variables for non-sensitive configuration

### Container Security
- Images are built using Google Cloud Build
- Base image: `python:3.11-slim`
- Regular security updates are applied

## 📈 Performance Optimization

### Resource Allocation
- **Memory**: 2Gi (adjustable based on usage)
- **CPU**: 1 vCPU (adjustable based on load)
- **Max Instances**: 10 (prevents cost overruns)
- **Timeout**: 300 seconds (5 minutes)

### Scaling
- **Min Instances**: 0 (cost optimization)
- **Max Instances**: 10 (performance limit)
- **Target CPU**: 60% (efficient scaling)

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check build logs
   gcloud builds log <build-id>
   
   # Rebuild with verbose output
   gcloud builds submit --verbosity=debug
   ```

2. **Deployment Failures**
   ```bash
   # Check service status
   gcloud run services describe $SERVICE_NAME --region=$REGION
   
   # View recent logs
   gcloud logs read $SERVICE_NAME --region=$REGION --limit=100
   ```

3. **Rollback Issues**
   ```bash
   # Verify revision exists
   gcloud run revisions describe <revision-name> --region=$REGION
   
   # Check revision status
   gcloud run revisions list --service=$SERVICE_NAME --region=$REGION
   ```

### Health Checks
The deployment includes automatic health checks:
- **Readiness**: Checks if service is ready to receive traffic
- **Liveness**: Checks if service is running properly
- **Timeout**: 4 seconds
- **Interval**: 30 seconds

## 📝 Best Practices

1. **Always test before deploying to production**
2. **Keep the last 10 revisions for easy rollback**
3. **Monitor logs after deployment**
4. **Use meaningful commit messages for better version tracking**
5. **Document any manual changes to the deployment**
6. **Regularly clean up old revisions to manage costs**

## 🔗 Useful Commands Reference

```bash
# Quick deployment
./deploy-cloud-run-versioned.sh

# List revisions
./deploy-cloud-run-versioned.sh list

# Rollback
./rollback.sh <revision-name>

# Clean up
./deploy-cloud-run-versioned.sh cleanup

# Test deployment
./deploy-cloud-run-versioned.sh test

# View logs
gcloud logs tail $SERVICE_NAME --region=$REGION

# Service status
gcloud run services describe $SERVICE_NAME --region=$REGION
```

## 📞 Support

For issues with the deployment system:
1. Check the troubleshooting section above
2. Review the logs: `gcloud logs tail $SERVICE_NAME --region=$REGION`
3. Verify your Google Cloud project permissions
4. Ensure all required APIs are enabled 