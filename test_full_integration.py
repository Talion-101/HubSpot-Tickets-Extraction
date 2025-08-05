#!/usr/bin/env python3
"""
Integration test for priority statistics with full workflow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.parser import parse_ticket_data
from app import calculate_priority_stats

def test_full_integration():
    """Test the complete workflow with priority statistics"""
    print("🚀 Testing Full Integration with Priority Statistics...")
    
    # Test data with mixed priorities using new HubSpot format
    hubspot_data = """Critical System Outage

Preview
88888888888
John Doe (john.doe@company.com)
Open
Aug 5, 2025 9:00 AM GMT+5:30
Aug 5, 2025 9:30 AM GMT+5:30
Aug 5, 2025 9:15 AM GMT+5:30
Urgent
Tech Support Team

Database Performance Issue

Preview
77777777777
Jane Smith
In Progress
Aug 5, 2025 10:00 AM GMT+5:30
Aug 5, 2025 11:00 AM GMT+5:30
Aug 5, 2025 10:30 AM GMT+5:30
High
Database Admin

Feature Enhancement Request

Preview
66666666666
Bob Johnson
New
Aug 5, 2025 8:00 AM GMT+5:30
Aug 5, 2025 8:30 AM GMT+5:30
Aug 5, 2025 8:15 AM GMT+5:30
Medium
Product Manager

Minor UI Tweak

Preview
55555555555
Alice Wilson
Closed
Aug 4, 2025 3:00 PM GMT+5:30
Aug 4, 2025 4:00 PM GMT+5:30
Aug 4, 2025 3:30 PM GMT+5:30
Low
UI/UX Team"""

    # Parse the data
    parsed_data, errors = parse_ticket_data(hubspot_data)
    
    print(f"✅ Parsing Results:")
    print(f"   - Tickets parsed: {len(parsed_data)}")
    print(f"   - Errors: {len(errors)}")
    
    if errors:
        print(f"   - Error details: {errors}")
        return False
    
    if len(parsed_data) != 4:
        print(f"❌ Expected 4 tickets, got {len(parsed_data)}")
        return False
    
    # Calculate priority statistics
    priority_stats = calculate_priority_stats(parsed_data)
    
    print(f"\n📊 Priority Statistics:")
    total_tickets = sum(stat['count'] for stat in priority_stats)
    print(f"   Total Tickets: {total_tickets}")
    
    for stat in priority_stats:
        print(f"   {stat['name']}: {stat['count']} tickets")
        print(f"      Color: {stat['color']}")
    
    # Verify we have the expected distribution
    expected_distribution = {
        'Urgent': 1,
        'High': 1, 
        'Medium': 1,
        'Low': 1
    }
    
    actual_distribution = {stat['name']: stat['count'] for stat in priority_stats}
    
    for priority, expected_count in expected_distribution.items():
        actual_count = actual_distribution.get(priority, 0)
        if actual_count != expected_count:
            print(f"❌ Expected {expected_count} {priority} tickets, got {actual_count}")
            return False
    
    print(f"\n🎯 Sample Parsed Tickets:")
    for i, ticket in enumerate(parsed_data, 1):
        print(f"   Ticket {i}: {ticket['TICKET NAME']} - Priority: {ticket['PRIORITY']}")
    
    return True

if __name__ == "__main__":
    success = test_full_integration()
    if success:
        print("\n🎉 Full integration test passed!")
        print("🌟 Priority statistics feature is ready for production!")
        print("🎨 Users will love the color-coded priority breakdown!")
    else:
        print("\n❌ Integration test failed!")
        sys.exit(1)
