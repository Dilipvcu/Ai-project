#!/bin/bash
# Quick start script for development

set -e

echo "🚀 AI Document Analysis Engine - Quick Start"
echo "==========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "📋 Checking prerequisites..."
echo "✅ Docker is running"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp backend/.env.example .env
    echo "⚠️  Please update .env with your API keys"
fi

echo ""
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check health
echo ""
echo "🏥 Checking service health..."

# Check backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend is starting (takes a moment)..."
fi

# Check frontend
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running"
else
    echo "⚠️  Frontend is starting..."
fi

echo ""
echo "✨ Services are starting up!"
echo ""
echo "📱 Access the application:"
echo "   • Frontend: http://localhost:3000"
echo "   • API Docs: http://localhost:8000/docs"
echo "   • API Health: http://localhost:8000/health"
echo ""
echo "📊 Monitoring:"
echo "   • Prometheus: http://localhost:9090"
echo ""
echo "📝 View logs:"
echo "   docker-compose logs -f backend"
echo "   docker-compose logs -f frontend"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
