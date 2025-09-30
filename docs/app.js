document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const form = document.getElementById('ticketForm');
    const textarea = document.getElementById('ticket_data');
    const resetButton = document.getElementById('resetButton');
    const resultsSection = document.getElementById('resultsSection');
    const instructionsSection = document.getElementById('instructionsSection');
    const ticketCount = document.getElementById('ticketCount');
    const downloadExcel = document.getElementById('downloadExcel');
    
    // Current Data State
    let currentData = null;
    
    // Form Submission Handler
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const rawData = textarea.value.trim();
        if (!rawData) {
            showAlert('Please paste some ticket data to process.', 'error');
            return;
        }
        
        // Parse data
        const { parsedData, errors } = parseTicketData(rawData);
        
        if (errors && errors.length > 0) {
            showAlert('Parsing errors: ' + errors.join('; '), 'error');
            return;
        }
        
        if (!parsedData || parsedData.length === 0) {
            showAlert('No valid ticket data found.', 'error');
            return;
        }
        
        // Store current data
        currentData = parsedData;
        
        // Update UI
        displayResults(parsedData);
        
        // Show reset button
        resetButton.classList.remove('d-none');
        
        // Hide instructions
        instructionsSection.classList.add('d-none');
        
        // Show results
        resultsSection.classList.remove('d-none');
    });
    
    // Reset Button Handler
    resetButton.addEventListener('click', function() {
        // Clear textarea
        textarea.value = '';
        
        // Hide results
        resultsSection.classList.add('d-none');
        
        // Show instructions
        instructionsSection.classList.remove('d-none');
        
        // Hide reset button
        resetButton.classList.add('d-none');
        
        // Clear current data
        currentData = null;
    });
    
    // Download Excel Handler
    downloadExcel.addEventListener('click', function() {
        if (!currentData || currentData.length === 0) {
            showAlert('No data available for download. Please parse some ticket data first.', 'error');
            return;
        }
        
        createAndDownloadExcel(currentData);
    });
    
    // Display Results Function
    function displayResults(data) {
        // Update ticket count
        ticketCount.textContent = `${data.length} tickets successfully parsed`;
        
        // Calculate and display priority stats
        const priorityStats = calculatePriorityStats(data);
        displayPriorityStats(priorityStats);
        
        // Display table
        displayTable(data);
    }
    
    // Display Priority Stats Function
    function displayPriorityStats(stats) {
        const container = document.getElementById('priorityStatsGrid');
        container.innerHTML = '';
        
        stats.forEach(stat => {
            const statCard = document.createElement('div');
            statCard.className = 'priority-stat-card';
            statCard.innerHTML = `
                <div class="priority-badge" style="background: ${stat.color};">
                    ${stat.count}
                </div>
                <div class="priority-label" style="color: ${stat.color};">
                    ${stat.name}
                </div>
            `;
            container.appendChild(statCard);
        });
    }
    
    // Display Table Function
    function displayTable(data) {
        const table = document.getElementById('resultsTable');
        const thead = table.querySelector('thead tr');
        const tbody = table.querySelector('tbody');
        
        // Clear existing content
        thead.innerHTML = '';
        tbody.innerHTML = '';
        
        // Add headers
        HEADERS.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            thead.appendChild(th);
        });
        
        // Add data rows
        data.forEach(ticket => {
            const tr = document.createElement('tr');
            HEADERS.forEach(header => {
                const td = document.createElement('td');
                td.textContent = ticket[header] || '';
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }
    
    // Create and Download Excel Function
    function createAndDownloadExcel(data) {
        // Create a new workbook
        const wb = XLSX.utils.book_new();
        
        // Convert data to worksheet
        const ws = XLSX.utils.json_to_sheet(data);
        
        // Add worksheet to workbook
        XLSX.utils.book_append_sheet(wb, ws, "HubSpot Tickets");
        
        // Save workbook
        XLSX.writeFile(wb, 'hubspot_tickets.xlsx');
    }
    
    // Show Alert Function
    function showAlert(message, type) {
        const alertContainer = document.getElementById('alertContainer');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type === 'error' ? 'danger-premium' : 'premium'} alert-dismissible fade show fade-in-up`;
        alert.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert"></button>
        `;
        alertContainer.appendChild(alert);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }
    
    // Textarea Auto-resize
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.max(300, this.scrollHeight) + 'px';
    });
    
    // Textarea Focus Effects
    textarea.addEventListener('focus', function() {
        this.style.transform = 'scale(1.01)';
    });
    
    textarea.addEventListener('blur', function() {
        this.style.transform = 'scale(1)';
    });
    
    // Form Loading State
    form.addEventListener('submit', function() {
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalHTML = submitBtn.innerHTML;
        
        submitBtn.innerHTML = '<span class="loading-spinner me-2"></span>Processing Magic...';
        submitBtn.disabled = true;
        
        submitBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        submitBtn.style.transform = 'scale(0.98)';
        
        // Reset button state after processing
        setTimeout(() => {
            submitBtn.innerHTML = originalHTML;
            submitBtn.disabled = false;
            submitBtn.style.transform = '';
        }, 1000);
    });
    
    // Smooth Scroll to Results
    function scrollToResults() {
        const resultsCard = document.querySelector('.fade-in-up:last-of-type');
        if (resultsCard) {
            setTimeout(() => {
                resultsCard.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start',
                    inline: 'nearest'
                });
            }, 300);
        }
    }
    
    // Table Row Hover Effects
    document.addEventListener('click', function() {
        const tableRows = document.querySelectorAll('#resultsTable tbody tr');
        tableRows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.01)';
                this.style.zIndex = '10';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.zIndex = 'auto';
            });
        });
    });
    
    // Typing Effect for Placeholder
    function initTypingEffect() {
        if (textarea && !currentData) {
            const placeholderText = textarea.placeholder;
            textarea.placeholder = '';
            let i = 0;
            
            const typeWriter = () => {
                if (i < placeholderText.length) {
                    textarea.placeholder += placeholderText.charAt(i);
                    i++;
                    setTimeout(typeWriter, 20);
                }
            };
            
            setTimeout(typeWriter, 1000);
        }
    }
    
    // Initialize typing effect
    initTypingEffect();
});