/**
 * Main application logic for SF Pickleball Courts Finder
 */

// Data Configuration - Use relative paths for static JSON files
const DATA_BASE_URL = 'data';

// Application State
let allCourts = [];
let filteredCourts = [];
let neighborhoods = [];

// DOM Elements
const searchInput = document.getElementById('searchInput');
const neighborhoodFilter = document.getElementById('neighborhoodFilter');
const netsFilter = document.getElementById('netsFilter');
const clearFiltersBtn = document.getElementById('clearFilters');
const courtCountEl = document.getElementById('courtCount');
const sidebar = document.getElementById('sidebar');
const closeSidebarBtn = document.getElementById('closeSidebar');
const courtDetailsEl = document.getElementById('courtDetails');

/**
 * Initialize the application
 */
async function init() {
    try {
        // Load courts and neighborhoods
        await Promise.all([loadCourts(), loadNeighborhoods()]);
        
        // Set up event listeners
        setupEventListeners();
        
        // Initialize the map
        initMap();
        
        // Update display
        updateDisplay();
    } catch (error) {
        console.error('Initialization error:', error);
        showError('Failed to load application data. Please refresh the page.');
    }
}

/**
 * Load all courts from static JSON file
 */
async function loadCourts() {
    try {
        const response = await fetch(`${DATA_BASE_URL}/courts.json`);
        const data = await response.json();
        
        if (data.success) {
            allCourts = data.courts;
            filteredCourts = [...allCourts];
            return allCourts;
        } else {
            throw new Error(data.error || 'Failed to load courts');
        }
    } catch (error) {
        console.error('Error loading courts:', error);
        throw error;
    }
}

/**
 * Load neighborhoods from static JSON file
 */
async function loadNeighborhoods() {
    try {
        const response = await fetch(`${DATA_BASE_URL}/neighborhoods.json`);
        const data = await response.json();
        
        if (data.success) {
            neighborhoods = data.neighborhoods;
            populateNeighborhoodFilter();
            return neighborhoods;
        } else {
            throw new Error(data.error || 'Failed to load neighborhoods');
        }
    } catch (error) {
        console.error('Error loading neighborhoods:', error);
        throw error;
    }
}

/**
 * Populate the neighborhood filter dropdown
 */
function populateNeighborhoodFilter() {
    neighborhoods.forEach(neighborhood => {
        const option = document.createElement('option');
        option.value = neighborhood;
        option.textContent = neighborhood;
        neighborhoodFilter.appendChild(option);
    });
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    searchInput.addEventListener('input', debounce(applyFilters, 300));
    neighborhoodFilter.addEventListener('change', applyFilters);
    netsFilter.addEventListener('change', applyFilters);
    clearFiltersBtn.addEventListener('click', clearFilters);
    closeSidebarBtn.addEventListener('click', closeSidebar);
}

/**
 * Apply filters to the courts list
 */
function applyFilters() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const selectedNeighborhood = neighborhoodFilter.value;
    const onlyNets = netsFilter.checked;
    
    filteredCourts = allCourts.filter(court => {
        // Search filter
        if (searchTerm && !court.name.toLowerCase().includes(searchTerm)) {
            return false;
        }
        
        // Neighborhood filter
        if (selectedNeighborhood && court.neighborhood !== selectedNeighborhood) {
            return false;
        }
        
        // Nets filter
        if (onlyNets && !court.nets_provided) {
            return false;
        }
        
        return true;
    });
    
    updateDisplay();
}

/**
 * Clear all filters
 */
function clearFilters() {
    searchInput.value = '';
    neighborhoodFilter.value = '';
    netsFilter.checked = false;
    filteredCourts = [...allCourts];
    updateDisplay();
}

/**
 * Update the display with filtered results
 */
function updateDisplay() {
    // Update court count
    const count = filteredCourts.length;
    courtCountEl.textContent = `Showing ${count} of ${allCourts.length} courts`;
    
    // Update map markers
    updateMapMarkers(filteredCourts);
}

/**
 * Show court details in sidebar
 */
function showCourtDetails(court) {
    // Extract court availability info from hours if present
    const courtAvailability = extractCourtAvailability(court.hours_of_operation);
    
    const html = `
        <div class="detail-section">
            <h3>${court.name}</h3>
            <div class="detail-row">
                <span class="detail-label">📍 Address:</span>
                <span>${court.address}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">🏘️ Neighborhood:</span>
                <span>${court.neighborhood || 'N/A'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">🎾 Courts:</span>
                <span>${court.num_courts || 'N/A'}${courtAvailability ? ` - ${courtAvailability}` : ''}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">🥅 Nets:</span>
                <span class="badge ${court.nets_provided ? '' : 'no-nets'}">
                    ${court.nets_provided ? '✓ Provided' : '✗ Not Provided'}
                </span>
            </div>
            ${court.amenities && court.amenities.length > 0 ? `
                <div class="detail-row">
                    <span class="detail-label">✨ Amenities:</span>
                    <div class="amenities-list">
                        ${court.amenities.map(a => `<span class="badge">${a}</span>`).join('')}
                    </div>
                </div>
            ` : ''}
        </div>
        
        ${getReservationSection(court)}
    `;
    
    courtDetailsEl.innerHTML = html;
    sidebar.classList.add('active');
}

/**
 * Extract court availability info from hours string
 */
function extractCourtAvailability(hoursString) {
    if (!hoursString) return null;
    
    // Match patterns like "(4 courts - all reservable)" and extract just the availability part
    const match = hoursString.match(/\(\d+\s+courts\s*-\s*([^)]+)\)/);
    return match ? match[1] : null;
}

/**
 * Clean hours string by removing court availability info
 */
function cleanHoursString(hoursString) {
    if (!hoursString) return '';
    
    // Remove the court availability info in parentheses
    return hoursString.replace(/\s*\(\d+\s+courts\s*-\s*[^)]+\)/, '').trim();
}

/**
 * Generate reservation section HTML
 */
function getReservationSection(court) {
    const hasReservationInfo = court.hours_of_operation || court.pricing || court.reservation_url;
    
    if (!hasReservationInfo) {
        return '';
    }
    
    const hasReservationUrl = court.reservation_url && court.reservation_url.trim() !== '';
    const cleanedHours = cleanHoursString(court.hours_of_operation);
    
    return `
        <div class="reservation-section">
            <h3>🏓 Reservation Info</h3>
            <div class="reservation-info">
                ${cleanedHours ? `
                    <div class="reservation-row">
                        <strong>⏰ Hours</strong>
                        <span>${cleanedHours}</span>
                    </div>
                ` : ''}
                ${court.pricing ? `
                    <div class="reservation-row">
                        <strong>💰 Pricing</strong>
                        <span>${court.pricing}</span>
                    </div>
                ` : ''}
            </div>
            ${hasReservationUrl ? `
                <a href="${court.reservation_url}" 
                   target="_blank" 
                   rel="noopener noreferrer" 
                   class="reserve-btn">
                    Check Availability & Reserve →
                </a>
            ` : `
                <div style="margin-top: 0.5rem; color: #666; font-size: 0.9rem; text-align: center;">
                    Walk-in only - No online reservations
                </div>
            `}
        </div>
    `;
}

/**
 * Close the sidebar
 */
function closeSidebar() {
    sidebar.classList.remove('active');
}

/**
 * Show error message
 */
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    document.querySelector('.container').insertBefore(errorDiv, document.querySelector('.main-content'));
}

/**
 * Debounce helper function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
