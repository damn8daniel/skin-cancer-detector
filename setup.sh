#!/bin/bash
# Complete Setup and Installation Script

echo "╔════════════════════════════════════════════════╗"
echo "║   Skin Cancer Detector - Complete Setup       ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Step 1: Check Python
echo "📋 Step 1: Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION found"
else
    echo "❌ Python 3 not found"
    echo "   Install from: https://www.python.org/downloads/"
    exit 1
fi
echo ""

# Step 2: Check Node.js
echo "📋 Step 2: Checking Node.js installation..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js $NODE_VERSION found"
else
    echo "❌ Node.js not found"
    echo "   Install from: https://nodejs.org/"
    exit 1
fi
echo ""

# Step 3: Install Python dependencies
echo "📋 Step 3: Installing Python dependencies..."
cd backend
if pip3 install -r requirements.txt; then
    echo "✅ Python dependencies installed"
else
    echo "⚠️  Some packages may need additional setup"
    echo "   TensorFlow might take a while to install"
fi
cd ..
echo ""

# Step 4: Install Node dependencies
echo "📋 Step 4: Installing Node.js dependencies..."
cd frontend/web
if npm install; then
    echo "✅ Node dependencies installed"
else
    echo "❌ Error installing Node dependencies"
    exit 1
fi
cd ../..
echo ""

# Step 5: Test backend
echo "📋 Step 5: Testing backend..."
cd backend
python3 -c "from config.settings import APP_NAME; print(f'✅ Backend configuration loaded: {APP_NAME}')"
cd ..
echo ""

# Step 6: Create necessary directories
echo "📋 Step 6: Creating necessary directories..."
mkdir -p backend/models/saved_models
mkdir -p backend/data
echo "✅ Directories created"
echo ""

echo "╔════════════════════════════════════════════════╗"
echo "║           ✅ SETUP COMPLETE!                   ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "🚀 Ready to start!"
echo ""
echo "To start the application:"
echo ""
echo "   OPTION 1 - Two separate terminals:"
echo "   Terminal 1: ./start-backend.sh"
echo "   Terminal 2: ./start-frontend.sh"
echo ""
echo "   OPTION 2 - One command (both servers):"
echo "   ./start-all.sh"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "📖 Read README.md for detailed instructions"
echo ""
