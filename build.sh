#!/bin/bash
# Build script for optimized PDF extraction container

echo "Building optmized PDF extraction container..."

# Build with build-time optimizations
docker build \
    --no-cache \
    --tag pdf-extractor:latest \
    --tag pdf-extractor:v1.0 \
    .

echo "Build completed!"
echo "Image size:"
docker images pdf-extractor:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo ""
echo "To run the container:"
echo "docker run --rm -v /path/to/pdfs:/pdfs pdf-extractor:latest /pdfs/sample.pdf"