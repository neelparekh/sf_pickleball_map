"""Data models for pickleball courts."""

import json
from typing import List, Dict, Optional
from pathlib import Path


class Court:
    """Represents a pickleball court location."""
    
    def __init__(
        self,
        id: str,
        name: str,
        address: str,
        neighborhood: str = "",
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        hours: str = "",
        num_courts: int = 0,
        nets_provided: bool = False,
        amenities: List[str] = None
    ):
        self.id = id
        self.name = name
        self.address = address
        self.neighborhood = neighborhood
        self.latitude = latitude
        self.longitude = longitude
        self.hours = hours
        self.num_courts = num_courts
        self.nets_provided = nets_provided
        self.amenities = amenities or []
    
    def to_dict(self) -> Dict:
        """Convert court to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'neighborhood': self.neighborhood,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'hours': self.hours,
            'num_courts': self.num_courts,
            'nets_provided': self.nets_provided,
            'amenities': self.amenities
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Court':
        """Create court from dictionary."""
        return cls(**data)


class CourtStorage:
    """Handles storage and retrieval of court data."""
    
    def __init__(self, data_file: str = "data/courts.json"):
        self.data_file = Path(data_file)
        self.courts: List[Court] = []
        self.load()
    
    def load(self):
        """Load courts from JSON file."""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.courts = [Court.from_dict(court_data) for court_data in data]
    
    def save(self):
        """Save courts to JSON file."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump([court.to_dict() for court in self.courts], f, indent=2)
    
    def add_court(self, court: Court):
        """Add a court to storage."""
        self.courts.append(court)
    
    def get_all(self) -> List[Dict]:
        """Get all courts as dictionaries."""
        return [court.to_dict() for court in self.courts]
    
    def get_by_id(self, court_id: str) -> Optional[Dict]:
        """Get a specific court by ID."""
        for court in self.courts:
            if court.id == court_id:
                return court.to_dict()
        return None
    
    def filter_courts(
        self,
        search: Optional[str] = None,
        neighborhood: Optional[str] = None,
        nets_provided: Optional[bool] = None
    ) -> List[Dict]:
        """Filter courts based on criteria."""
        filtered = self.courts
        
        if search:
            search_lower = search.lower()
            filtered = [c for c in filtered if search_lower in c.name.lower()]
        
        if neighborhood:
            filtered = [c for c in filtered if c.neighborhood == neighborhood]
        
        if nets_provided is not None:
            filtered = [c for c in filtered if c.nets_provided == nets_provided]
        
        return [court.to_dict() for court in filtered]
    
    def get_neighborhoods(self) -> List[str]:
        """Get unique list of neighborhoods."""
        neighborhoods = set(c.neighborhood for c in self.courts if c.neighborhood)
        return sorted(list(neighborhoods))
