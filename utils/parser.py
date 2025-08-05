"""
Parser module for HubSpot ticket data
Handles parsing of raw text input into structured data
"""

import re

# Fixed headers for HubSpot tickets
HEADERS = [
    'TICKET NAME',
    'TICKET - CONTACTS', 
    'TICKET STATUS',
    'CREATE DATE',
    'LAST ACTIVITY DATE',
    'LAST CUSTOMER REPLY DATE',
    'PRIORITY',
    'TICKET OWNER'
]

def parse_ticket_data(raw_data):
    """
    Parse raw ticket data into structured format
    
    Args:
        raw_data (str): Raw text input with ticket data
        
    Returns:
        tuple: (parsed_data, errors)
            parsed_data (list): List of dictionaries with ticket data
            errors (list): List of error messages
    """
    if not raw_data or not raw_data.strip():
        return [], ['No data provided']
    
    lines = raw_data.strip().split('\n')
    parsed_data = []
    errors = []
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Try to split by pipe first, then by tab
        if '|' in line:
            values = [val.strip() for val in line.split('|')]
        elif '\t' in line:
            values = [val.strip() for val in line.split('\t')]
        else:
            # If no delimiters found, treat as single value (error case)
            values = [line.strip()]
        
        # Validate that we have exactly 8 values
        if len(values) != 8:
            errors.append(f'Line {line_num}: Expected 8 values, got {len(values)} - "{line[:50]}{"..." if len(line) > 50 else ""}"')
            continue
        
        # Create dictionary mapping headers to values
        ticket_dict = {}
        for header, value in zip(HEADERS, values):
            ticket_dict[header] = value.strip() if value else ''
        
        parsed_data.append(ticket_dict)
    
    return parsed_data, errors

def validate_ticket_data(data):
    """
    Additional validation for parsed ticket data
    
    Args:
        data (list): List of ticket dictionaries
        
    Returns:
        list: List of validation errors
    """
    errors = []
    
    if not data:
        errors.append('No valid ticket data found')
        return errors
    
    # Check for required fields
    required_fields = ['TICKET NAME', 'TICKET STATUS']
    
    for i, ticket in enumerate(data, 1):
        for field in required_fields:
            if not ticket.get(field, '').strip():
                errors.append(f'Row {i}: Missing required field "{field}"')
    
    return errors
