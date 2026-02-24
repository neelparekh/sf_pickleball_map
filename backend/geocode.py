"""Geocode addresses to latitude/longitude coordinates."""

import json
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from models import CourtStorage


def geocode_courts():
    """Geocode all courts in storage."""
    storage = CourtStorage()
    geolocator = Nominatim(user_agent="sf-pickleball-app")
    
    geocoded_count = 0
    skipped_count = 0
    
    for court in storage.courts:
        # Skip if already has coordinates
        if court.latitude and court.longitude:
            skipped_count += 1
            continue
        
        try:
            print(f"Geocoding: {court.name}...")
            # Add San Francisco, CA to ensure we get the right location
            full_address = f"{court.address}, San Francisco, CA"
            
            location = geolocator.geocode(full_address, timeout=10)
            
            if location:
                court.latitude = location.latitude
                court.longitude = location.longitude
                geocoded_count += 1
                print(f"  -> {location.latitude}, {location.longitude}")
            else:
                print(f"  -> Could not geocode")
            
            # Be respectful to the geocoding service
            time.sleep(1)
            
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"  -> Error: {e}")
            continue
    
    # Save updated storage
    storage.save()
    print(f"\nGeocoding complete!")
    print(f"  Geocoded: {geocoded_count}")
    print(f"  Skipped (already had coordinates): {skipped_count}")
    print(f"  Total courts: {len(storage.courts)}")


if __name__ == "__main__":
    geocode_courts()
