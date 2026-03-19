#!/bin/bash
# Deployment script for AWS

set -e

echo "🚀 Deploying to AWS..."
echo "====================="

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO=${ECR_REPO:-ai-document-analysis}
CLUSTER_NAME=${CLUSTER_NAME:-docanalysis}

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}ℹ️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Prerequisites
log_info "Checking prerequisites..."

if ! command -v aws &> /dev/null; then
    log_error "AWS CLI is not installed"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed"
    exit 1
fi

# Build images
log_info "Building Docker images..."
docker-compose build

# Get ECR login
log_info "Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com

# Tag and push images
log_info "Pushing images to ECR..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO"

docker tag ai-document-analysis-backend:latest $ECR_URI:backend-latest
docker tag ai-document-analysis-frontend:latest $ECR_URI:frontend-latest

docker push $ECR_URI:backend-latest
docker push $ECR_URI:frontend-latest

log_info "✅ Deployment complete!"
log_info "Update your ECS task definitions with:"
log_info "  Backend: $ECR_URI:backend-latest"
log_info "  Frontend: $ECR_URI:frontend-latest"
