"""Flask API for pickleball courts."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from models import CourtStorage

app = Flask(__name__)
CORS(app)

# Initialize storage
storage = CourtStorage()


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


if __name__ == '__main__':
    print(f"Loaded {len(storage.courts)} courts")
    print(f"Neighborhoods: {', '.join(storage.get_neighborhoods())}")
    print("\nStarting Flask API on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
