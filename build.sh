#!/bin/bash

# Build script for GitHub Pages deployment
# This script exports court data and prepares files for deployment

set -e

echo "🏗️  Building SF Pickleball Courts Finder..."

# Navigate to backend directory
cd "$(dirname "$0")/backend"

echo "📊 Exporting court data to static JSON files..."
python export_static.py

echo ""
echo "✅ Build complete!"
echo ""
echo "📁 Static files ready in frontend/ directory:"
echo "   - frontend/index.html"
echo "   - frontend/data/courts.json"
echo "   - frontend/data/neighborhoods.json"
echo "   - frontend/data/stats.json"
echo ""
echo "🚀 To deploy:"
echo "   1. Push changes to main branch"
echo "   2. GitHub Actions will automatically deploy to GitHub Pages"
echo ""
echo "🧪 To test locally:"
echo "   cd frontend && python3 -m http.server 8000"
echo "   Open http://localhost:8000"
