# HubSpot Ticket Parser

A Flask web application that parses raw HubSpot ticket data into structured tables and exports them to Excel files. All processing happens in memory without storing any data on disk.

## Features

- 📋 **Parse Raw Data**: Paste unstructured ticket data (pipe or tab delimited)
- 🎨 **Dark UI**: Modern glassmorphism design with Bootstrap 5
- 📊 **HTML Table**: View parsed data in a responsive table
- 📥 **Excel Export**: Download results as .xlsx file with styling
- 🔒 **Memory Only**: No data persistence - everything processed in memory
- 🚀 **Deploy Ready**: Configured for Render deployment

## Input Format

The app expects raw ticket data with exactly 9 fields per line:

```
TICKET NAME | TICKET ID | TICKET - CONTACTS | TICKET STATUS | CREATE DATE | LAST ACTIVITY DATE | LAST CUSTOMER REPLY DATE | PRIORITY | TICKET OWNER
```

### Example Input:
```
Login Issue | TK-001 | john.doe@example.com | Open | 2025-08-01 | 2025-08-04 | 2025-08-03 | High | Alice
Payment Failure | TK-002 | jane.smith@example.com | In Progress | 2025-07-29 | 2025-08-02 | 2025-08-01 | Medium | Bob
```

### Supported Delimiters:
- Pipe (`|`) 
- Tab (`\t`)

## Project Structure

```
hubspot-ticket-parser/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Single-page UI with form and table
├── static/
│   └── styles.css        # Dark theme styling
├── utils/
│   ├── __init__.py
│   ├── parser.py         # Text parsing logic
│   └── excel.py          # Excel generation with openpyxl
├── requirements.txt      # Python dependencies
├── render.yaml          # Render deployment config
└── README.md
```

## Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd HubSpot-Tickets-Extraction
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open browser**
   Navigate to `http://localhost:5000`

### Deploy to Render

1. **Push to GitHub** (private repository recommended)
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Use these settings:
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

3. **Environment Variables**
   - `SECRET_KEY`: Auto-generated (for Flask sessions)
   - `FLASK_ENV`: `production`

## Usage

1. **Paste Data**: Copy your raw HubSpot ticket data into the textarea
2. **Generate Table**: Click "Generate Table" to parse and display
3. **Download Excel**: Click "Download Excel" to get a formatted .xlsx file
4. **Clear Data**: Use "Clear Data" to reset and start over

## Technical Details

### Dependencies
- **Flask 2.3.3**: Web framework
- **openpyxl 3.1.2**: Excel file creation
- **pandas 2.1.1**: Data manipulation (optional fallback)
- **gunicorn 21.2.0**: Production WSGI server

### Memory Management
- All data processing happens in `BytesIO` streams
- No files written to disk
- Session storage for temporary data (download feature)
- Automatic cleanup when session expires

### Error Handling
- Validates exactly 9 fields per row
- Shows specific error messages for invalid data
- Graceful handling of mixed delimiters
- Empty line filtering

### Excel Features
- Professional styling with headers
- Auto-adjusted column widths
- Cell borders and alignment
- Color-coded header row

## API Endpoints

- `GET /` - Main page with form
- `POST /parse` - Process ticket data
- `GET /download` - Generate Excel file
- `GET /clear` - Clear session data

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive design
- Bootstrap 5 components
- Font Awesome icons

## Security

- CSRF protection with Flask session
- No file uploads (paste-only interface)
- Environment-based secret key
- No data persistence

## Testing

Test with various data formats:

```bash
# Normal case
Login Issue | TK-001 | user@email.com | Open | 2025-08-01 | 2025-08-04 | 2025-08-03 | High | Alice

# Tab delimited
Login Issue	TK-002	user@email.com	Open	2025-08-01	2025-08-04	2025-08-03	High	Alice

# Error case (wrong field count)
Login Issue | TK-003 | user@email.com | Open | 2025-08-01 | High
```

## License

Private repository - All rights reserved

## Support

For issues or questions, please create an issue in the GitHub repository.
