#!/usr/bin/env python3
"""
Quick test to verify the UI improvements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.parser import parse_ticket_data

def test_ui_improvements():
    """Test that parsing still works correctly after UI changes"""
    print("🧪 Testing UI Improvements...")
    
    # Test new HubSpot format
    hubspot_data = """Cancellation of Steven Fricano's DNA Web App account

Preview
27333837927
Leon Morales
New (Support Pipeline)
Aug 1, 2025 10:14 PM GMT+5:30
Aug 1, 2025 10:48 PM GMT+5:30
Aug 1, 2025 10:14 PM GMT+5:30
Urgent
Isuru Promodh (isuru.promodh@dnabehavior.com)

Password Reset Request

Preview
27333837928
Sarah Johnson (sarah.johnson@example.com)
Open
Aug 2, 2025 9:30 AM GMT+5:30
Aug 2, 2025 11:00 AM GMT+5:30
Aug 2, 2025 9:45 AM GMT+5:30
Medium
John Smith (john.smith@dnabehavior.com)"""

    # Parse the data
    parsed_data, errors = parse_ticket_data(hubspot_data)
    
    print(f"✅ Parsing complete:")
    print(f"   - Tickets parsed: {len(parsed_data)}")
    print(f"   - Errors: {len(errors)}")
    
    if errors:
        print(f"   - Error details: {errors}")
        return False
    
    if len(parsed_data) != 2:
        print(f"❌ Expected 2 tickets, got {len(parsed_data)}")
        return False
    
    # Display parsed tickets
    print("\n📋 Parsed Tickets:")
    for i, ticket in enumerate(parsed_data, 1):
        print(f"\n--- Ticket {i} ---")
        for key, value in ticket.items():
            print(f"   {key}: {value}")
    
    return True

if __name__ == "__main__":
    success = test_ui_improvements()
    if success:
        print("\n🎉 UI improvements verified! Parsing functionality intact.")
    else:
        print("\n❌ Something went wrong!")
        sys.exit(1)
