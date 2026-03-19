#!/bin/bash
# Test runner script

set -e

echo "🧪 Running Tests"
echo "==============="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test backend
echo -e "${YELLOW}Testing Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "Running pytest..."
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

echo -e "${GREEN}✅ Backend tests passed${NC}"
cd ..

echo ""

# Test frontend
echo -e "${YELLOW}Testing Frontend...${NC}"
cd frontend

echo "Installing dependencies..."
npm ci --silent

echo "Running tests..."
npm test -- --watchAll=false --passWithNoTests

echo -e "${GREEN}✅ Frontend tests passed${NC}"
cd ..

echo ""
echo -e "${GREEN}✅ All tests passed!${NC}"
