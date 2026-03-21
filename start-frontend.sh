#!/bin/bash
# Start React Web App

echo "================================================"
echo "🌐 Starting Skin Cancer Detector Web App"
echo "================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/frontend/web" || exit 1

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
    echo ""
fi

echo "Starting React development server..."
echo "Web app will open at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop"
echo "================================================"
echo ""

npm start
