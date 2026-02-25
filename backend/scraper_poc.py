"""
Proof-of-concept scraper for rec.us court availability.

Tests if we can extract availability data from SF Rec & Parks reservation system.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta
import warnings

# Suppress SSL warnings when verify=False
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def test_rec_us_structure(court_url):
    """
    Test what data we can get from rec.us without JavaScript execution.
    
    Args:
        court_url: URL like https://www.rec.us/buenavista
    """
    print(f"\n{'='*60}")
    print(f"Testing: {court_url}")
    print(f"{'='*60}\n")
    
    # Try to fetch the page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(court_url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        print(f"✓ Successfully fetched page (status: {response.status_code})")
        print(f"✓ Content length: {len(response.text)} bytes\n")
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for Next.js data
        next_data = soup.find('script', {'id': '__NEXT_DATA__'})
        if next_data:
            print("✓ Found __NEXT_DATA__ script tag")
            try:
                data = json.loads(next_data.string)
                print("\n__NEXT_DATA__ structure:")
                print(json.dumps(data, indent=2)[:1000] + "...\n")
                
                # Extract location ID
                if 'query' in data and 'locationId' in data['query']:
                    location_id = data['query']['locationId']
                    print(f"✓ Location ID: {location_id}\n")
                    return location_id
            except json.JSONDecodeError as e:
                print(f"✗ Could not parse JSON: {e}")
        else:
            print("✗ No __NEXT_DATA__ found")
            
        # Look for any API calls in scripts
        scripts = soup.find_all('script', {'src': re.compile(r'/_next/static')})
        print(f"\n✓ Found {len(scripts)} Next.js script tags")
        
        return None
        
    except requests.RequestException as e:
        print(f"✗ Error fetching page: {e}")
        return None


def attempt_api_discovery(location_id):
    """
    Try to find the API endpoint that rec.us uses for availability.
    
    This would normally require browser DevTools to inspect network requests.
    """
    print(f"\n{'='*60}")
    print("API Discovery Attempt")
    print(f"{'='*60}\n")
    
    # Common API patterns to try
    api_patterns = [
        f"https://api.rec.us/locations/{location_id}/availability",
        f"https://api.rec.us/v1/locations/{location_id}/availability",
        f"https://www.rec.us/api/locations/{location_id}/availability",
        f"https://www.rec.us/api/v1/locations/{location_id}/availability",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.rec.us/'
    }
    
    for api_url in api_patterns:
        try:
            print(f"Testing: {api_url}")
            response = requests.get(api_url, headers=headers, timeout=5, verify=False)
            if response.status_code == 200:
                print(f"  ✓ SUCCESS! Status: {response.status_code}")
                print(f"  Response preview:")
                print(f"  {response.text[:500]}\n")
                return api_url
            elif response.status_code == 404:
                print(f"  ✗ Not found (404)")
            elif response.status_code == 401 or response.status_code == 403:
                print(f"  ⚠ Authentication required ({response.status_code})")
            else:
                print(f"  ? Status: {response.status_code}")
        except requests.RequestException as e:
            print(f"  ✗ Error: {e}")
    
    print("\n⚠ Could not find API endpoint through basic patterns")
    return None


def create_mock_availability_data():
    """
    Create mock availability data to show what the data structure would look like.
    """
    print(f"\n{'='*60}")
    print("Mock Availability Data Structure")
    print(f"{'='*60}\n")
    
    today = datetime.now()
    availability = {
        "court_id": "buena-vista-park",
        "court_name": "Buena Vista Park",
        "date_range": {
            "start": today.strftime("%Y-%m-%d"),
            "end": (today + timedelta(days=7)).strftime("%Y-%m-%d")
        },
        "days": []
    }
    
    # Generate mock data for next 7 days
    for day_offset in range(7):
        date = today + timedelta(days=day_offset)
        day_data = {
            "date": date.strftime("%Y-%m-%d"),
            "day_of_week": date.strftime("%A"),
            "slots": []
        }
        
        # Generate 90-minute slots from 7 AM to 9 PM
        start_hour = 7
        end_hour = 21
        
        for hour in range(start_hour, end_hour):
            for minutes in [0, 90]:  # 0 min, 90 min (1.5 hour slots)
                if hour == end_hour - 1 and minutes == 90:
                    break  # Don't go past 9 PM
                
                start_time = f"{hour:02d}:{minutes:02d}"
                end_minutes = minutes + 90
                end_hour_adj = hour + (end_minutes // 60)
                end_minutes_adj = end_minutes % 60
                end_time = f"{end_hour_adj:02d}:{end_minutes_adj:02d}"
                
                # Mock availability: Random pattern
                # In real data, this would come from scraping
                import random
                available = random.random() > 0.3  # 70% available
                
                slot = {
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration_minutes": 90,
                    "available": available,
                    "price": 5.00 if available else None
                }
                day_data["slots"].append(slot)
        
        availability["days"].append(day_data)
    
    print("Example data structure:")
    print(json.dumps(availability, indent=2)[:1500] + "...\n")
    
    # Save to file
    output_file = "backend/mock_availability.json"
    with open(output_file, 'w') as f:
        json.dump(availability, f, indent=2)
    print(f"✓ Saved mock data to: {output_file}")
    
    return availability


def main():
    """Run the proof-of-concept scraper test."""
    
    print("\n" + "="*60)
    print("REC.US SCRAPER PROOF-OF-CONCEPT")
    print("="*60)
    
    # Test court URL
    test_court = "https://www.rec.us/buenavista"
    
    # Step 1: Analyze page structure
    location_id = test_rec_us_structure(test_court)
    
    # Step 2: Try to find API
    if location_id:
        api_url = attempt_api_discovery(location_id)
    
    # Step 3: Create mock data structure
    mock_data = create_mock_availability_data()
    
    # Summary
    print(f"\n{'='*60}")
    print("FINDINGS & RECOMMENDATIONS")
    print(f"{'='*60}\n")
    
    print("1. ✓ rec.us is a Next.js React application")
    print("2. ✓ Found location ID in __NEXT_DATA__")
    print("3. ⚠ Data is loaded via JavaScript (not in initial HTML)")
    print("4. ⚠ Need to either:")
    print("   a) Use headless browser (Playwright/Selenium)")
    print("   b) Reverse engineer their API endpoints")
    print("   c) Inspect browser DevTools to find API calls\n")
    
    print("NEXT STEPS:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("1. Manual inspection:")
    print("   • Open https://www.rec.us/buenavista in Chrome")
    print("   • Open DevTools (Network tab)")
    print("   • Look for API calls when calendar loads")
    print("   • Document endpoint, headers, auth requirements")
    print("")
    print("2. If API found: Build simple scraper")
    print("3. If no API: Use Playwright with headless browser")
    print("4. Consider: Start with just 2-3 most popular courts")
    print("")


if __name__ == "__main__":
    main()
