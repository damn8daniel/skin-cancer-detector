#!/bin/bash
# Start both backend and frontend together

echo "╔════════════════════════════════════════════════╗"
echo "║  Starting Complete Skin Cancer Detector System ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping all services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup EXIT INT TERM

# Start backend in background
echo "🚀 Starting Backend API..."
cd "$SCRIPT_DIR/backend" || exit 1
../start-backend.sh > /tmp/skincancer-backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo "   Logs: tail -f /tmp/skincancer-backend.log"
echo ""

# Wait for backend to start
sleep 3

# Check if backend is running
if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ Backend started successfully"
else
    echo "❌ Backend failed to start"
    echo "   Check logs: cat /tmp/skincancer-backend.log"
    exit 1
fi
echo ""

# Start frontend in background
echo "🌐 Starting Frontend Web App..."
cd "$SCRIPT_DIR" || exit 1
./start-frontend.sh > /tmp/skincancer-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
echo "   Logs: tail -f /tmp/skincancer-frontend.log"
echo ""

echo "╔════════════════════════════════════════════════╗"
echo "║              ✅ SYSTEM RUNNING!                ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "🌐 Web App: http://localhost:3000"
echo "🔌 API: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""
echo "Monitoring services..."
echo ""

# Keep script running and monitor processes
while true; do
    if ! ps -p $BACKEND_PID > /dev/null; then
        echo "❌ Backend crashed! Check logs."
        exit 1
    fi
    if ! ps -p $FRONTEND_PID > /dev/null; then
        echo "❌ Frontend crashed! Check logs."
        exit 1
    fi
    sleep 5
done
