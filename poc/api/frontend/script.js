// Note: API_BASE_URL is now defined in config.js
// Load config.js in your HTML before this script

// State management
let currentFiles = {
    'dl': null,
    'eb': null,
    'ld': []
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeUploadAreas();
});

// Tab Management
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// Initialize Upload Areas with Drag & Drop
function initializeUploadAreas() {
    const uploadConfigs = [
        { type: 'dl', inputId: 'file-input-dl', areaId: 'upload-area-dl', multiple: false },
        { type: 'eb', inputId: 'file-input-eb', areaId: 'upload-area-eb', multiple: false },
        { type: 'ld', inputId: 'file-input-ld', areaId: 'upload-area-ld', multiple: true }
    ];

    uploadConfigs.forEach(config => {
        const fileInput = document.getElementById(config.inputId);
        const uploadArea = document.getElementById(config.areaId);

        // File input change event
        fileInput.addEventListener('change', (e) => {
            handleFileSelect(e.target.files, config.type, config.multiple);
        });

        // Drag and drop events
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            handleFileSelect(e.dataTransfer.files, config.type, config.multiple);
        });

        // Click to upload
        uploadArea.addEventListener('click', (e) => {
            if (!e.target.classList.contains('browse-btn')) {
                fileInput.click();
            }
        });
    });
}

// Handle File Selection
function handleFileSelect(files, type, multiple) {
    if (!files || files.length === 0) return;

    // Validate file types
    const validImageTypes = CONFIG.ACCEPTED_IMAGE_TYPES;
    const validBillTypes = CONFIG.ACCEPTED_BILL_TYPES;

    for (let file of files) {
        const isValid = type === 'eb' 
            ? validBillTypes.includes(file.type)
            : validImageTypes.includes(file.type);

        if (!isValid) {
            showError(`Invalid file type: ${file.name}. Please upload an image file.`);
            return;
        }

        // Check file size
        if (file.size > CONFIG.MAX_FILE_SIZE) {
            const maxSizeMB = CONFIG.MAX_FILE_SIZE / (1024 * 1024);
            showError(`File too large: ${file.name}. Maximum size is ${maxSizeMB}MB.`);
            return;
        }
    }

    if (multiple) {
        currentFiles[type] = Array.from(files);
        displayMultiplePreview(type);
    } else {
        currentFiles[type] = files[0];
        displaySinglePreview(type);
    }

    // Hide upload area and show preview
    document.getElementById(`upload-area-${type}`).style.display = 'none';
    document.getElementById(`preview-${type}`).style.display = 'block';
    
    // Hide results section
    document.getElementById(`results-${type}`).style.display = 'none';
}

// Display Single File Preview
function displaySinglePreview(type) {
    const file = currentFiles[type];
    const reader = new FileReader();

    reader.onload = (e) => {
        const img = document.getElementById(`preview-img-${type}`);
        img.src = e.target.result;
    };

    reader.readAsDataURL(file);
}

// Display Multiple Files Preview
function displayMultiplePreview(type) {
    const files = currentFiles[type];
    const previewGrid = document.getElementById(`preview-grid-${type}`);
    previewGrid.innerHTML = '';

    files.forEach((file, index) => {
        const reader = new FileReader();

        reader.onload = (e) => {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';

            const img = document.createElement('img');
            img.src = e.target.result;
            img.alt = `Page ${index + 1}`;

            const pageNumber = document.createElement('div');
            pageNumber.className = 'preview-item-number';
            pageNumber.textContent = `Page ${index + 1}`;

            previewItem.appendChild(img);
            previewItem.appendChild(pageNumber);
            previewGrid.appendChild(previewItem);
        };

        reader.readAsDataURL(file);
    });
}

// Remove File
function removeFile(type) {
    currentFiles[type] = type === 'ld' ? [] : null;
    document.getElementById(`upload-area-${type}`).style.display = 'block';
    document.getElementById(`preview-${type}`).style.display = 'none';
    document.getElementById(`results-${type}`).style.display = 'none';

    // Reset file input
    const fileInput = document.getElementById(`file-input-${type}`);
    fileInput.value = '';
}

// Submit Document for Processing
async function submitDocument(type) {
    const file = currentFiles[type];
    
    if (!file || (Array.isArray(file) && file.length === 0)) {
        showError('Please select a file first.');
        return;
    }

    showLoading(true);

    try {
        let result;
        
        switch(type) {
            case 'dl':
                result = await processDriversLicense(file);
                displayDriversLicenseResults(result);
                break;
            case 'eb':
                result = await processEnergyBill(file);
                displayEnergyBillResults(result);
                break;
            case 'ld':
                result = await processLargeDocument(file);
                displayLargeDocumentResults(result);
                break;
        }

        document.getElementById(`results-${type}`).style.display = 'block';
    } catch (error) {
        showError(error.message || 'An error occurred while processing the document.');
    } finally {
        showLoading(false);
    }
}

