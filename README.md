# SF Pickleball Courts Finder

A web application to discover and visualize pickleball playing opportunities in San Francisco.

🌐 **[View Live Site](https://your-username.github.io/pickleball/)** *(Update after deployment)*

## Features

- 🗺️ **Interactive Map**: Browse all SF pickleball courts on an interactive Leaflet map
- 🔍 **Search**: Find courts by name in real-time
- 🏘️ **Filter by Neighborhood**: Filter courts by San Francisco neighborhoods
- 🥅 **Nets Filter**: Show only courts that provide nets
- 📊 **Court Details**: View detailed information about each court including:
  - Address and neighborhood
  - Number of courts
  - Whether nets are provided
  - Amenities and availability
- 🏓 **Reservation Information**: Access booking details for each court:
  - Operating hours
  - Pricing information
  - Direct links to SF Rec & Parks reservation system
  - Permit requirements for tournaments

## Data Source

Court data is sourced from the [SF Recreation and Parks Department](https://sfrecpark.org/1772/Where-to-Play-Pickleball) website and includes 17+ outdoor pickleball court locations across San Francisco.

## Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Leaflet.js for interactive mapping
- OpenStreetMap tiles
- Static JSON data files

**Data Management:**
- Python 3.11 (for data export)
- Flask models (for data structure)

**Deployment:**
- GitHub Pages (static hosting)
- GitHub Actions (automated deployment)

## Deployment

This site is deployed as a **static site** on GitHub Pages. All interactive features (search, filtering, map) work client-side.

### Automatic Deployment

Pushing to the `main` branch automatically triggers deployment via GitHub Actions:
1. Exports court data to JSON files
2. Deploys frontend to GitHub Pages
3. Site updates within a few minutes

### Manual Build (Optional)

To build locally before pushing:

```bash
./build.sh
```

This exports fresh data to `frontend/data/` directory.

## Development

### Prerequisites
- Python 3.11+
- [Pixi](https://prefix.dev/docs/pixi/overview) (optional, for environment management)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/pickleball.git
cd pickleball
```

2. Install dependencies:
```bash
pixi install
# OR
pip install flask flask-cors
```

3. Export court data (if needed):
```bash
cd backend
python export_static.py
```

### Running Locally

Serve the frontend with any HTTP server:

```bash
cd frontend
python3 -m http.server 8000
```

Then open: **http://localhost:8000/**

### Adding New Courts
```bash
cd backend
python populate_data.py  # or: pixi run python populate_data.py
python export_static.py   # Export to JSON
```

## Project Structure

```
pickleball/
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions deployment workflow
├── backend/
│   ├── app.py              # Flask REST API (legacy, not used in deployment)
│   ├── models.py           # Data models for courts
│   ├── populate_data.py    # Script to populate court data
│   ├── export_static.py    # Export data to static JSON files
│   ├── geocode.py          # Geocoding utilities
│   └── data/
│       └── courts.json     # Court data storage
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── css/
│   │   └── styles.css      # Application styles
│   ├── js/
│   │   ├── app.js          # Main application logic
│   │   └── map.js          # Leaflet map integration
│   └── data/               # Generated static data files
│       ├── courts.json     # Exported court data
│       ├── neighborhoods.json
│       └── stats.json
├── build.sh                # Build script for local testing
├── pyproject.toml          # Pixi/Python project configuration
└── README.md               # This file
```

## Usage

1. **Browse Courts**: The map loads automatically with all available courts marked
2. **Search**: Type in the search box to filter courts by name
3. **Filter by Neighborhood**: Use the dropdown to show courts in specific neighborhoods
4. **Filter by Nets**: Check "Nets Provided" to show only courts with nets
5. **View Details**: Click on any map marker or court to view detailed information
6. **Check Reservation Info**: View hours, pricing, and click "Check Availability & Reserve" to book
7. **Clear Filters**: Click "Clear Filters" to reset all filters

## Data Model

Each court includes:
- `id`: Unique identifier
- `name`: Court name
- `address`: Full address
- `neighborhood`: SF neighborhood
- `latitude` / `longitude`: GPS coordinates
- `num_courts`: Number of pickleball courts
- `nets_provided`: Boolean indicating if nets are provided
- `amenities`: List of available amenities
- `hours_of_operation`: Operating hours
- `pricing`: Cost information
- `reservation_url`: Link to online booking system
- `permit_required`: Whether permits are needed for tournaments

**Note**: Reservation data is manually curated and may require periodic updates. Last updated: February 2026.

## Future Enhancements

- [ ] Add court photos
- [ ] User reviews and ratings
- [x] Reservation information with booking links *(COMPLETED)*
- [ ] Real-time slot availability via automated scraping
- [ ] Directions integration
- [ ] "Find courts near me" feature using geolocation
- [ ] Indoor courts data
- [ ] Mobile app version
- [ ] Court condition reports from users
- [ ] Automated data refresh from SF Recreation website

## Development

### Adding New Courts

1. Edit `backend/populate_data.py` and add court data to `courts_data` list
2. Run the populate script:
```bash
cd backend
python populate_data.py
```
3. Export to JSON:
```bash
python export_static.py
```
4. Commit and push to deploy

### Updating Court Data

When court information changes:
1. Update `backend/data/courts.json` manually, OR
2. Update `backend/populate_data.py` and re-run it
3. Run `./build.sh` or `python backend/export_static.py`
4. Commit and push changes

## GitHub Pages Configuration

### Initial Setup

1. Go to repository Settings > Pages
2. Set Source to "GitHub Actions"
3. Push to main branch to trigger first deployment
4. Site will be live at `https://your-username.github.io/pickleball/`

### Custom Domain (Optional)

1. In repository Settings > Pages, add your custom domain
2. Configure DNS records with your domain provider
3. Enable "Enforce HTTPS"

## Legacy Flask API (Optional)

The repository still includes the Flask backend API for local development if needed:

```bash
cd backend
pixi run python app.py
```

API endpoints available at `http://localhost:5000/api/*` (see old README for details).

**Note**: The deployed GitHub Pages site does not use the Flask API - it's fully static.

## Usage

If you need to geocode addresses (requires fixing SSL certificate issues):

```bash
cd backend
pixi run python geocode.py
```

## License

This project is for educational and personal use. Court data is provided by SF Recreation and Parks Department.

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## Support

For issues or questions, please open an issue on the repository.

---

Built with ❤️ for the San Francisco pickleball community
