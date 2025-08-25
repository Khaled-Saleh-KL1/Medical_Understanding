#!/bin/bash

# Medical Understanding AI - Docker Deployment Script

echo "🚀 Medical Understanding AI - Docker Deployment"
echo "================================================"

# Check if .env file exists
if [ ! -f "src/.env" ]; then
    echo "❌ Error: .env file not found in src/ directory"
    echo "Please create src/.env with your API keys:"
    echo "GEMINI_API_KEY=your_key_here"
    echo "TAVILY_API_KEY=your_key_here"
    exit 1
fi

# Build and run with docker compose
echo "🔨 Building Docker image..."
docker compose build

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo "🚀 Starting Medical Understanding AI API..."
docker compose up -d

if [ $? -eq 0 ]; then
    echo "✅ Medical Understanding AI API is running!"
    echo ""
    echo "📍 Access points:"
    echo "   • API: http://localhost:8000"
    echo "   • Docs: http://localhost:8000/docs"
    echo "   • Health: http://localhost:8000/health"
    echo ""
    echo "📊 Monitoring:"
    echo "   • Logs: docker compose logs -f medical-ai-api"
    echo "   • Stop: docker compose down"
    echo "   • Status: docker compose ps"
else
    echo "❌ Failed to start the API!"
    exit 1
fi
