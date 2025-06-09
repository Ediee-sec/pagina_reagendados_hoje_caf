// DOM Elements
const filterColumn = document.getElementById('filterColumn');
const filterValue = document.getElementById('filterValue');
const sortBy = document.getElementById('sortBy');
const sortOrder = document.getElementById('sortOrder');
const downloadBtn = document.getElementById('downloadBtn');
const downloadMenu = document.getElementById('downloadMenu');
const loadingOverlay = document.getElementById('loadingOverlay');
const dataTable = document.getElementById('dataTable');

// Utility Functions
function showLoading() {
    loadingOverlay.classList.add('show');
}

function hideLoading() {
    loadingOverlay.classList.remove('show');
}

function getQueryParams() {
    const params = new URLSearchParams();
    
    if (filterColumn.value && filterValue.value.trim()) {
        params.append('filter_column', filterColumn.value);
        params.append('filter_value', filterValue.value.trim());
    }
    
    if (sortBy.value) {
        params.append('sort_by', sortBy.value);
    }
    
    if (sortOrder.value) {
        params.append('sort_order', sortOrder.value);
    }
    
    return params;
}

function updatePage() {
    showLoading();
    const params = getQueryParams();
    const url = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
    window.location.href = url;
}

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

// Filter Functionality
filterColumn.addEventListener('change', () => {
    if (!filterColumn.value) {
        filterValue.value = '';
    }
    updatePage();
});

const debouncedFilter = debounce(() => {
    if (filterColumn.value) {
        updatePage();
    }
}, 500);

filterValue.addEventListener('input', debouncedFilter);

filterValue.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && filterColumn.value) {
        updatePage();
    }
});

// Sort Functionality
sortBy.addEventListener('change', updatePage);
sortOrder.addEventListener('change', updatePage);

// Table Header Click Sorting
dataTable.addEventListener('click', (e) => {
    const th = e.target.closest('th[data-sort]');
    if (th) {
        const sortField = th.getAttribute('data-sort');
        const currentSort = sortBy.value;
        const currentOrder = sortOrder.value;
        
        if (currentSort === sortField) {
            // Toggle order if same field
            sortOrder.value = currentOrder === 'asc' ? 'desc' : 'asc';
        } else {
            // Set new field and default to ascending
            sortBy.value = sortField;
            sortOrder.value = 'asc';
        }
        
        updatePage();
    }
});

// Download Functionality
downloadBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    downloadMenu.classList.toggle('show');
});

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!downloadBtn.contains(e.target)) {
        downloadMenu.classList.remove('show');
    }
});

// Handle download format selection
downloadMenu.addEventListener('click', (e) => {
    e.preventDefault();
    const link = e.target.closest('a[data-format]');
    if (link) {
        const format = link.getAttribute('data-format');
        downloadData(format);
        downloadMenu.classList.remove('show');
    }
});

function downloadData(format) {
    showLoading();
    
    const params = getQueryParams();
    const downloadUrl = `/download/${format}?${params.toString()}`;
    
    if (format === 'json') {
        // For JSON, open in new tab
        window.open(downloadUrl, '_blank');
        hideLoading();
    } else {
        // For other formats, trigger download
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `data.${format}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Hide loading after a short delay
        setTimeout(hideLoading, 1000);
    }
}

// Update sort icons based on current sort
function updateSortIcons() {
    const currentSort = sortBy.value;
    const currentOrder = sortOrder.value;
    
    // Reset all icons
    document.querySelectorAll('.sort-icon').forEach(icon => {
        icon.className = 'fas fa-sort sort-icon';
    });
    
    // Update current sort icon
    const currentHeader = document.querySelector(`th[data-sort="${currentSort}"] .sort-icon`);
    if (currentHeader) {
        currentHeader.className = `fas fa-sort-${currentOrder === 'asc' ? 'up' : 'down'} sort-icon`;
    }
}

// Initialize sort icons on page load
document.addEventListener('DOMContentLoaded', () => {
    updateSortIcons();
    
    // Add hover effects to table rows
    const tableRows = document.querySelectorAll('.table-row');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.transform = 'translateX(5px)';
        });
        
        row.addEventListener('mouseleave', () => {
            row.style.transform = 'translateX(0)';
        });
    });
    
    // Add click to copy functionality for phone numbers
    const phoneLinks = document.querySelectorAll('.phone-link');
    phoneLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const phoneNumber = link.textContent.trim();
            
            if (navigator.clipboard) {
                navigator.clipboard.writeText(phoneNumber).then(() => {
                    showToast('Número copiado para a área de transferência!');
                });
            } else {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = phoneNumber;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showToast('Número copiado para a área de transferência!');
            }
        });
    });
});

// Toast notification function
function showToast(message) {
    // Remove existing toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create new toast
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4299e1;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease, fadeOut 0.3s ease 2.7s;
    `;
    
    document.body.appendChild(toast);
    
    // Remove toast after animation
    setTimeout(() => {
        toast.remove();
    }, 3000);
}


