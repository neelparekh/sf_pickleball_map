# Railway Deployment Guide

## Quick Deploy to Railway

1. **Install Railway CLI** (if not already installed):
   ```bash
   npm i -g @railway/cli
   # or
   brew install railway
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize and Deploy**:
   ```bash
   # From the project root
   railway init
   railway up
   ```

4. **Generate Domain**:
   ```bash
   railway domain
   ```
   This will give you a URL like `https://your-app.railway.app`

## Manual Deployment (via GitHub)

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `neelparekh/sf_pickleball_map`
5. Railway will auto-detect Python and use the configuration files

## Configuration Files

- `railway.json` - Railway-specific configuration
- `Procfile` - Process command for web server
- `backend/requirements.txt` - Python dependencies

## Environment Variables

No environment variables needed! The app works out of the box.

## CORS Configuration

The backend is configured to accept requests from:
- `https://neelparekh.github.io` (GitHub Pages)
- `http://localhost:8080` (local development)

## After Deployment

1. Get your Railway URL (e.g., `https://sf-pickleball.railway.app`)
2. Test the API:
   ```bash
   curl https://YOUR-APP.railway.app/api/health
   curl https://YOUR-APP.railway.app/api/courts
   curl https://YOUR-APP.railway.app/api/availability/buena-vista-park?days=3
   ```

3. Update frontend to use the Railway URL (see below)

## Update Frontend

Add this to `frontend/js/app.js`:

```javascript
// At the top of app.js
const API_BASE_URL = 'https://YOUR-APP.railway.app/api';

// Then in the loadAvailability function:
async function loadAvailability(courtId, days = 7) {
    const response = await fetch(`${API_BASE_URL}/availability/${courtId}?days=${days}`);
    const data = await response.json();
    return data;
}
```

## Free Tier Limits

Railway free tier includes:
- 500 hours/month of runtime (~16 hours/day)
- $5 credit/month
- Automatic sleep after 30 min of inactivity

Perfect for this project!

## Monitoring

View logs in Railway dashboard or via CLI:
```bash
railway logs
```

## Troubleshooting

**App won't start?**
- Check logs: `railway logs`
- Verify Python version in logs
- Ensure all dependencies are in `requirements.txt`

**CORS errors?**
- Verify GitHub Pages domain in `backend/app.py` CORS config
- Check Railway deployment URL matches your expectations
