#!/usr/bin/env python3
"""
Test the new priority statistics feature
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import calculate_priority_stats

def test_priority_stats():
    """Test the priority statistics calculation"""
    print("📊 Testing Priority Statistics Feature...")
    
    # Create test data with various priorities
    test_data = [
        {'TICKET NAME': 'Critical System Down', 'PRIORITY': 'Urgent'},
        {'TICKET NAME': 'Server Error', 'PRIORITY': 'Urgent'},
        {'TICKET NAME': 'Database Issue', 'PRIORITY': 'High'},
        {'TICKET NAME': 'Performance Problem', 'PRIORITY': 'High'},
        {'TICKET NAME': 'Feature Request', 'PRIORITY': 'Medium'},
        {'TICKET NAME': 'Bug Report', 'PRIORITY': 'Medium'},
        {'TICKET NAME': 'Minor Issue', 'PRIORITY': 'Low'},
        {'TICKET NAME': 'Documentation Update', 'PRIORITY': 'Low'},
        {'TICKET NAME': 'Enhancement', 'PRIORITY': 'Low'},
    ]
    
    # Calculate priority statistics
    priority_stats = calculate_priority_stats(test_data)
    
    print(f"✅ Priority Statistics Calculated:")
    print(f"   Total tickets: {len(test_data)}")
    
    for stat in priority_stats:
        print(f"   {stat['name']}: {stat['count']} tickets (Color: {stat['color']})")
    
    # Verify the counts
    expected_counts = {'Urgent': 2, 'High': 2, 'Medium': 2, 'Low': 3}
    
    for stat in priority_stats:
        expected = expected_counts.get(stat['name'], 0)
        if stat['count'] != expected:
            print(f"❌ Error: Expected {expected} {stat['name']} tickets, got {stat['count']}")
            return False
    
    # Test color assignments
    color_map = {
        'Urgent': '#dc2626',
        'High': '#ef4444', 
        'Medium': '#f59e0b',
        'Low': '#10b981'
    }
    
    for stat in priority_stats:
        expected_color = color_map.get(stat['name'])
        if stat['color'] != expected_color:
            print(f"❌ Error: Expected {stat['name']} to have color {expected_color}, got {stat['color']}")
            return False
    
    print("✅ All priority statistics are correct!")
    return True

if __name__ == "__main__":
    success = test_priority_stats()
    if success:
        print("\n🎉 Priority statistics feature is working perfectly!")
        print("🎨 The color-coded priority breakdown will look amazing!")
    else:
        print("\n❌ Priority statistics test failed!")
        sys.exit(1)
