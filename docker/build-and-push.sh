#!/bin/bash
# Odoo Docker Build and Push to Harbor Script

set -e

# Configuration
HARBOR_REGISTRY="${HARBOR_REGISTRY:-harbor.yourdomain.com}"
HARBOR_PROJECT="${HARBOR_PROJECT:-odoo}"
IMAGE_NAME="odoo"
VERSION="${VERSION:-19.0}"
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# Full image name
FULL_IMAGE_NAME="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${IMAGE_NAME}"

echo "======================================"
echo "Odoo Docker Build and Push"
echo "======================================"
echo "Registry: ${HARBOR_REGISTRY}"
echo "Project: ${HARBOR_PROJECT}"
echo "Image: ${IMAGE_NAME}"
echo "Version: ${VERSION}"
echo "Commit: ${GIT_COMMIT}"
echo "======================================"
echo ""

# Check if logged into Harbor
echo "Checking Harbor registry login..."
if ! docker info | grep -q "${HARBOR_REGISTRY}"; then
    echo "Please login to Harbor registry first:"
    echo "  docker login ${HARBOR_REGISTRY}"
    exit 1
fi

# Build the image
echo "Building Docker image..."
docker build \
    --build-arg BUILD_DATE="${BUILD_DATE}" \
    --build-arg VCS_REF="${GIT_COMMIT}" \
    --build-arg VERSION="${VERSION}" \
    -t "${FULL_IMAGE_NAME}:${VERSION}" \
    -t "${FULL_IMAGE_NAME}:${VERSION}-${GIT_COMMIT}" \
    -t "${FULL_IMAGE_NAME}:latest" \
    -f Dockerfile \
    .

echo ""
echo "Build completed successfully!"
echo ""

# Display image details
echo "Image details:"
docker images | grep "${IMAGE_NAME}" | head -3

echo ""
read -p "Push images to Harbor? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing images to Harbor..."
    
    # Push versioned image
    echo "Pushing ${FULL_IMAGE_NAME}:${VERSION}..."
    docker push "${FULL_IMAGE_NAME}:${VERSION}"
    
    # Push image with commit hash
    echo "Pushing ${FULL_IMAGE_NAME}:${VERSION}-${GIT_COMMIT}..."
    docker push "${FULL_IMAGE_NAME}:${VERSION}-${GIT_COMMIT}"
    
    # Push latest tag
    echo "Pushing ${FULL_IMAGE_NAME}:latest..."
    docker push "${FULL_IMAGE_NAME}:latest"
    
    echo ""
    echo "======================================"
    echo "✅ Images pushed successfully!"
    echo "======================================"
    echo ""
    echo "Available tags:"
    echo "  - ${FULL_IMAGE_NAME}:${VERSION}"
    echo "  - ${FULL_IMAGE_NAME}:${VERSION}-${GIT_COMMIT}"
    echo "  - ${FULL_IMAGE_NAME}:latest"
    echo ""
    echo "Pull command:"
    echo "  docker pull ${FULL_IMAGE_NAME}:${VERSION}"
    echo ""
else
    echo "Push cancelled."
fi
