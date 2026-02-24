#!/bin/bash

# SF Pickleball Courts Finder - Startup Script

echo "🏓 Starting SF Pickleball Courts Finder..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Start backend API
echo "📡 Starting Flask API on port 5000..."
cd backend
pixi run python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "✅ Backend API is running (PID: $BACKEND_PID)"
else
    echo "❌ Failed to start backend API"
    exit 1
fi

# Start frontend server
echo "🌐 Starting frontend server on port 8000..."
cd frontend
python3 -m http.server 8000 &
FRONTEND_PID=$!
cd ..

echo "⏳ Waiting for frontend to start..."
sleep 3

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ✅ APPLICATION IS READY!                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Open in your browser: http://localhost:8000"
echo ""
echo "📊 Backend API: http://localhost:5000/api/*"
echo "   - Health:        http://localhost:5000/api/health"
echo "   - All Courts:    http://localhost:5000/api/courts"
echo "   - Neighborhoods: http://localhost:5000/api/neighborhoods"
echo ""
echo "🛑 To stop the servers, run:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "   Or press Ctrl+C and run:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Open browser automatically (macOS)
if command -v open &> /dev/null; then
    echo "🚀 Opening browser..."
    sleep 2
    open http://localhost:8000
fi

echo "💡 Press Ctrl+C to stop (then run kill command above)"
echo ""

# Keep script running
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

# Wait for processes
wait
