#!/bin/bash

# Frontend Hosting Configuration
# Use this script to run the frontend on different hosts

echo "🚀 AI Document Analysis - Frontend Hosting Setup"
echo "=================================================="
echo ""

# Check if port argument is provided
if [ -z "$1" ]; then
    echo "Usage: ./run-frontend.sh [port]"
    echo ""
    echo "Examples:"
    echo "  ./run-frontend.sh 3000    # Run on localhost:3000"
    echo "  ./run-frontend.sh 3001    # Run on localhost:3001"
    echo "  ./run-frontend.sh 8080    # Run on localhost:8080"
    echo ""
    echo "Default options:"
    echo "  npm run dev              # Port 3000 (default)"
    echo "  npm run dev:3001         # Port 3001"
    echo "  npm run dev:3002         # Port 3002"
    echo ""
    exit 1
fi

PORT=$1

echo "Starting Frontend on port $PORT..."
echo ""
echo "✅ Frontend URL: http://localhost:$PORT"
echo "✅ Backend API: http://localhost:8000"
echo "✅ API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Export PORT and run dev server
export PORT=$PORT
npm run dev:custom
