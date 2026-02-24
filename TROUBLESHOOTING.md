# Troubleshooting Guide

## Common Issues and Solutions

### Issue: "Not Found" error at http://localhost:5000/

**Solution**: This is normal! The Flask API only serves endpoints under `/api/`. 

**Correct URLs to use:**
- http://localhost:5000/api/health
- http://localhost:5000/api/courts
- http://localhost:5000/api/neighborhoods
- http://localhost:5000/api/stats

The frontend app automatically calls these API endpoints.

### Issue: "Unable to connect" at http://localhost:8000/

**Cause**: The frontend server is not running.

**Solution**: Start the frontend server:
```bash
cd frontend
python3 -m http.server 8000
```

### Issue: No courts showing on the map

**Checklist:**
1. Is the Flask API running? Test: `curl http://localhost:5000/api/health`
2. Is the API returning courts? Test: `curl http://localhost:5000/api/courts`
3. Check browser console (F12) for errors
4. Verify CORS is not blocking requests (should see API calls in Network tab)

### Issue: Map not loading

**Solution**: 
- Check internet connection (Leaflet loads tiles from OpenStreetMap)
- Check browser console for JavaScript errors
- Verify Leaflet CSS and JS are loading

### Quick Health Check

Run these commands to verify everything is working:

```bash
# Test backend API
curl http://localhost:5000/api/health

# Test courts endpoint
curl http://localhost:5000/api/courts | python3 -m json.tool | head -20

# Test frontend
curl -I http://localhost:8000/
```

### Restarting the Application

If things aren't working, try restarting:

```bash
# Stop all processes
pkill -f "python app.py"
pkill -f "http.server 8000"

# Start backend
cd backend
pixi run python app.py &

# Start frontend (in new terminal or background)
cd ../frontend
python3 -m http.server 8000 &

# Or use the startup script
./start.sh
```

### Viewing Logs

Backend logs are shown in the terminal where you ran `python app.py`.

For frontend access logs:
```bash
tail -f /tmp/frontend_server.log
```

### Port Already in Use

If you see "Address already in use" errors:

```bash
# Find process using port 5000
lsof -ti:5000

# Kill the process
kill $(lsof -ti:5000)

# Same for port 8000
kill $(lsof -ti:8000)
```

### Data Not Loading

If courts aren't showing:

```bash
# Re-populate the data
cd backend
pixi run python populate_data.py

# Verify data file exists
ls -lh data/courts.json

# Check data content
cat data/courts.json | python3 -m json.tool | head -30
```

### Browser-Specific Issues

**Chrome/Edge:**
- Clear cache: Ctrl+Shift+Delete
- Hard reload: Ctrl+Shift+R

**Firefox:**
- Clear cache: Ctrl+Shift+Delete
- Hard reload: Ctrl+F5

**Safari:**
- Clear cache: Cmd+Option+E
- Hard reload: Cmd+Shift+R

### CORS Errors

If you see CORS errors in browser console:

1. Verify Flask-CORS is installed: `pixi list | grep flask-cors`
2. Check that `CORS(app)` is in `backend/app.py`
3. Restart the backend server

### Still Having Issues?

Check:
1. Python version: `python3 --version` (should be 3.11+)
2. Pixi is installed: `pixi --version`
3. All dependencies installed: `pixi install`
4. Correct directory: You should be in `/path/to/pickleball/`
