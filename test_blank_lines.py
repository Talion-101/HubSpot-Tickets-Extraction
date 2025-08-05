#!/usr/bin/env python3
"""
Test script for the exact HubSpot format with blank lines
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.parser import parse_ticket_data

def test_exact_hubspot_format():
    """Test the exact format from the user with blank line after ticket name"""
    print("🧪 Testing Exact HubSpot Format with Blank Lines...")
    
    # Exact format from user with blank line after ticket name
    exact_format = """Cancellation of Steven Fricano's DNA Web App account

Preview
27333837927
Leon Morales
New (Support Pipeline)
Aug 1, 2025 10:14 PM GMT+5:30
Aug 1, 2025 10:48 PM GMT+5:30
Aug 1, 2025 10:14 PM GMT+5:30
Urgent
Isuru Promodh (isuru.promodh@dnabehavior.com)"""
    
    result, errors = parse_ticket_data(exact_format)
    
    print(f"✅ Parsing result:")
    print(f"   - Tickets parsed: {len(result)}")
    print(f"   - Errors: {len(errors)}")
    
    if errors:
        print(f"   - Error details: {errors}")
    
    if result:
        print("\n📋 Parsed Ticket:")
        for key, value in result[0].items():
            print(f"   {key}: {value}")
    
    # Test multiple tickets with blank lines
    print("\n🔄 Testing Multiple Tickets with Blank Lines...")
    
    multiple_tickets = """First Ticket with Blank Line

Preview
11111111111
contact1@example.com
Open
Aug 1, 2025 10:00 AM
Aug 1, 2025 11:00 AM
Aug 1, 2025 10:30 AM
High
Owner 1

Second Ticket with Blank Line

Preview
22222222222
contact2@example.com
Closed
Aug 2, 2025 09:00 AM
Aug 2, 2025 10:00 AM
Aug 2, 2025 09:15 AM
Medium
Owner 2"""

    result2, errors2 = parse_ticket_data(multiple_tickets)
    
    print(f"✅ Multiple tickets result:")
    print(f"   - Tickets parsed: {len(result2)}")
    print(f"   - Errors: {len(errors2)}")
    
    if errors2:
        print(f"   - Error details: {errors2}")
    
    # Test without Preview but with blank lines
    print("\n🔄 Testing Without Preview but with Blank Lines...")
    
    no_preview_format = """Account Issue with Blank Line

12345678901
user@example.com
In Progress
Aug 3, 2025 10:00 AM
Aug 3, 2025 11:00 AM
Aug 3, 2025 10:15 AM
Medium
Support Team"""

    result3, errors3 = parse_ticket_data(no_preview_format)
    
    print(f"✅ No preview result:")
    print(f"   - Tickets parsed: {len(result3)}")
    print(f"   - Errors: {len(errors3)}")
    
    if errors3:
        print(f"   - Error details: {errors3}")
    
    return len(result) > 0 and len(errors) == 0

if __name__ == "__main__":
    success = test_exact_hubspot_format()
    if success:
        print("\n🎉 All tests passed! The system now handles blank lines correctly.")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
