from flask import Flask, render_template, request, session, send_file, jsonify, flash, redirect, url_for
import os
import logging
from utils.parser import parse_ticket_data
from utils.excel import create_excel_file

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_priority_stats(data):
    """Calculate ticket count statistics by priority"""
    priority_counts = {}
    
    for ticket in data:
        priority = ticket.get('PRIORITY', '').strip().lower()
        
        # Normalize priority names
        if priority in ['urgent', 'critical']:
            priority = 'urgent'
        elif priority in ['high']:
            priority = 'high'
        elif priority in ['medium', 'med', 'normal']:
            priority = 'medium'
        elif priority in ['low']:
            priority = 'low'
        else:
            priority = 'unknown'
        
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    # Define priority order and colors
    priority_order = ['urgent', 'high', 'medium', 'low', 'unknown']
    priority_colors = {
        'urgent': '#dc2626',    # Really red
        'high': '#ef4444',      # Red
        'medium': '#f59e0b',    # Yellowish orange
        'low': '#10b981',       # Green
        'unknown': '#6b7280'    # Gray
    }
    
    # Create ordered list with colors
    stats = []
    for priority in priority_order:
        if priority in priority_counts:
            stats.append({
                'name': priority.capitalize(),
                'count': priority_counts[priority],
                'color': priority_colors[priority]
            })
    
    return stats

@app.route('/')
def index():
    """Display the main form for pasting ticket data"""
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_tickets():
    """Parse the pasted ticket data and display results"""
    try:
        # Get the raw text data from the form
        raw_data = request.form.get('ticket_data', '').strip()
        
        if not raw_data:
            flash('Please paste some ticket data to process.', 'error')
            return redirect(url_for('index'))
        
        # Parse the data
        parsed_data, errors = parse_ticket_data(raw_data)
        
        if errors:
            flash(f'Parsing errors: {"; ".join(errors)}', 'error')
            return redirect(url_for('index'))
        
        if not parsed_data:
            flash('No valid ticket data found.', 'error')
            return redirect(url_for('index'))
        
        # Calculate priority statistics
        priority_stats = calculate_priority_stats(parsed_data)
        
        # Store parsed data in session for download
        session['parsed_data'] = parsed_data
        
        return render_template('index.html', data=parsed_data, priority_stats=priority_stats, show_download=True)
        
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download')
def download_excel():
    """Generate and download Excel file"""
    try:
        parsed_data = session.get('parsed_data')
        
        if not parsed_data:
            flash('No data available for download. Please parse some ticket data first.', 'error')
            return redirect(url_for('index'))
        
        # Create Excel file in memory
        excel_file = create_excel_file(parsed_data)
        
        return send_file(
            excel_file,
            as_attachment=True,
            download_name='hubspot_tickets.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        flash(f'Error generating Excel file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/clear')
def clear_data():
    """Clear session data"""
    session.pop('parsed_data', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
