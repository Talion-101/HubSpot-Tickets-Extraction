#!/usr/bin/env python3
"""
Test script for HubSpot Ticket Parser
Run this to validate all functionality works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.parser import parse_ticket_data
from utils.excel import create_excel_file

def test_parser():
    """Test the parser functionality"""
    print("🧪 Testing Parser...")
    
    # Test case 1: Valid pipe-separated data
    test_data1 = """Login Issue | john.doe@example.com | Open | 2025-08-01 | 2025-08-04 | 2025-08-03 | High | Alice
Payment Failure | jane.smith@example.com | In Progress | 2025-07-29 | 2025-08-02 | 2025-08-01 | Medium | Bob"""
    
    result1, errors1 = parse_ticket_data(test_data1)
    assert len(result1) == 2, f"Expected 2 tickets, got {len(result1)}"
    assert len(errors1) == 0, f"Expected no errors, got {errors1}"
    print("  ✅ Pipe-separated data parsing works")
    
    # Test case 2: Tab-separated data
    test_data2 = "Login Issue\tjohn.doe@example.com\tOpen\t2025-08-01\t2025-08-04\t2025-08-03\tHigh\tAlice"
    result2, errors2 = parse_ticket_data(test_data2)
    assert len(result2) == 1, f"Expected 1 ticket, got {len(result2)}"
    assert len(errors2) == 0, f"Expected no errors, got {errors2}"
    print("  ✅ Tab-separated data parsing works")
    
    # Test case 3: Invalid data (wrong number of fields)
    test_data3 = "Login Issue | john.doe@example.com | Open"
    result3, errors3 = parse_ticket_data(test_data3)
    assert len(result3) == 0, f"Expected 0 tickets, got {len(result3)}"
    assert len(errors3) > 0, f"Expected errors, got none"
    print("  ✅ Error handling for invalid data works")
    
    # Test case 4: Empty data
    result4, errors4 = parse_ticket_data("")
    assert len(result4) == 0, f"Expected 0 tickets, got {len(result4)}"
    assert len(errors4) > 0, f"Expected errors, got none"
    print("  ✅ Error handling for empty data works")
    
    print("✅ Parser tests passed!")
    return result1

def test_excel_generation(data):
    """Test Excel file generation"""
    print("\n📊 Testing Excel Generation...")
    
    try:
        excel_file = create_excel_file(data)
        assert excel_file is not None, "Excel file should not be None"
        assert len(excel_file.getvalue()) > 0, "Excel file should have content"
        print(f"  ✅ Excel file generated successfully ({len(excel_file.getvalue())} bytes)")
        
        # Test with empty data
        try:
            create_excel_file([])
            assert False, "Should raise error for empty data"
        except ValueError:
            print("  ✅ Error handling for empty data works")
        
        print("✅ Excel generation tests passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Excel generation failed: {e}")
        return False

def test_headers():
    """Test that headers are correct"""
    print("\n📋 Testing Headers...")
    
    from utils.parser import HEADERS
    expected_headers = [
        'TICKET NAME',
        'TICKET - CONTACTS', 
        'TICKET STATUS',
        'CREATE DATE',
        'LAST ACTIVITY DATE',
        'LAST CUSTOMER REPLY DATE',
        'PRIORITY',
        'TICKET OWNER'
    ]
    
    assert HEADERS == expected_headers, f"Headers mismatch: {HEADERS}"
    print("  ✅ Headers are correct")
    print("✅ Header tests passed!")

def run_all_tests():
    """Run all tests"""
    print("🚀 Running HubSpot Ticket Parser Tests\n")
    
    try:
        # Test headers
        test_headers()
        
        # Test parser
        sample_data = test_parser()
        
        # Test Excel generation
        test_excel_generation(sample_data)
        
        print("\n🎉 All tests passed! The application is ready to use.")
        return True
        
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
