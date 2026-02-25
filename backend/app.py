"""Flask API for pickleball courts."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from models import CourtStorage
from availability_scraper import RecUsAvailabilityScraper
from datetime import datetime
import os

app = Flask(__name__)

# Configure CORS for production and development
allowed_origins = [
    "http://localhost:8080",
    "http://localhost:5000", 
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5000",
    "https://neelparekh.github.io"
]

CORS(app, origins=allowed_origins)

# Initialize storage
storage = CourtStorage()

# Initialize scraper
scraper = RecUsAvailabilityScraper()


@app.route('/api/courts', methods=['GET'])
def get_courts():
    """Get all courts with optional filtering."""
    try:
        # Get query parameters
        search = request.args.get('search', None)
        neighborhood = request.args.get('neighborhood', None)
        nets_provided_param = request.args.get('nets_provided', None)
        
        # Convert nets_provided to boolean if provided
        nets_provided = None
        if nets_provided_param is not None:
            nets_provided = nets_provided_param.lower() in ['true', '1', 'yes']
        
        # Filter courts
        courts = storage.filter_courts(
            search=search,
            neighborhood=neighborhood,
            nets_provided=nets_provided
        )
        
        return jsonify({
            'success': True,
            'count': len(courts),
            'courts': courts
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/courts/<court_id>', methods=['GET'])
def get_court(court_id):
    """Get a specific court by ID."""
    try:
        court = storage.get_by_id(court_id)
        
        if court:
            return jsonify({
                'success': True,
                'court': court
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Court not found'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/neighborhoods', methods=['GET'])
def get_neighborhoods():
    """Get list of all neighborhoods."""
    try:
        neighborhoods = storage.get_neighborhoods()
        
        return jsonify({
            'success': True,
            'neighborhoods': neighborhoods
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about courts."""
    try:
        all_courts = storage.get_all()
        
        stats = {
            'total_courts': len(all_courts),
            'courts_with_nets': len([c for c in all_courts if c.get('nets_provided')]),
            'total_court_count': sum(c.get('num_courts', 0) for c in all_courts),
            'neighborhoods': len(storage.get_neighborhoods())
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'courts_loaded': len(storage.courts)
    })


@app.route('/api/availability/<court_id>', methods=['GET'])
def get_availability(court_id):
    """
    Get real-time availability for a court.
    
    Query params:
        date: Date in YYYY-MM-DD format (optional, defaults to today)
        days: Number of days to fetch (optional, defaults to 7)
    """
    try:
        # Get court details
        court = storage.get_by_id(court_id)
        if not court:
            return jsonify({
                'success': False,
                'error': 'Court not found'
            }), 404
        
        # Check if court has reservation_url (i.e., is reservable)
        if not court.get('reservation_url'):
            return jsonify({
                'success': True,
                'court_id': court_id,
                'court_name': court['name'],
                'message': 'This court is open play only (not reservable)',
                'availability': []
            })
        
        # Get query parameters
        date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
        days = int(request.args.get('days', 7))
        
        # Need to map court_id to location_id
        # For now, we'll use a mapping for known courts
        location_id_map = {
            'buena-vista-park': '3f842b1e-13f9-447d-ab12-62b62d954d3e',
            # Add more mappings as needed
        }
        
        location_id = location_id_map.get(court_id)
        if not location_id:
            return jsonify({
                'success': True,
                'court_id': court_id,
                'court_name': court['name'],
                'message': 'Availability data not yet available for this court',
                'availability': []
            })
        
        # Fetch availability
        availability_data = scraper.get_availability_for_court(
            location_id,
            court['name'],
            date,
            days
        )
        
        return jsonify({
            'success': True,
            **availability_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/availability/check', methods=['GET'])
def check_availability():
    """
    Check if courts are available at a specific time.
    
    Query params:
        court_id: Court ID (required)
        date: Date in YYYY-MM-DD format (required)
        start_time: Start time HH:MM (required)
        end_time: End time HH:MM (required)
    """
    try:
        court_id = request.args.get('court_id')
        date = request.args.get('date')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        if not all([court_id, date, start_time, end_time]):
            return jsonify({
                'success': False,
                'error': 'Missing required parameters'
            }), 400
        
        # Get court and location_id
        court = storage.get_by_id(court_id)
        if not court:
            return jsonify({
                'success': False,
                'error': 'Court not found'
            }), 404
        
        location_id_map = {
            'buena-vista-park': '3f842b1e-13f9-447d-ab12-62b62d954d3e',
        }
        
        location_id = location_id_map.get(court_id)
        if not location_id:
            return jsonify({
                'success': False,
                'error': 'Availability check not supported for this court'
            }), 404
        
        # Check availability
        has_availability = scraper.check_availability_for_time_range(
            location_id,
            date,
            start_time,
            end_time
        )
        
        return jsonify({
            'success': True,
            'court_id': court_id,
            'court_name': court['name'],
            'date': date,
            'time_range': f"{start_time} - {end_time}",
            'available': has_availability
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print(f"Loaded {len(storage.courts)} courts")
    print(f"Neighborhoods: {', '.join(storage.get_neighborhoods())}")
    
    port = int(os.environ.get('PORT', 5000))
    print(f"\nStarting Flask API on port {port}")
    
    # Use production settings when PORT is set (Railway)
    if 'PORT' in os.environ:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(debug=True, host='0.0.0.0', port=port)
