/**
 * Main application logic for SF Pickleball Courts Finder
 */

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

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
 * Load all courts from the API
 */
async function loadCourts() {
    try {
        const response = await fetch(`${API_BASE_URL}/courts`);
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
 * Load neighborhoods from the API
 */
async function loadNeighborhoods() {
    try {
        const response = await fetch(`${API_BASE_URL}/neighborhoods`);
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
                <span class="detail-label">🎾 Number of Courts:</span>
                <span>${court.num_courts || 'N/A'}</span>
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
    `;
    
    courtDetailsEl.innerHTML = html;
    sidebar.classList.add('active');
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
