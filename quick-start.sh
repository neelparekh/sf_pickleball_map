#!/bin/bash

# Simple startup - just runs the commands you need

echo "Starting backend..."
cd /Users/neel.parekh/Documents/repos/fun/pickleball/backend
pixi run python app.py &

echo "Waiting 5 seconds for backend to start..."
sleep 5

echo "Starting frontend..."
cd /Users/neel.parekh/Documents/repos/fun/pickleball/frontend
python3 -m http.server 8000 &

sleep 3

echo ""
echo "✅ READY!"
echo ""
echo "Open your browser to: http://localhost:8000"
echo ""
echo "Press Ctrl+C when done"
echo ""

wait
