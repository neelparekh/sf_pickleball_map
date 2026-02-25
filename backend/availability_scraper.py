"""
Real-time availability scraper for SF Rec & Parks courts.

Fetches court availability from api.rec.us and provides clean API.
"""

import requests
import warnings
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


class RecUsAvailabilityScraper:
    """Scraper for rec.us court availability."""
    
    BASE_URL = "https://api.rec.us/v1/locations"
    
    def __init__(self):
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://www.rec.us/'
        }
    
    def fetch_schedule(self, location_id: str, start_date: str = None) -> Dict:
        """
        Fetch schedule for a location.
        
        Args:
            location_id: UUID of the location
            start_date: Date in YYYY-MM-DD format (defaults to today)
        
        Returns:
            Dict with schedule data
        """
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        url = f"{self.BASE_URL}/{location_id}/schedule"
        params = {'startDate': start_date}
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching schedule for {location_id}: {e}")
            return {}
    
    def parse_availability(self, schedule_data: Dict, date: str = None) -> List[Dict]:
        """
        Parse schedule data into availability slots.
        
        Args:
            schedule_data: Raw schedule data from API
            date: Date to parse (YYYY-MM-DD), defaults to today
        
        Returns:
            List of availability slots with time and status
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        date_key = date.replace("-", "")  # Convert to YYYYMMDD
        
        dates = schedule_data.get('dates', {})
        courts_data = dates.get(date_key, [])
        
        availability = []
        
        for court in courts_data:
            court_number = court.get('courtNumber', 'Unknown')
            sports = court.get('sports', [])
            sport_names = [s['name'] for s in sports]
            schedule = court.get('schedule', {})
            
            for time_range, details in schedule.items():
                start_time, end_time = time_range.split(', ')
                reference_type = details.get('referenceType', '')
                
                # Determine availability
                if reference_type == 'RESERVABLE':
                    available = True
                    status = 'available'
                elif reference_type == 'RESERVATION':
                    available = False
                    status = 'booked'
                elif reference_type == 'OPEN':
                    available = True
                    status = 'open_play'
                else:
                    available = False
                    status = 'unknown'
                
                slot = {
                    'court': court_number,
                    'sports': sport_names,
                    'start_time': start_time,
                    'end_time': end_time,
                    'available': available,
                    'status': status,
                    'reference_type': reference_type
                }
                
                availability.append(slot)
        
        return availability
    
    def get_availability_for_court(
        self,
        location_id: str,
        court_name: str,
        start_date: str = None,
        days: int = 7
    ) -> Dict:
        """
        Get availability for a specific court over multiple days.
        
        Args:
            location_id: UUID of the location
            court_name: Name of the court (for display)
            start_date: Start date (YYYY-MM-DD)
            days: Number of days to fetch
        
        Returns:
            Dict with availability by date
        """
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        
        result = {
            'court_id': location_id,
            'court_name': court_name,
            'date_range': {
                'start': start_date,
                'end': (start + timedelta(days=days-1)).strftime("%Y-%m-%d")
            },
            'days': []
        }
        
        for day_offset in range(days):
            date = start + timedelta(days=day_offset)
            date_str = date.strftime("%Y-%m-%d")
            
            # Fetch schedule for this date
            schedule_data = self.fetch_schedule(location_id, date_str)
            availability = self.parse_availability(schedule_data, date_str)
            
            # Filter for pickleball courts only
            pickleball_slots = [
                slot for slot in availability
                if 'Pickleball' in slot.get('sports', [])
            ]
            
            day_data = {
                'date': date_str,
                'day_of_week': date.strftime("%A"),
                'slots': pickleball_slots,
                'total_slots': len(pickleball_slots),
                'available_slots': len([s for s in pickleball_slots if s['available']])
            }
            
            result['days'].append(day_data)
        
        return result
    
    def check_availability_for_time_range(
        self,
        location_id: str,
        date: str,
        start_time: str,
        end_time: str
    ) -> bool:
        """
        Check if courts are available during a specific time range.
        
        Args:
            location_id: UUID of the location
            date: Date to check (YYYY-MM-DD)
            start_time: Start time (HH:MM)
            end_time: End time (HH:MM)
        
        Returns:
            True if any courts available during that time
        """
        schedule_data = self.fetch_schedule(location_id, date)
        availability = self.parse_availability(schedule_data, date)
        
        # Filter for pickleball and available slots
        for slot in availability:
            if not slot['available'] or 'Pickleball' not in slot.get('sports', []):
                continue
            
            slot_start = slot['start_time']
            slot_end = slot['end_time']
            
            # Check if slot overlaps with requested time range
            if slot_start <= start_time and slot_end >= end_time:
                return True
        
        return False


def main():
    """Test the scraper."""
    scraper = RecUsAvailabilityScraper()
    
    # Test with Buena Vista Park
    location_id = "3f842b1e-13f9-447d-ab12-62b62d954d3e"
    
    print("Testing Buena Vista Park availability scraper...\n")
    
    # Get today's schedule
    today = datetime.now().strftime("%Y-%m-%d")
    schedule = scraper.fetch_schedule(location_id, today)
    
    print(f"✓ Fetched schedule for {today}")
    print(f"  Dates available: {list(schedule.get('dates', {}).keys())}")
    
    # Parse availability
    availability = scraper.parse_availability(schedule, today)
    print(f"\n✓ Found {len(availability)} total slots")
    
    # Show pickleball slots
    pickleball_slots = [s for s in availability if 'Pickleball' in s.get('sports', [])]
    print(f"  Pickleball slots: {len(pickleball_slots)}")
    
    available_count = len([s for s in pickleball_slots if s['available']])
    print(f"  Available: {available_count}")
    print(f"  Booked: {len(pickleball_slots) - available_count}")
    
    # Show first few slots
    print("\nSample slots:")
    for slot in pickleball_slots[:5]:
        status_icon = "✓" if slot['available'] else "✗"
        print(f"  {status_icon} {slot['court']}: {slot['start_time']}-{slot['end_time']} ({slot['status']})")
    
    # Get 7-day availability
    print(f"\n\nFetching 7-day availability...")
    week_data = scraper.get_availability_for_court(
        location_id,
        "Buena Vista Park",
        today,
        days=7
    )
    
    print(f"✓ Got data for {len(week_data['days'])} days:")
    for day in week_data['days']:
        print(f"  {day['date']} ({day['day_of_week']}): {day['available_slots']}/{day['total_slots']} available")
    
    # Test time range check
    print(f"\n\nChecking specific time range...")
    has_availability = scraper.check_availability_for_time_range(
        location_id,
        today,
        "15:00",
        "17:00"
    )
    print(f"  3-5 PM today: {'✓ Available' if has_availability else '✗ Not available'}")


if __name__ == "__main__":
    main()
