"""
Parser module for HubSpot ticket data
Handles parsing of raw text input into structured data
"""

import re

# Fixed headers for HubSpot tickets
HEADERS = [
    'TICKET NAME',
    'TICKET ID',
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
    Supports both legacy formats (pipe/tab separated) and new HubSpot format (line-by-line)
    
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
    
    # Check if this is the new HubSpot format (line-by-line)
    if _is_new_hubspot_format(lines):
        return _parse_new_hubspot_format(lines, errors)
    
    # Legacy format parsing (pipe or tab separated)
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
        
        # Validate that we have exactly 9 values
        if len(values) != 9:
            errors.append(f'Line {line_num}: Expected 9 values, got {len(values)} - "{line[:50]}{"..." if len(line) > 50 else ""}"')
            continue
        
        # Create dictionary mapping headers to values
        ticket_dict = {}
        for header, value in zip(HEADERS, values):
            ticket_dict[header] = value.strip() if value else ''
        
        parsed_data.append(ticket_dict)
    
    return parsed_data, errors

def _is_new_hubspot_format(lines):
    """
    Detect if the input is in the new HubSpot format (line-by-line)
    Considers blank lines and "Preview" indicators
    
    Args:
        lines (list): List of lines from the input
        
    Returns:
        bool: True if it appears to be new HubSpot format
    """
    # Get all lines (including empty ones) and non-empty lines for analysis
    all_lines = [line.strip() for line in lines]
    non_empty_lines = [line for line in all_lines if line]
    
    # New format typically has no pipe or tab separators
    has_separators = any('|' in line or '\t' in line for line in non_empty_lines)
    
    # If has separators, it's likely legacy format
    if has_separators:
        return False
    
    # Strong indicators of new HubSpot format:
    # 1. Contains "Preview" (case insensitive)
    has_preview = any(line.lower() == 'preview' for line in non_empty_lines)
    
    # 2. Has blank lines (indicates structured formatting)
    has_blank_lines = len(all_lines) > len(non_empty_lines)
    
    # 3. Reasonable number of non-empty lines for ticket data
    reasonable_line_count = len(non_empty_lines) >= 9
    
    # If we have preview or (blank lines + reasonable count), likely new format
    if has_preview:
        return True
    
    if has_blank_lines and reasonable_line_count:
        # Additional check: see if the count makes sense for ticket structure
        # With preview: 10 lines per ticket, without preview: 9 lines per ticket
        return (len(non_empty_lines) % 9 == 0 or 
                len(non_empty_lines) % 10 == 0 or
                len(non_empty_lines) >= 9)
    
    # Fallback: if no separators and sufficient lines, assume new format
    return not has_separators and reasonable_line_count

def _parse_new_hubspot_format(lines, errors):
    """
    Parse the new HubSpot format where each field is on a separate line
    Handles blank lines and "Preview" lines that should be ignored
    
    Args:
        lines (list): List of lines from the input
        errors (list): List to append errors to
        
    Returns:
        list: List of parsed ticket dictionaries
    """
    parsed_data = []
    
    # Keep original lines but strip whitespace for processing
    processed_lines = [line.strip() for line in lines]
    
    # Process tickets in chunks
    i = 0
    ticket_count = 0
    
    while i < len(processed_lines):
        ticket_count += 1
        ticket_lines = []
        
        # Collect lines for one ticket
        # Expected format:
        # 1. Ticket Name
        # 2. [Blank line] (optional - skip if present)
        # 3. Preview (optional - skip if present)
        # 4. Ticket ID
        # 5. Ticket Contacts
        # 6. Ticket Status
        # 7. Create Date
        # 8. Last Activity Date
        # 9. Last Customer Reply Date
        # 10. Priority
        # 11. Ticket Owner
        
        # Skip any initial empty lines
        while i < len(processed_lines) and not processed_lines[i]:
            i += 1
        
        # Get ticket name (first non-empty line)
        if i < len(processed_lines) and processed_lines[i]:
            ticket_lines.append(processed_lines[i])
            i += 1
        else:
            # No more content
            break
        
        # Skip any blank lines after ticket name
        while i < len(processed_lines) and not processed_lines[i]:
            i += 1
        
        # Check if next line is "Preview" and skip it
        if i < len(processed_lines) and processed_lines[i].lower() == 'preview':
            i += 1  # Skip "Preview"
            
            # Skip any blank lines after "Preview"
            while i < len(processed_lines) and not processed_lines[i]:
                i += 1
        
        # Collect the remaining 8 fields (ID, Contacts, Status, Create Date, Last Activity, Last Reply, Priority, Owner)
        fields_needed = 8
        for field_num in range(fields_needed):
            # Skip any blank lines before each field
            while i < len(processed_lines) and not processed_lines[i]:
                i += 1
            
            if i < len(processed_lines) and processed_lines[i]:
                ticket_lines.append(processed_lines[i])
                i += 1
            else:
                break
        
        # Validate we have exactly 9 fields
        if len(ticket_lines) != 9:
            errors.append(f'Ticket {ticket_count}: Expected 9 fields, got {len(ticket_lines)}. Fields found: {ticket_lines}')
            # Try to continue parsing if there might be more tickets
            continue
        
        # Create ticket dictionary
        ticket_dict = {}
        for header, value in zip(HEADERS, ticket_lines):
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
    required_fields = ['TICKET NAME', 'TICKET ID', 'TICKET STATUS']
    
    for i, ticket in enumerate(data, 1):
        for field in required_fields:
            if not ticket.get(field, '').strip():
                errors.append(f'Row {i}: Missing required field "{field}"')
    
    return errors
