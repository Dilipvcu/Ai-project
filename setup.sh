#!/bin/bash

# Build setup script
echo "🚀 AI Document Analysis Engine - Setup Script"
echo "=============================================="

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi
echo "✅ Docker found: $(docker --version)"

# Setup backend
echo ""
echo "📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
echo "✅ Backend setup complete"

# Setup frontend
echo ""
echo "📦 Setting up frontend..."
cd ../frontend
npm install
echo "✅ Frontend setup complete"

echo ""
echo "✨ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Docker Compose (recommended):"
echo "     docker-compose up"
echo ""
echo "  2. Manual setup:"
echo "     Backend:  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "     Frontend: cd frontend && npm run dev"
echo ""
echo "Then open http://localhost:3000 in your browser"
