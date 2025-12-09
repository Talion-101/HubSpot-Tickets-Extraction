/**
 * Main Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const ticketDataInput = document.getElementById('ticketData');
    const parseBtn = document.getElementById('parseBtn');
    const resetBtn = document.getElementById('resetBtn');
    const exportBtn = document.getElementById('exportBtn');
    const resultsSection = document.getElementById('resultsSection');
    const instructionsSection = document.getElementById('instructionsSection');
    const resultsTableBody = document.querySelector('#resultsTable tbody');
    const resultCount = document.getElementById('resultCount');
    const statsGrid = document.getElementById('statsGrid');
    const alertContainer = document.getElementById('alertContainer');
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;

    // Theme Logic
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
    }

    themeToggle.addEventListener('click', () => {
        html.classList.toggle('dark');
        localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
    });

    // State
    let parsedTickets = [];

    // Event Listeners
    parseBtn.addEventListener('click', handleParse);
    resetBtn.addEventListener('click', handleReset);
    exportBtn.addEventListener('click', handleExport);

    // Auto-resize textarea
    ticketDataInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (this.value.trim() === '') {
            this.style.height = 'auto'; // Reset
        }
    });

    /**
     * Handle formatting and displaying results
     */
    function handleParse() {
        // Clear previous alerts
        alertContainer.innerHTML = '';

        const rawData = ticketDataInput.value;
        if (!rawData.trim()) {
            showAlert('Please paste some ticket data to process.', 'error');
            return;
        }

        // Show loading state
        const originalBtnText = parseBtn.innerHTML;
        parseBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        parseBtn.disabled = true;

        // Small delay to allow UI to update (spinner)
        setTimeout(() => {
            try {
                const result = window.Parser.parseTicketData(rawData);

                if (result.errors.length > 0) {
                    showAlert(`Parsing errors: ${result.errors.join('; ')}`, 'error');
                }

                if (result.data.length === 0) {
                    if (result.errors.length === 0) {
                        showAlert('No valid ticket data found.', 'error');
                    }
                } else {
                    // Success
                    parsedTickets = result.data;
                    displayResults(parsedTickets);
                    calculateAndShowStats(parsedTickets);

                    // Toggle UI
                    instructionsSection.classList.add('hidden');
                    resultsSection.classList.remove('hidden');
                    resetBtn.classList.remove('hidden');
                    resetBtn.classList.add('inline-flex');

                    // Scroll to results
                    // resultsSection.scrollIntoView({ behavior: 'smooth' }); // Disable Smooth Scroll for "No Animation" rule
                    resultsSection.scrollIntoView();

                    showAlert(`Successfully processed ${parsedTickets.length} tickets!`, 'info');
                }

            } catch (e) {
                console.error(e);
                showAlert(`An unexpected error occurred: ${e.message}`, 'error');
            } finally {
                // Reset button state
                parseBtn.innerHTML = originalBtnText;
                parseBtn.disabled = false;
            }
        }, 100); // Faster timeout for "No Animation" feel
    }

    function handleReset() {
        ticketDataInput.value = '';
        ticketDataInput.style.height = 'auto';
        parsedTickets = [];

        resultsSection.classList.add('hidden');
        instructionsSection.classList.remove('hidden');
        resetBtn.classList.add('hidden');
        resetBtn.classList.remove('inline-flex');
        alertContainer.innerHTML = '';
    }

    function handleExport() {
        if (parsedTickets.length === 0) return;
        window.ExcelExporter.downloadExcel(parsedTickets, 'hubspot_tickets.xlsx');
    }

    function displayResults(data) {
        resultCount.textContent = `${data.length} tickets parsed`;
        resultsTableBody.innerHTML = '';

        data.forEach((ticket, index) => {
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-gray-50/50 dark:hover:bg-white/5 border-b border-gray-100 dark:border-white/5 transition-none';

            // Ensure order matches headers
            const headers = [
                'TICKET NAME', 'TICKET ID', 'TICKET STATUS',
                'CREATE DATE', 'PRIORITY', 'TICKET OWNER'
            ];

            headers.forEach(header => {
                const td = document.createElement('td');
                td.className = 'p-3 whitespace-nowrap text-gray-700 dark:text-gray-300';

                let value = ticket[header] || '';

                // Add specific styling for status or priority if needed
                if (header === 'PRIORITY') {
                    const p = value.toLowerCase();
                    let colorClass = 'text-gray-500';
                    if (['urgent', 'critical'].includes(p)) colorClass = 'text-red-500 font-medium';
                    else if (['high'].includes(p)) colorClass = 'text-red-500';
                    else if (['medium', 'med', 'normal'].includes(p)) colorClass = 'text-yellow-500';
                    else if (['low'].includes(p)) colorClass = 'text-green-500';

                    td.innerHTML = `<span class="${colorClass}">${value}</span>`;
                } else {
                    td.textContent = value;
                }

                tr.appendChild(td);
            });
            resultsTableBody.appendChild(tr);
        });
    }

    function calculateAndShowStats(data) {
        const counts = {};

        data.forEach(ticket => {
            let priority = (ticket['PRIORITY'] || '').trim().toLowerCase();

            // Normalize
            if (['urgent', 'critical'].includes(priority)) priority = 'urgent';
            else if (['high'].includes(priority)) priority = 'high';
            else if (['medium', 'med', 'normal'].includes(priority)) priority = 'medium';
            else if (['low'].includes(priority)) priority = 'low';
            else priority = 'unknown';

            counts[priority] = (counts[priority] || 0) + 1;
        });

        const priorityConfig = {
            'urgent': { color: 'text-red-600 dark:text-red-400', label: 'Urgent' },
            'high': { color: 'text-red-500 dark:text-red-400', label: 'High' },
            'medium': { color: 'text-yellow-500 dark:text-yellow-400', label: 'Medium' },
            'low': { color: 'text-green-500 dark:text-green-400', label: 'Low' },
            'unknown': { color: 'text-gray-400 dark:text-gray-500', label: 'Unknown' }
        };

        const order = ['urgent', 'high', 'medium', 'low', 'unknown'];

        statsGrid.innerHTML = '';

        order.forEach(p => {
            if (counts[p]) {
                const config = priorityConfig[p];
                const div = document.createElement('div');
                div.className = 'bg-gray-50 dark:bg-white/5 rounded-xl p-3 border border-gray-100 dark:border-white/5 text-center';
                div.innerHTML = `
                    <div class="text-2xl font-bold ${config.color}">${counts[p]}</div>
                    <div class="text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400 mt-1">${config.label}</div>
                `;
                statsGrid.appendChild(div);
            }
        });
    }

    function showAlert(message, type = 'info') {
        const div = document.createElement('div');

        let colors = '';
        let icon = '';

        if (type === 'error') {
            colors = 'bg-red-50 dark:bg-red-500/10 text-red-600 dark:text-red-400 border border-red-100 dark:border-red-500/20';
            icon = 'fa-exclamation-circle';
        } else {
            colors = 'bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-500/20';
            icon = 'fa-info-circle';
        }

        div.className = `p-4 rounded-xl flex items-center gap-3 ${colors}`;
        div.innerHTML = `
            <i class="fas ${icon}"></i>
            <span class="text-sm font-medium">${message}</span>
        `;
        alertContainer.appendChild(div);
    }
});
