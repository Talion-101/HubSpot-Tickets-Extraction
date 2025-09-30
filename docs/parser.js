// Parser module for HubSpot ticket data
const HEADERS = [
    'TICKET NAME',
    'TICKET ID',
    'TICKET - CONTACTS', 
    'TICKET STATUS',
    'CREATE DATE',
    'LAST ACTIVITY DATE',
    'LAST CUSTOMER REPLY DATE',
    'PRIORITY',
    'TICKET OWNER'
];

function isNewHubspotFormat(lines) {
    const allLines = lines.map(line => line.trim());
    const nonEmptyLines = allLines.filter(line => line);
    
    // Check for separators
    const hasSeparators = nonEmptyLines.some(line => line.includes('|') || line.includes('\t'));
    
    if (hasSeparators) {
        return false;
    }
    
    // Check for Preview
    const hasPreview = nonEmptyLines.some(line => line.toLowerCase() === 'preview');
    
    // Check for blank lines
    const hasBlankLines = allLines.length > nonEmptyLines.length;
    
    // Check for reasonable line count
    const reasonableLineCount = nonEmptyLines.length >= 9;
    
    if (hasPreview) {
        return true;
    }
    
    if (hasBlankLines && reasonableLineCount) {
        return (nonEmptyLines.length % 9 === 0 || 
                nonEmptyLines.length % 10 === 0 ||
                nonEmptyLines.length >= 9);
    }
    
    return !hasSeparators && reasonableLineCount;
}

function parseNewHubspotFormat(lines) {
    const parsedData = [];
    const errors = [];
    
    let i = 0;
    let ticketCount = 0;
    
    while (i < lines.length) {
        ticketCount++;
        const ticketLines = [];
        
        // Skip empty lines
        while (i < lines.length && !lines[i].trim()) {
            i++;
        }
        
        // Get ticket name
        if (i < lines.length && lines[i].trim()) {
            ticketLines.push(lines[i].trim());
            i++;
        } else {
            break;
        }
        
        // Skip blank lines after ticket name
        while (i < lines.length && !lines[i].trim()) {
            i++;
        }
        
        // Check for Preview
        if (i < lines.length && lines[i].trim().toLowerCase() === 'preview') {
            i++;
            
            while (i < lines.length && !lines[i].trim()) {
                i++;
            }
        }
        
        // Collect remaining fields
        const fieldsNeeded = 8;
        for (let fieldNum = 0; fieldNum < fieldsNeeded; fieldNum++) {
            while (i < lines.length && !lines[i].trim()) {
                i++;
            }
            
            if (i < lines.length && lines[i].trim()) {
                ticketLines.push(lines[i].trim());
                i++;
            } else {
                break;
            }
        }
        
        // Validate field count
        if (ticketLines.length !== 9) {
            errors.push(`Ticket ${ticketCount}: Expected 9 fields, got ${ticketLines.length}`);
            continue;
        }
        
        // Create ticket dictionary
        const ticketDict = {};
        HEADERS.forEach((header, index) => {
            ticketDict[header] = ticketLines[index].trim();
        });
        
        parsedData.push(ticketDict);
    }
    
    return { parsedData, errors };
}

function parseTicketData(rawData) {
    if (!rawData || !rawData.trim()) {
        return { parsedData: [], errors: ['No data provided'] };
    }
    
    const lines = rawData.trim().split('\n');
    const parsedData = [];
    const errors = [];
    
    // Check format
    if (isNewHubspotFormat(lines)) {
        return parseNewHubspotFormat(lines);
    }
    
    // Legacy format parsing
    lines.forEach((line, lineNum) => {
        line = line.trim();
        
        if (!line) {
            return;
        }
        
        let values;
        if (line.includes('|')) {
            values = line.split('|').map(val => val.trim());
        } else if (line.includes('\t')) {
            values = line.split('\t').map(val => val.trim());
        } else {
            values = [line.trim()];
        }
        
        if (values.length !== 9) {
            errors.push(`Line ${lineNum + 1}: Expected 9 values, got ${values.length} - "${line.slice(0, 50)}${line.length > 50 ? '...' : ''}"`);
            return;
        }
        
        const ticketDict = {};
        HEADERS.forEach((header, index) => {
            ticketDict[header] = values[index] || '';
        });
        
        parsedData.push(ticketDict);
    });
    
    return { parsedData, errors };
}

function calculatePriorityStats(data) {
    const priorityCounts = {};
    
    data.forEach(ticket => {
        let priority = (ticket['PRIORITY'] || '').trim().toLowerCase();
        
        // Normalize priority names
        if (['urgent', 'critical'].includes(priority)) {
            priority = 'urgent';
        } else if (['high'].includes(priority)) {
            priority = 'high';
        } else if (['medium', 'med', 'normal'].includes(priority)) {
            priority = 'medium';
        } else if (['low'].includes(priority)) {
            priority = 'low';
        } else {
            priority = 'unknown';
        }
        
        priorityCounts[priority] = (priorityCounts[priority] || 0) + 1;
    });
    
    const priorityOrder = ['urgent', 'high', 'medium', 'low', 'unknown'];
    const priorityColors = {
        'urgent': '#dc2626',    // Really red
        'high': '#ef4444',      // Red
        'medium': '#f59e0b',    // Yellowish orange
        'low': '#10b981',       // Green
        'unknown': '#6b7280'    // Gray
    };
    
    const stats = [];
    priorityOrder.forEach(priority => {
        if (priority in priorityCounts) {
            stats.push({
                name: priority.charAt(0).toUpperCase() + priority.slice(1),
                count: priorityCounts[priority],
                color: priorityColors[priority]
            });
        }
    });
    
    return stats;
}