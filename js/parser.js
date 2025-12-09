/**
 * HubSpot Ticket Parser Module
 * Ported from utils/parser.py
 */

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

const Parser = {
    /**
     * Parse raw ticket data into structured format
     * @param {string} rawData - Raw text input
     * @returns {Object} result - { data: Array, errors: Array }
     */
    parseTicketData: function(rawData) {
        if (!rawData || !rawData.trim()) {
            return { data: [], errors: ['No data provided'] };
        }

        const lines = rawData.trim().split('\n');
        const errors = [];
        
        // Check if this is the new HubSpot format (line-by-line)
        if (this.isNewHubSpotFormat(lines)) {
            return this.parseNewHubSpotFormat(lines);
        }

        // Legacy format parsing (pipe or tab separated)
        const parsedData = [];
        
        lines.forEach((line, index) => {
            line = line.trim();
            if (!line) return;

            let values = [];

            if (line.includes('|')) {
                values = line.split('|').map(val => val.trim());
            } else if (line.includes('\t')) {
                values = line.split('\t').map(val => val.trim());
            } else {
                values = [line.trim()];
            }

            // Validate that we have exactly 9 values
            if (values.length !== 9) {
                const shortLine = line.length > 50 ? line.substring(0, 50) + '...' : line;
                errors.push(`Line ${index + 1}: Expected 9 values, got ${values.length} - "${shortLine}"`);
                return;
            }

            const ticketObj = {};
            HEADERS.forEach((header, i) => {
                ticketObj[header] = values[i] || '';
            });

            parsedData.push(ticketObj);
        });

        return { data: parsedData, errors: errors };
    },

    /**
     * Detect if the input is in the new HubSpot format
     * @param {Array} lines 
     * @returns {boolean}
     */
    isNewHubSpotFormat: function(lines) {
        const allLines = lines.map(l => l.trim());
        const nonEmptyLines = allLines.filter(l => l);

        const hasSeparators = nonEmptyLines.some(l => l.includes('|') || l.includes('\t'));
        
        if (hasSeparators) return false;

        const hasPreview = nonEmptyLines.some(l => l.toLowerCase() === 'preview');
        const hasBlankLines = allLines.length > nonEmptyLines.length;
        const reasonableLineCount = nonEmptyLines.length >= 9;

        if (hasPreview) return true;

        if (hasBlankLines && reasonableLineCount) {
            return (nonEmptyLines.length % 9 === 0 || 
                    nonEmptyLines.length % 10 === 0 ||
                    nonEmptyLines.length >= 9);
        }

        return !hasSeparators && reasonableLineCount;
    },

    /**
     * Parse the new HubSpot format (line-by-line)
     * @param {Array} lines 
     * @returns {Object} { data: Array, errors: Array }
     */
    parseNewHubSpotFormat: function(lines) {
        const parsedData = [];
        const errors = [];
        const processedLines = lines.map(l => l.trim());

        let i = 0;
        let ticketCount = 0;

        while (i < processedLines.length) {
            ticketCount++;
            const ticketLines = [];

            // Skip any initial empty lines
            while (i < processedLines.length && !processedLines[i]) {
                i++;
            }

            // Get ticket name
            if (i < processedLines.length && processedLines[i]) {
                ticketLines.push(processedLines[i]);
                i++;
            } else {
                break;
            }

            // Skip blank lines after ticket name
            while (i < processedLines.length && !processedLines[i]) {
                i++;
            }

            // Check for Preview
            if (i < processedLines.length && processedLines[i].toLowerCase() === 'preview') {
                i++; // Skip Preview
                while (i < processedLines.length && !processedLines[i]) {
                    i++;
                }
            }

            // Collect remaining 8 fields
            for (let j = 0; j < 8; j++) {
                while (i < processedLines.length && !processedLines[i]) {
                    i++;
                }

                if (i < processedLines.length && processedLines[i]) {
                    ticketLines.push(processedLines[i]);
                    i++;
                } else {
                    break;
                }
            }

            if (ticketLines.length !== 9) {
                errors.push(`Ticket ${ticketCount}: Expected 9 fields, got ${ticketLines.length}. Fields found: ${ticketLines.join(', ')}`);
                continue;
            }

            const ticketObj = {};
            HEADERS.forEach((header, idx) => {
                ticketObj[header] = ticketLines[idx] || '';
            });

            parsedData.push(ticketObj);
        }

        return { data: parsedData, errors: errors };
    }
};

window.Parser = Parser;
