/**
 * Excel Export Module
 * Uses SheetJS (xlsx) to generate Excel files
 */

const ExcelExporter = {
    /**
     * Download data as Excel file
     * @param {Array} data - List of ticket objects
     * @param {string} filename - Output filename
     */
    downloadExcel: function (data, filename = 'hubspot_tickets.xlsx') {
        if (!data || data.length === 0) {
            console.error('No data to export');
            return;
        }

        // Create worksheet
        // We rely on the object keys order which matches HEADERS in parser.js
        const ws = XLSX.utils.json_to_sheet(data);

        // Auto-width columns
        const colWidths = [];
        // Get all keys (headers)
        const keys = Object.keys(data[0]);

        keys.forEach(key => {
            let maxWidth = key.length;
            data.forEach(row => {
                const val = row[key] ? String(row[key]) : '';
                if (val.length > maxWidth) maxWidth = val.length;
            });
            // Cap width at 50 chars
            colWidths.push({ wch: Math.min(maxWidth + 2, 50) });
        });

        ws['!cols'] = colWidths;

        // Create workbook
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "HubSpot Tickets");

        // Write file
        XLSX.writeFile(wb, filename);
    }
};

window.ExcelExporter = ExcelExporter;