// API Calls
async function processDriversLicense(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${CONFIG.API_BASE_URL}/ocr/drivers-license`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to process driver\'s license');
    }

    return await response.json();
}

async function processEnergyBill(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${CONFIG.API_BASE_URL}/ocr/energy-bill`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to process energy bill');
    }

    return await response.json();
}

async function processLargeDocument(files) {
    const formData = new FormData();
    
    files.forEach((file) => {
        formData.append('files', file);
    });

    const response = await fetch(`${CONFIG.API_BASE_URL}/ocr/large-document`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to process large document');
    }

    return await response.json();
}

// Display Results
function displayDriversLicenseResults(data) {
    const container = document.getElementById('results-content-dl');
    
    const fields = [
        { label: 'Name', value: data.name || 'N/A' },
        { label: 'CPF', value: data.cpf ? formatCPF(data.cpf) : 'N/A' },
        { label: 'Birth Date', value: data.birth_date ? formatDate(data.birth_date) : 'N/A' },
        { label: 'Emission Date', value: data.emission_date ? formatDate(data.emission_date) : 'N/A' },
        { label: 'Father Name', value: data.father_name || 'N/A' },
        { label: 'Mother Name', value: data.mother_name || 'N/A' }
    ];

    let html = fields.map(field => `
        <div class="result-item">
            <div class="result-label">${field.label}</div>
            <div class="result-value">${field.value}</div>
        </div>
    `).join('');

    // Add raw OCR section if available
    if (data.raw_ocr) {
        html += `
            <div class="result-item" style="margin-top: 20px;">
                <div class="result-label">Raw OCR Text</div>
                <div class="result-value" style="white-space: pre-wrap; font-family: monospace; font-size: 12px;">
                    ${data.raw_ocr['<OCR>'] || JSON.stringify(data.raw_ocr, null, 2)}
                </div>
            </div>
        `;
    }

    // Add status indicator
    if (data.structured !== undefined) {
        html += `
            <div class="result-item" style="margin-top: 10px;">
                <div class="result-label">Processing Status</div>
                <div class="result-value">
                    ${data.structured ? '✅ Structured by LLM' : '⚠️ Mock data (JSON parser not yet implemented)'}
                </div>
            </div>
        `;
    }

    container.innerHTML = html;
}

function displayEnergyBillResults(data) {
    const container = document.getElementById('results-content-eb');
    
    const fields = [
        { label: 'Customer Name', value: data.customer_name },
        { label: 'Customer ID', value: data.customer_id },
        { label: 'Address', value: data.address },
        { label: 'Reference Month', value: data.reference_month },
        { label: 'Due Date', value: formatDate(data.due_date) },
        { label: 'Total Amount', value: formatCurrency(data.total_amount) },
        { label: 'Consumption (kWh)', value: `${data.consumption_kwh} kWh` },
        { label: 'Installation Number', value: data.installation_number }
    ];

    container.innerHTML = fields.map(field => `
        <div class="result-item">
            <div class="result-label">${field.label}</div>
            <div class="result-value">${field.value}</div>
        </div>
    `).join('');
}

function displayLargeDocumentResults(data) {
    const container = document.getElementById('results-content-ld');
    
    let html = `
        <div class="result-item mb-2">
            <div class="result-label">Total Pages</div>
            <div class="result-value">${data.total_pages}</div>
        </div>
    `;

    // Display content for each page
    data.content.forEach((page, index) => {
        html += `
            <div class="page-content">
                <div class="page-header">📄 Page ${index + 1}</div>
                <div class="page-text">${formatPageContent(page)}</div>
            </div>
        `;
    });

    // Display summary if available
    if (data.summary) {
        html += `
            <div class="summary-section">
                <h4>📋 Document Summary</h4>
                <p>${data.summary}</p>
            </div>
        `;
    }

    container.innerHTML = html;
}

// Utility Functions
function formatCPF(cpf) {
    if (!cpf) return cpf;
    // Format: 000.000.000-00
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

function formatDate(date) {
    if (!date) return date;
    // Try to parse and format the date
    try {
        const d = new Date(date);
        if (!isNaN(d.getTime())) {
            return d.toLocaleDateString('pt-BR');
        }
    } catch (e) {
        // If parsing fails, return as is
    }
    return date;
}

function formatCurrency(amount) {
    if (amount === null || amount === undefined) return amount;
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(amount);
}

function formatPageContent(page) {
    // Handle different possible structures
    if (typeof page === 'string') {
        return page;
    } else if (page.text) {
        return page.text;
    } else if (page.content) {
        return page.content;
    } else {
        return JSON.stringify(page, null, 2);
    }
}

// UI Helpers
function showLoading(show) {
    document.getElementById('loading-overlay').style.display = show ? 'flex' : 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    
    errorText.textContent = message;
    errorDiv.style.display = 'flex';

    // Auto-hide after configured delay
    setTimeout(() => {
        closeError();
    }, CONFIG.AUTO_HIDE_ERROR_DELAY);
}

function closeError() {
    document.getElementById('error-message').style.display = 'none';
}
