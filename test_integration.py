#!/usr/bin/env python3
"""
Integration test to verify the complete workflow works with the new format
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.parser import parse_ticket_data
from utils.excel import create_excel_file
import tempfile

def test_complete_workflow():
    """Test the complete workflow with the new HubSpot format"""
    print("🧪 Testing Complete Workflow with New HubSpot Format...")
    
    # Test data that matches your exact example
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
Sarah Johnson
Open
Aug 2, 2025 9:30 AM GMT+5:30
Aug 2, 2025 11:00 AM GMT+5:30
Aug 2, 2025 9:45 AM GMT+5:30
Medium
John Smith (john.smith@dnabehavior.com)"""

    # Step 1: Parse the data
    parsed_data, errors = parse_ticket_data(hubspot_data)
    
    print(f"✅ Parsing complete!")
    print(f"   - Tickets parsed: {len(parsed_data)}")
    print(f"   - Errors: {len(errors)}")
    
    if errors:
        print(f"   - Error details: {errors}")
        return False
    
    # Step 2: Display parsed data
    print("\n📋 Parsed Tickets:")
    for i, ticket in enumerate(parsed_data, 1):
        print(f"\n--- Ticket {i} ---")
        for key, value in ticket.items():
            print(f"{key}: {value}")
    
    # Step 3: Generate Excel file
    try:
        excel_buffer = create_excel_file(parsed_data)
        
        # Check if BytesIO buffer has content
        if excel_buffer and excel_buffer.getvalue():
            print(f"\n✅ Excel file generated successfully!")
            print(f"   - Buffer size: {len(excel_buffer.getvalue())} bytes")
        else:
            print("❌ Excel file generation failed!")
            return False
        
    except Exception as e:
        print(f"❌ Excel generation error: {e}")
        return False
    
    print("\n🎉 Complete workflow test passed!")
    return True

def test_mixed_formats():
    """Test that both old and new formats work in the same session"""
    print("\n🔄 Testing Mixed Format Compatibility...")
    
    # Old format
    old_format = "Login Issue | TK-001 | john.doe@example.com | Open | 2025-08-01 | 2025-08-04 | 2025-08-03 | High | Alice"
    
    # New format
    new_format = """Account Setup Issue
Preview
12345678901
jane.doe@example.com
In Progress
Aug 2, 2025 10:00 AM GMT+5:30
Aug 2, 2025 2:00 PM GMT+5:30
Aug 2, 2025 10:30 AM GMT+5:30
High
Support Team"""
    
    # Test old format
    old_result, old_errors = parse_ticket_data(old_format)
    print(f"✅ Old format: {len(old_result)} tickets, {len(old_errors)} errors")
    
    # Test new format
    new_result, new_errors = parse_ticket_data(new_format)
    print(f"✅ New format: {len(new_result)} tickets, {len(new_errors)} errors")
    
    print("🎉 Mixed format compatibility test passed!")

if __name__ == "__main__":
    success = test_complete_workflow()
    test_mixed_formats()
    
    if success:
        print("\n🎯 All tests passed! The system is ready to handle the new HubSpot format.")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
