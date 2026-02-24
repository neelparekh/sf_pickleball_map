/**
 * Leaflet map integration for SF Pickleball Courts
 */

let map;
let markersLayer;
let currentMarkers = [];

/**
 * Initialize the Leaflet map
 */
function initMap() {
    // Create map centered on San Francisco
    map = L.map('map').setView([37.7749, -122.4194], 12);
    
    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Create a layer group for markers
    markersLayer = L.layerGroup().addTo(map);
    
    console.log('Map initialized');
}

/**
 * Update map markers based on filtered courts
 */
function updateMapMarkers(courts) {
    // Clear existing markers
    markersLayer.clearLayers();
    currentMarkers = [];
    
    if (!courts || courts.length === 0) {
        return;
    }
    
    // Create markers for each court
    courts.forEach(court => {
        if (court.latitude && court.longitude) {
            const marker = createMarker(court);
            currentMarkers.push(marker);
            markersLayer.addLayer(marker);
        }
    });
    
    // Fit map to show all markers
    if (currentMarkers.length > 0) {
        const group = new L.featureGroup(currentMarkers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

/**
 * Create a marker for a court
 */
function createMarker(court) {
    // Custom icon based on whether nets are provided
    const iconColor = court.nets_provided ? '#4a7c59' : '#ff9800';
    
    const icon = L.divIcon({
        className: 'custom-marker',
        html: `
            <div style="
                background-color: ${iconColor};
                width: 30px;
                height: 30px;
                border-radius: 50% 50% 50% 0;
                transform: rotate(-45deg);
                border: 3px solid white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            "></div>
        `,
        iconSize: [30, 30],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30]
    });
    
    // Create marker
    const marker = L.marker([court.latitude, court.longitude], { icon })
        .bindPopup(createPopupContent(court));
    
    // Add click event to show details
    marker.on('click', () => {
        showCourtDetails(court);
    });
    
    return marker;
}

/**
 * Create popup content for a marker
 */
function createPopupContent(court) {
    return `
        <div class="popup-content">
            <div class="popup-title">${court.name}</div>
            <div class="popup-info">
                <p><strong>📍</strong> ${court.neighborhood || 'N/A'}</p>
                <p><strong>🎾</strong> ${court.num_courts || 'N/A'} court${court.num_courts !== 1 ? 's' : ''}</p>
                <p>
                    <span class="badge ${court.nets_provided ? '' : 'no-nets'}">
                        ${court.nets_provided ? '✓ Nets Provided' : '✗ BYO Nets'}
                    </span>
                </p>
            </div>
        </div>
    `;
}

/**
 * Fly to a specific court on the map
 */
function flyToCourt(court) {
    if (court.latitude && court.longitude) {
        map.flyTo([court.latitude, court.longitude], 15, {
            duration: 1
        });
    }
}

/**
 * Get user's current location (optional feature)
 */
function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLat = position.coords.latitude;
                const userLng = position.coords.longitude;
                
                // Add a marker for user's location
                L.marker([userLat, userLng], {
                    icon: L.divIcon({
                        className: 'user-location-marker',
                        html: '<div style="background: #2196F3; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>',
                        iconSize: [20, 20]
                    })
                }).addTo(map)
                    .bindPopup('You are here');
                
                // Center map on user location
                map.setView([userLat, userLng], 13);
            },
            (error) => {
                console.log('Geolocation error:', error);
            }
        );
    }
}
