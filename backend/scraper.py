"""Web scraper for SF Recreation pickleball courts."""

import requests
from bs4 import BeautifulSoup
import re
import time
from models import Court, CourtStorage


class PickleballScraper:
    """Scrapes pickleball court data from SF Recreation website."""
    
    def __init__(self):
        self.base_url = "https://sfrecpark.org"
        self.courts_url = "https://sfrecpark.org/1772/Where-to-Play-Pickleball"
        self.storage = CourtStorage()
        self.courts_data = []
    
    def scrape(self):
        """Main scraping method."""
        print("Fetching pickleball courts data...")
        
        try:
            response = requests.get(self.courts_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Parse the page to find court information
            # The website likely has court data in tables, lists, or specific divs
            self.parse_courts(soup)
            
            print(f"Found {len(self.courts_data)} courts")
            
            # Save courts to storage
            for court_data in self.courts_data:
                court = Court(**court_data)
                self.storage.add_court(court)
            
            self.storage.save()
            print(f"Saved {len(self.courts_data)} courts to storage")
            
        except Exception as e:
            print(f"Error scraping data: {e}")
            raise
    
    def parse_courts(self, soup):
        """Parse court information from the page."""
        # Look for court information in various possible locations
        
        # Try to find tables with court data
        tables = soup.find_all('table')
        if tables:
            self.parse_table_data(tables)
        
        # Try to find lists with court data
        lists = soup.find_all(['ul', 'ol'])
        if lists and not self.courts_data:
            self.parse_list_data(lists)
        
        # Try to find divs with specific classes or patterns
        if not self.courts_data:
            self.parse_content_divs(soup)
    
    def parse_table_data(self, tables):
        """Parse court data from HTML tables."""
        for table in tables:
            rows = table.find_all('tr')
            
            # Skip header row
            for i, row in enumerate(rows[1:] if len(rows) > 1 else rows, 1):
                cells = row.find_all(['td', 'th'])
                
                if len(cells) >= 2:
                    court_data = self.extract_court_info_from_cells(cells, i)
                    if court_data:
                        self.courts_data.append(court_data)
    
    def parse_list_data(self, lists):
        """Parse court data from HTML lists."""
        for ul in lists:
            items = ul.find_all('li')
            
            for i, item in enumerate(items, 1):
                text = item.get_text(strip=True)
                
                # Skip empty or very short items
                if len(text) < 10:
                    continue
                
                court_data = self.extract_court_info_from_text(text, i)
                if court_data:
                    self.courts_data.append(court_data)
    
    def parse_content_divs(self, soup):
        """Parse court data from content divs."""
        # Look for editor content or main content areas
        content_areas = soup.find_all(['div'], class_=re.compile(r'(editor|content|body)', re.I))
        
        for content in content_areas:
            # Get all text and try to parse it
            text = content.get_text()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Try to find patterns that indicate court information
            for i, line in enumerate(lines):
                if self.looks_like_court_name(line):
                    court_data = self.extract_court_info_from_lines(lines, i)
                    if court_data:
                        self.courts_data.append(court_data)
    
    def extract_court_info_from_cells(self, cells, index):
        """Extract court information from table cells."""
        # Common table formats: Name | Address | Details
        court_name = cells[0].get_text(strip=True)
        
        if not court_name or len(court_name) < 3:
            return None
        
        address = cells[1].get_text(strip=True) if len(cells) > 1 else ""
        details = cells[2].get_text(strip=True) if len(cells) > 2 else ""
        
        # Check for nets provided
        nets_provided = self.check_nets_provided(details + " " + str(cells))
        
        return {
            'id': self.generate_id(court_name),
            'name': court_name,
            'address': address,
            'neighborhood': self.extract_neighborhood(address),
            'nets_provided': nets_provided,
            'amenities': self.extract_amenities(details)
        }
    
    def extract_court_info_from_text(self, text, index):
        """Extract court information from plain text."""
        # Look for patterns like "Court Name - Address" or "Court Name, Address"
        
        # Try to split by common separators
        parts = re.split(r'[-–—,]', text, maxsplit=1)
        
        if len(parts) >= 2:
            court_name = parts[0].strip()
            rest = parts[1].strip()
        else:
            court_name = text.strip()
            rest = ""
        
        # Check for nets provided
        nets_provided = self.check_nets_provided(text)
        
        return {
            'id': self.generate_id(court_name),
            'name': court_name,
            'address': rest,
            'neighborhood': self.extract_neighborhood(rest),
            'nets_provided': nets_provided,
            'amenities': self.extract_amenities(text)
        }
    
    def extract_court_info_from_lines(self, lines, start_index):
        """Extract court info from multiple lines."""
        court_name = lines[start_index]
        
        # Look at next few lines for address and details
        address = ""
        details = ""
        
        for i in range(start_index + 1, min(start_index + 4, len(lines))):
            line = lines[i]
            if self.looks_like_address(line):
                address = line
            elif len(line) > 10:
                details += " " + line
        
        nets_provided = self.check_nets_provided(details + " " + address)
        
        return {
            'id': self.generate_id(court_name),
            'name': court_name,
            'address': address,
            'neighborhood': self.extract_neighborhood(address),
            'nets_provided': nets_provided,
            'amenities': self.extract_amenities(details)
        }
    
    def looks_like_court_name(self, text):
        """Check if text looks like a court name."""
        # Court names often contain words like "Park", "Recreation", "Center"
        keywords = ['park', 'playground', 'recreation', 'center', 'courts']
        text_lower = text.lower()
        
        return any(keyword in text_lower for keyword in keywords) and len(text) < 100
    
    def looks_like_address(self, text):
        """Check if text looks like an address."""
        # Addresses often contain street numbers and street names
        return bool(re.search(r'\d+\s+\w+\s+(Street|St|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Road|Rd)', text, re.I))
    
    def check_nets_provided(self, text):
        """Check if nets are provided based on text."""
        text_lower = text.lower()
        
        # Positive indicators
        if any(phrase in text_lower for phrase in ['nets provided', 'nets available', 'has nets', 'with nets']):
            return True
        
        # Negative indicators
        if any(phrase in text_lower for phrase in ['no nets', 'bring nets', 'byonet', 'byo net']):
            return False
        
        # Default to False if not specified
        return False
    
    def extract_neighborhood(self, address):
        """Extract neighborhood from address."""
        # SF neighborhoods - could be expanded
        neighborhoods = [
            'Mission', 'Castro', 'Noe Valley', 'Bernal Heights', 'Potrero Hill',
            'Sunset', 'Richmond', 'Haight', 'Marina', 'Pacific Heights',
            'North Beach', 'Chinatown', 'Financial District', 'SoMa',
            'Russian Hill', 'Nob Hill', 'Telegraph Hill', 'Excelsior',
            'Bayview', 'Visitacion Valley', 'Ingleside', 'Outer Mission'
        ]
        
        address_lower = address.lower()
        for neighborhood in neighborhoods:
            if neighborhood.lower() in address_lower:
                return neighborhood
        
        return ""
    
    def extract_amenities(self, text):
        """Extract amenities from text."""
        amenities = []
        text_lower = text.lower()
        
        amenity_keywords = {
            'restrooms': ['restroom', 'bathroom'],
            'parking': ['parking'],
            'water': ['water fountain', 'drinking water'],
            'lights': ['lights', 'lighting', 'lit'],
            'benches': ['bench', 'seating'],
        }
        
        for amenity, keywords in amenity_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                amenities.append(amenity)
        
        return amenities
    
    def generate_id(self, name):
        """Generate a unique ID from court name."""
        # Convert to lowercase, replace spaces with hyphens, remove special chars
        id_str = name.lower()
        id_str = re.sub(r'[^\w\s-]', '', id_str)
        id_str = re.sub(r'[-\s]+', '-', id_str)
        return id_str.strip('-')


def main():
    """Run the scraper."""
    scraper = PickleballScraper()
    scraper.scrape()
    print("Scraping complete!")


if __name__ == "__main__":
    main()
