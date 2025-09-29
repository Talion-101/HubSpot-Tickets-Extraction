// Priority Colors
const PRIORITY_COLORS = {
    "High": "#f5576c",
    "Medium": "#667eea",
    "Low": "#43e97b",
    "None": "#b8b8d1"
};

// Utility Functions
function parseTickets(rawData) {
    const lines = rawData.split("\n").filter(line => line.trim());
    const tickets = [];
    let currentTicket = {};
    
    for (let line of lines) {
        if (line.includes("Preview")) continue;
        
        if (line.includes("|") || line.includes("\t")) {
            // Legacy format
            const separator = line.includes("|") ? "|" : "\t";
            const [id, subject, priority, status, owner] = line.split(separator).map(s => s.trim());
            tickets.push({ id, subject, priority, status, owner });
        } else {
            // New format
            const match = line.match(/^(.*?):(.*?)$/);
            if (match) {
                const [, key, value] = match;
                currentTicket[key.trim()] = value.trim();
                
                // Check if this completes a ticket
                if (Object.keys(currentTicket).length === 5) {
                    tickets.push({...currentTicket});
                    currentTicket = {};
                }
            }
        }
    }
    
    return tickets;
}

function calculatePriorityStats(tickets) {
    const stats = {
        "High": 0,
        "Medium": 0,
        "Low": 0,
        "None": 0
    };
    
    tickets.forEach(ticket => {
        const priority = ticket.priority || "None";
        stats[priority]++;
    });
    
    return Object.entries(stats).map(([name, count]) => ({
        name,
        count,
        color: PRIORITY_COLORS[name]
    })).filter(stat => stat.count > 0);
}

function showAlert(message, type = "success") {
    const alertContainer = document.getElementById("alertContainer");
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${type === "error" ? "danger-premium" : "premium"} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === "error" ? "exclamation-triangle" : "info-circle"} me-2"></i>
        ${message}
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alertDiv);
    
    setTimeout(() => alertDiv.remove(), 5000);
}

function exportToExcel(tickets) {
    const ws = XLSX.utils.json_to_sheet(tickets);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Tickets");
    XLSX.writeFile(wb, "hubspot_tickets.xlsx");
}

function updatePriorityStats(stats) {
    const container = document.getElementById("priorityStats");
    container.innerHTML = `
        <div class="d-flex align-items-center mb-3">
            <i class="fas fa-chart-pie me-2" style="color: #00f5ff; font-size: 1.2rem;"></i>
            <h5 class="mb-0" style="color: white; font-weight: 600;">Priority Breakdown</h5>
        </div>
        <div class="priority-stats-grid">
            ${stats.map(stat => `
                <div class="priority-stat-card">
                    <div class="priority-badge" style="background: ${stat.color};">
                        ${stat.count}
                    </div>
                    <div class="priority-label" style="color: ${stat.color};">
                        ${stat.name}
                    </div>
                </div>
            `).join("")}
        </div>
    `;
}

function updateTable(tickets) {
    if (!tickets.length) return;
    
    const thead = document.querySelector("#resultsTable thead tr");
    const tbody = document.querySelector("#resultsTable tbody");
    const headers = Object.keys(tickets[0]);
    
    // Update headers
    thead.innerHTML = headers.map(header => 
        `<th scope="col">${header}</th>`
    ).join("");
    
    // Update body
    tbody.innerHTML = tickets.map(ticket => `
        <tr>
            ${headers.map(header => `<td>${ticket[header]}</td>`).join("")}
        </tr>
    `).join("");
}

// Event Listeners
document.getElementById("ticketForm").addEventListener("submit", function(e) {
    e.preventDefault();
    
    const rawData = document.getElementById("ticket_data").value;
    if (!rawData.trim()) {
        showAlert("Please paste some ticket data first!", "error");
        return;
    }
    
    try {
        const tickets = parseTickets(rawData);
        if (!tickets.length) {
            showAlert("No valid ticket data found. Please check the format.", "error");
            return;
        }
        
        // Update UI
        document.getElementById("ticketCount").textContent = tickets.length;
        document.getElementById("instructions").style.display = "none";
        document.getElementById("resultsSection").style.display = "block";
        document.getElementById("resetBtn").style.display = "inline-block";
        
        // Update stats and table
        const stats = calculatePriorityStats(tickets);
        updatePriorityStats(stats);
        updateTable(tickets);
        
        showAlert(`Successfully processed ${tickets.length} tickets!`);
        
        // Handle Excel export
        document.getElementById("exportBtn").onclick = () => exportToExcel(tickets);
        
    } catch (error) {
        console.error(error);
        showAlert("Error processing ticket data. Please check the format.", "error");
    }
});

document.getElementById("resetBtn").addEventListener("click", function() {
    document.getElementById("ticket_data").value = "";
    document.getElementById("resultsSection").style.display = "none";
    document.getElementById("instructions").style.display = "block";
    document.getElementById("resetBtn").style.display = "none";
    document.getElementById("alertContainer").innerHTML = "";
});

// Auto-resize textarea
const textarea = document.getElementById("ticket_data");
textarea.addEventListener("input", function() {
    this.style.height = "auto";
    this.style.height = Math.max(300, this.scrollHeight) + "px";
});