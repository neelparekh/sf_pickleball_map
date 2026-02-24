"""Manual data entry for SF pickleball courts based on website content."""

from models import Court, CourtStorage


def populate_sample_data():
    """Populate storage with SF pickleball court data."""
    storage = CourtStorage()
    
    # Real data from SF Recreation and Parks website - Outdoor Courts with coordinates
    courts_data = [
        {
            'id': 'alta-plaza-park',
            'name': 'Alta Plaza Park',
            'address': 'Clay St & Steiner St, San Francisco, CA',
            'neighborhood': 'Pacific Heights',
            'latitude': 37.7916,
            'longitude': -122.4366,
            'num_courts': 2,
            'nets_provided': True,
            'amenities': ['Open Play'],
            'hours_of_operation': '6:00 AM - 10:00 PM daily',
            'pricing': 'Free - No reservations, open play only',
            'reservation_url': '',
            'permit_required': False
        },
        {
            'id': 'buena-vista-park',
            'name': 'Buena Vista Park',
            'address': 'Haight St & Buena Vista Ave E, San Francisco, CA',
            'neighborhood': 'Haight',
            'latitude': 37.7685,
            'longitude': -122.4396,
            'num_courts': 4,
            'nets_provided': False,
            'amenities': ['Reservable'],
            'hours_of_operation': '6:00 AM - 10:00 PM daily',
            'pricing': '$5/hour (90-minute reservations)',
            'reservation_url': 'https://www.rec.us/buenavista',
            'permit_required': False
        },
        {
            'id': 'carl-larsen-playground',
            'name': 'Carl Larsen Playground',
            'address': '19th Ave & Wawona St, San Francisco, CA',
            'neighborhood': 'Sunset',
            'latitude': 37.7339,
            'longitude': -122.4755,
            'num_courts': 8,
            'nets_provided': True,
            'amenities': ['Open Play', 'Tournaments'],
            'hours_of_operation': '7:00 AM - 9:00 PM daily',
            'pricing': 'Free for open play; Permit required for tournaments',
            'reservation_url': 'https://sfrecpark.org/1591/Reservable-Pickleball-Courts',
            'permit_required': True
        },
        {
            'id': 'crocker-amazon-playground',
            'name': 'Crocker Amazon Playground',
            'address': 'Moscow St & Geneva Ave, San Francisco, CA',
            'neighborhood': 'Excelsior',
            'latitude': 37.7120,
            'longitude': -122.4273,
            'num_courts': 4,
            'nets_provided': True,
            'amenities': ['Reservable'],
            'hours_of_operation': '7:00 AM - 9:00 PM daily',
            'pricing': '$5/hour (90-minute reservations)',
            'reservation_url': 'https://www.rec.us/crockeramazon',
            'permit_required': False
        },
        {
            'id': 'east-cut-crossing',
            'name': 'East Cut Crossing',
            'address': '1st St & Folsom St, San Francisco, CA',
            'neighborhood': 'SoMa',
            'latitude': 37.7881,
            'longitude': -122.3927,
            'num_courts': 2,
            'nets_provided': True,
            'amenities': ['Open Play (Fri & Sun only)'],
            'hours_of_operation': 'Fridays & Sundays: 8:00 AM - 6:00 PM',
            'pricing': 'Free - No reservations, open play only',
            'reservation_url': '',
            'permit_required': False
        },
        {
            'id': 'george-christopher-playground',
            'name': 'George Christopher Playground',
            'address': 'Diamond Heights Blvd & Gold Mine Dr, San Francisco, CA',
            'neighborhood': 'Diamond Heights',
            'latitude': 37.7416,
            'longitude': -122.4453,
            'num_courts': 2,
            'nets_provided': False,
            'amenities': ['Open Play'],
            'hours_of_operation': '6:00 AM - 10:00 PM daily',
            'pricing': 'Free - No reservations, open play only',
            'reservation_url': '',
            'permit_required': False
        },
        {
            'id': 'goldman-tennis-center',
            'name': 'Goldman Tennis Center (GGP)',
            'address': 'Golden Gate Park, San Francisco, CA',
            'neighborhood': 'Golden Gate Park',
            'latitude': 37.7694,
            'longitude': -122.4862,
            'num_courts': 5,
            'nets_provided': True,
            'amenities': ['Reservations Only', 'Fees Apply'],
            'hours_of_operation': '7:00 AM - 9:00 PM daily',
            'pricing': 'Paid facility - See website for rates',
            'reservation_url': 'https://gtc.clubautomation.com/',
            'permit_required': True
        },
        {
            'id': 'jackson-playground',
            'name': 'Jackson Playground',
            'address': '17th St & Arkansas St, San Francisco, CA',
            'neighborhood': 'Potrero Hill',
            'latitude': 37.7628,
            'longitude': -122.3980,
            'num_courts': 2,
            'nets_provided': False,
            'amenities': ['Reservable'],
            'hours_of_operation': '6:00 AM - 10:00 PM daily',
            'pricing': '$5/hour (60-minute reservations)',
            'reservation_url': 'https://www.rec.us/jackson',
            'permit_required': False
        },
        {
            'id': 'louis-sutter-playground',
            'name': 'Louis Sutter Playground',
            'address': 'Gough St & Turk St, San Francisco, CA',
            'neighborhood': 'Western Addition',
            'latitude': 37.7819,
            'longitude': -122.4228,
            'num_courts': 6,
            'nets_provided': True,
            'amenities': ['Open Play', 'Tournaments'],
            'hours_of_operation': '7:00 AM - 9:00 PM daily',
            'pricing': 'Free for open play; Permit required for tournaments',
            'reservation_url': 'https://sfrecpark.org/1591/Reservable-Pickleball-Courts',
            'permit_required': True
        },
        {
            'id': 'moscone-playground',
            'name': 'Moscone Playground',
            'address': 'Chestnut St & Laguna St, San Francisco, CA',
            'neighborhood': 'Marina',
            'latitude': 37.8002,
            'longitude': -122.4304,
            'num_courts': 6,
            'nets_provided': True,
            'amenities': ['Reservable', 'Open Play', 'Tournaments'],
            'hours_of_operation': '7:00 AM - 9:00 PM daily',
            'pricing': '$5/hour (90-minute reservations); Permit for tournaments',
            'reservation_url': 'https://www.rec.us/moscone',
            'permit_required': True
        },
        {
            'id': 'parkside-square',
            'name': 'Parkside Square',
            'address': '28th Ave & Vicente St, San Francisco, CA',
            'neighborhood': 'Parkside',
            'latitude': 37.7379,
            'longitude': -122.4884,
            'num_courts': 8,
            'nets_provided': False,
            'amenities': ['Reservable'],
            'hours_of_operation': '6:00 AM - 10:00 PM daily',
            'pricing': '$5/hour (90-minute reservations)',
            'reservation_url': 'https://www.rec.us/parkside',
            'permit_required': False
        },
        {
            'id': 'presidio-wall-playground',
            'name': 'Presidio Wall Playground',
            'address': 'Lyon St & Greenwich St, San Francisco, CA',
            'neighborhood': 'Presidio',
            'latitude': 37.7979,
            'longitude': -122.4469,
            'num_courts': 6,
            'nets_provided': True,
            'amenities': ['Reservable', 'Open Play', 'Tournaments'],
            'hours_of_operation': '7:00 AM - 9:00 PM daily',
            'pricing': '$5/hour (90-minute reservations); Permit for tournaments',
            'reservation_url': 'https://rec.us/presidiowall',
            'permit_required': True
        },
        {
            'id': 'richmond-playground',
            'name': 'Richmond Playground',
            'address': '5th Ave & Balboa St, San Francisco, CA',
            'neighborhood': 'Richmond',
            'latitude': 37.7762,
            'longitude': -122.4636,
            'num_courts': 2,
            'nets_provided': True,
            'amenities': ['Reservable'],
            'hours_of_operation': '6:00 AM - 10:00 PM daily',
            'pricing': '$5/hour (60-minute reservations)',
            'reservation_url': 'http://rec.us/richmond',
            'permit_required': False
        },
        {
            'id': 'rossi-playground',
            'name': 'Rossi Playground',
            'address': 'Arguello Blvd & Anza St, San Francisco, CA',
            'neighborhood': 'Richmond',
            'latitude': 37.7791,
            'longitude': -122.4594,
            'num_courts': 9,
            'nets_provided': True,
            'amenities': ['Reservable', 'Open Play', 'Tournaments'],
            'hours_of_operation': '7:00 AM - 9:00 PM daily',
            'pricing': '$5/hour (90-minute reservations); Permit for tournaments',
            'reservation_url': 'https://rec.us/rossi',
            'permit_required': True
        },
        {
            'id': 'states-street-playground',
            'name': 'States Street Playground',
            'address': 'States St & 20th St, San Francisco, CA',
            'neighborhood': 'Bernal Heights',
            'latitude': 37.7418,
            'longitude': -122.4085,
            'num_courts': 2,
            'nets_provided': False,
            'amenities': ['Open Play'],
            'hours_of_operation': '6:00 AM - 10:00 PM daily',
            'pricing': 'Free - No reservations, open play only',
            'reservation_url': '',
            'permit_required': False
        },
        {
            'id': 'stern-grove',
            'name': 'Stern Grove',
            'address': '19th Ave & Sloat Blvd, San Francisco, CA',
            'neighborhood': 'Sunset',
            'latitude': 37.7344,
            'longitude': -122.4744,
            'num_courts': 6,
            'nets_provided': True,
            'amenities': ['Reservable'],
            'hours_of_operation': '7:00 AM - 9:00 PM daily',
            'pricing': '$5/hour (90-minute reservations)',
            'reservation_url': 'https://www.rec.us/sterngrove',
            'permit_required': False
        },
        {
            'id': 'upper-noe-rec-center',
            'name': 'Upper Noe Rec Center',
            'address': '295 Day St, San Francisco, CA',
            'neighborhood': 'Noe Valley',
            'latitude': 37.7416,
            'longitude': -122.4294,
            'num_courts': 2,
            'nets_provided': True,
            'amenities': ['Reservable', 'Open Play Tue/Thu 10:30am-1:30pm'],
            'hours_of_operation': '6:00 AM - 10:00 PM daily (Open play Tue/Thu 10:30am-1:30pm)',
            'pricing': '$5/hour (60-minute reservations)',
            'reservation_url': 'https://www.rec.us/uppernoe',
            'permit_required': False
        },
    ]
    
    for court_data in courts_data:
        court = Court(**court_data)
        storage.add_court(court)
    
    storage.save()
    print(f"Added {len(courts_data)} pickleball courts to storage")
    print(f"Neighborhoods: {', '.join(storage.get_neighborhoods())}")


if __name__ == "__main__":
    populate_sample_data()
