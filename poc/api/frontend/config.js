// API Configuration
// Change this to match your backend URL
const CONFIG = {
    // For local development
    API_BASE_URL: 'http://localhost:8000/api/v1',
    
    // For production, uncomment and update the line below:
    // API_BASE_URL: 'https://your-production-api.com/api/v1',

    // Maximum file size (in bytes) - 100 MB
    MAX_FILE_SIZE: 100 * 1024 * 1024,

    // Accepted file types
    ACCEPTED_IMAGE_TYPES: ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'],
    ACCEPTED_BILL_TYPES: ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'application/pdf'],

    // UI Settings
    AUTO_HIDE_ERROR_DELAY: 10000 // milliseconds
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
