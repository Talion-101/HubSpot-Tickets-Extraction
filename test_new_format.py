#!/usr/bin/env python3
"""
Test script specifically for the new HubSpot format
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.parser import parse_ticket_data

def test_new_hubspot_format():
    """Test the new HubSpot line-by-line format"""
    print("🧪 Testing New HubSpot Format...")
    
    # Test case 1: New format with Preview
    test_data_with_preview = """Cancellation of Steven Fricano's DNA Web App account
Preview
27333837927
Leon Morales
New (Support Pipeline)
Aug 1, 2025 10:14 PM GMT+5:30
Aug 1, 2025 10:48 PM GMT+5:30
Aug 1, 2025 10:14 PM GMT+5:30
Urgent
Isuru Promodh (isuru.promodh@dnabehavior.com)"""
    
    result1, errors1 = parse_ticket_data(test_data_with_preview)
    
    print(f"Parsed {len(result1)} tickets")
    print(f"Errors: {errors1}")
    
    if result1:
        print("\nFirst ticket:")
        for key, value in result1[0].items():
            print(f"  {key}: {value}")
    
    # Test case 2: New format without Preview
    test_data_without_preview = """Account Setup Issue
12345678901
john.doe@example.com
Open
Aug 2, 2025 10:00 AM GMT+5:30
Aug 2, 2025 2:00 PM GMT+5:30
Aug 2, 2025 10:30 AM GMT+5:30
High
Support Team (support@example.com)"""
    
    result2, errors2 = parse_ticket_data(test_data_without_preview)
    
    print(f"\nSecond test - Parsed {len(result2)} tickets")
    print(f"Errors: {errors2}")
    
    if result2:
        print("\nSecond ticket:")
        for key, value in result2[0].items():
            print(f"  {key}: {value}")
    
    # Test case 3: Multiple tickets with Preview
    test_multiple_tickets = """First Ticket Name
Preview
11111111111
contact1@example.com
Open
Aug 1, 2025 10:00 AM
Aug 1, 2025 11:00 AM
Aug 1, 2025 10:30 AM
High
Owner 1

Second Ticket Name
Preview
22222222222
contact2@example.com
Closed
Aug 2, 2025 09:00 AM
Aug 2, 2025 10:00 AM
Aug 2, 2025 09:15 AM
Medium
Owner 2"""
    
    result3, errors3 = parse_ticket_data(test_multiple_tickets)
    
    print(f"\nMultiple tickets test - Parsed {len(result3)} tickets")
    print(f"Errors: {errors3}")
    
    return result1, result2, result3

if __name__ == "__main__":
    test_new_hubspot_format()
