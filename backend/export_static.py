"""Export court data to static JSON files for GitHub Pages deployment."""

import json
from pathlib import Path
from models import CourtStorage


def export_static_data():
    """Export all API endpoint data to static JSON files."""
    
    # Initialize storage
    storage = CourtStorage()
    
    # Define output directory (frontend/data)
    output_dir = Path(__file__).parent.parent / "frontend" / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Export courts data
    courts_data = {
        'success': True,
        'count': len(storage.courts),
        'courts': storage.get_all()
    }
    with open(output_dir / "courts.json", 'w') as f:
        json.dump(courts_data, f, indent=2)
    print(f"✓ Exported {len(storage.courts)} courts to frontend/data/courts.json")
    
    # Export neighborhoods data
    neighborhoods = storage.get_neighborhoods()
    neighborhoods_data = {
        'success': True,
        'neighborhoods': neighborhoods
    }
    with open(output_dir / "neighborhoods.json", 'w') as f:
        json.dump(neighborhoods_data, f, indent=2)
    print(f"✓ Exported {len(neighborhoods)} neighborhoods to frontend/data/neighborhoods.json")
    
    # Export stats data
    total_courts = len(storage.courts)
    total_court_count = sum(c.num_courts for c in storage.courts)
    nets_provided_count = sum(1 for c in storage.courts if c.nets_provided)
    
    stats_data = {
        'success': True,
        'stats': {
            'total_locations': total_courts,
            'total_courts': total_court_count,
            'nets_provided': nets_provided_count,
            'neighborhoods': len(neighborhoods)
        }
    }
    with open(output_dir / "stats.json", 'w') as f:
        json.dump(stats_data, f, indent=2)
    print(f"✓ Exported stats to frontend/data/stats.json")
    
    print(f"\n✅ Successfully exported all data to {output_dir}")
    print(f"   - courts.json ({total_courts} locations)")
    print(f"   - neighborhoods.json ({len(neighborhoods)} neighborhoods)")
    print(f"   - stats.json")


if __name__ == "__main__":
    export_static_data()
