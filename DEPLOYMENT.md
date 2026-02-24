# GitHub Pages Deployment Guide

## Quick Reference

### First-Time Setup

1. **Enable GitHub Pages**
   - Go to repository Settings > Pages
   - Under "Build and deployment", set Source to **"GitHub Actions"**
   - Save changes

2. **Push to Deploy**
   ```bash
   git add .
   git commit -m "Deploy to GitHub Pages"
   git push origin main
   ```

3. **Check Deployment Status**
   - Go to Actions tab in GitHub
   - Watch the "Deploy to GitHub Pages" workflow
   - Site will be live at: `https://YOUR-USERNAME.github.io/pickleball/`

### Making Updates

#### Update Court Data

1. **Option A: Edit data file directly**
   ```bash
   # Edit backend/data/courts.json
   cd backend
   python export_static.py
   git add ../frontend/data/
   git commit -m "Update court data"
   git push
   ```

2. **Option B: Edit populate script**
   ```bash
   # Edit backend/populate_data.py
   cd backend
   python populate_data.py
   python export_static.py
   git add ../frontend/data/
   git commit -m "Update court data"
   git push
   ```

#### Update Frontend Code

```bash
# Edit files in frontend/ (HTML, CSS, JS)
git add frontend/
git commit -m "Update frontend"
git push
```

### Build Locally First (Optional)

```bash
./build.sh              # Run export script
cd frontend
python3 -m http.server 8000
# Test at http://localhost:8000
```

### Troubleshooting Deployment

1. **Check Actions Tab**: Look for failed workflow runs
2. **Common Issues**:
   - Data files not committed: Make sure `frontend/data/*.json` are tracked
   - Python dependencies: Verify GitHub Actions installs flask and flask-cors
   - Permissions: Check repository has Pages enabled

3. **View Logs**: Click on failed workflow run to see detailed error messages

### Custom Domain Setup

1. Add `CNAME` file to `frontend/` directory:
   ```
   your-domain.com
   ```

2. Configure DNS with your domain provider:
   - Add `A` records pointing to GitHub Pages IPs
   - Or add `CNAME` record pointing to `YOUR-USERNAME.github.io`

3. Enable HTTPS in repository Settings > Pages

### Architecture Notes

- **Deployment**: GitHub Actions workflow (`.github/workflows/deploy.yml`)
- **Build Step**: Exports `backend/data/courts.json` → `frontend/data/*.json`
- **Frontend**: Pure static files (HTML/CSS/JS) served from `frontend/` directory
- **No Server**: All filtering/search happens client-side in browser
- **Data Updates**: Require commit + push (no real-time updates)

### Files That Must Be Committed

✅ `frontend/data/courts.json`
✅ `frontend/data/neighborhoods.json`
✅ `frontend/data/stats.json`
✅ All files in `frontend/` directory
✅ `.github/workflows/deploy.yml`

### Files Excluded from Git

❌ `__pycache__/` (Python cache)
❌ `.pixi/` (except config.toml)
❌ IDE files (.vscode, .idea)
