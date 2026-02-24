# SF Pickleball Courts Finder

A web application to discover and visualize pickleball playing opportunities in San Francisco.

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

## Data Source

Court data is sourced from the [SF Recreation and Parks Department](https://sfrecpark.org/1772/Where-to-Play-Pickleball) website and includes 17+ outdoor pickleball court locations across San Francisco.

## Tech Stack

**Backend:**
- Python 3.11
- Flask (REST API)
- Flask-CORS
- JSON data storage

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Leaflet.js for interactive mapping
- OpenStreetMap tiles

**Environment Management:**
- Pixi for Python environment and dependency management

## Installation

### Prerequisites
- Python 3.11+
- [Pixi](https://prefix.dev/docs/pixi/overview) for environment management

### Setup

1. Clone or navigate to the repository:
```bash
cd /path/to/pickleball
```

2. Install dependencies using Pixi (already configured):
```bash
pixi install
```

3. Populate the courts data:
```bash
cd backend
pixi run python populate_data.py
```

## Running the Application

### Quick Start (Easiest Method)

Use the provided startup script:

```bash
./start.sh
```

This will start both backend and frontend servers automatically.

### Manual Start

#### 1. Start the Flask API Server

```bash
cd backend
pixi run python app.py
```

The API will be available at `http://localhost:5000/api/*`

**Note**: The root URL `http://localhost:5000/` will show a 404 error - this is normal! The API endpoints are under `/api/`

### API Endpoints

- `GET /api/courts` - Get all courts (supports query params: `search`, `neighborhood`, `nets_provided`)
- `GET /api/courts/<id>` - Get specific court details
- `GET /api/neighborhoods` - Get list of neighborhoods
- `GET /api/stats` - Get statistics about courts
- `GET /api/health` - Health check endpoint

#### 2. Start the Frontend

Serve the frontend with a simple HTTP server:

```bash
cd frontend
python3 -m http.server 8000
```

Then open your browser to: **http://localhost:8000/**

**Important**: 
- Make sure the Flask API is running on port 5000 before opening the frontend
- Use `http://localhost:8000/` to view the app (not port 5000)
- The backend API endpoints are at `http://localhost:5000/api/*`

### Troubleshooting

If you encounter issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common problems and solutions.

## Project Structure

```
pickleball/
├── backend/
│   ├── app.py              # Flask REST API
│   ├── models.py           # Data models for courts
│   ├── populate_data.py    # Script to populate court data
│   ├── scraper.py          # Web scraper (for future use)
│   ├── geocode.py          # Geocoding utilities
│   ├── requirements.txt    # Python dependencies
│   └── data/
│       └── courts.json     # Court data storage
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── css/
│   │   └── styles.css      # Application styles
│   └── js/
│       ├── app.js          # Main application logic
│       └── map.js          # Leaflet map integration
├── pyproject.toml          # Pixi/Python project configuration
└── README.md               # This file
```

## Usage

1. **Browse Courts**: The map loads automatically with all available courts marked
2. **Search**: Type in the search box to filter courts by name
3. **Filter by Neighborhood**: Use the dropdown to show courts in specific neighborhoods
4. **Filter by Nets**: Check "Nets Provided" to show only courts with nets
5. **View Details**: Click on any map marker or court to view detailed information
6. **Clear Filters**: Click "Clear Filters" to reset all filters

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

## Future Enhancements

- [ ] Add court photos
- [ ] User reviews and ratings
- [ ] Real-time availability/reservations
- [ ] Directions integration
- [ ] "Find courts near me" feature using geolocation
- [ ] Indoor courts data
- [ ] Mobile app version
- [ ] Court condition reports from users
- [ ] Automated data refresh from SF Recreation website

## Development

### Adding New Courts

Edit `backend/populate_data.py` and add new court data to the `courts_data` list, then run:

```bash
cd backend
pixi run python populate_data.py
```

### Refreshing Geocoding

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
