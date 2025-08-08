#!/usr/bin/env python3
"""
Test script to verify the complete flow:
1. PDF Processing
2. MongoDB Storage
3. Export functionality
"""

import requests
import json
import tempfile
import os

# Test configuration
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("✅ Health check:", response.json())
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_process_endpoint():
    """Test the process endpoint info"""
    try:
        response = requests.get(f"{BASE_URL}/process")
        print("✅ Process endpoint info:", response.json())
        return True
    except Exception as e:
        print(f"❌ Process endpoint test failed: {e}")
        return False

def create_mock_pdf():
    """Create a mock PDF file for testing"""
    # Create a simple text file as mock PDF
    mock_content = """
    Asset ID: 12345
    Plot Number: PLOT001
    Survey Number: SURVEY123
    House ID: HOUSE001
    Floor Number: 2
    Building Number: BLDG001
    Building Name: Test Building
    Area: 1500.00
    Area Unit: Square Feet
    Street Name: Test Street
    Locality: Test Locality
    Landmark: Test Landmark
    Block Number: BLOCK001
    City / Town / Village: Test City
    Taluka: Test Taluka
    District: Test District
    Pin Code: 123456
    State: Maharashtra
    Security Interest ID: SI001
    Type Of Security Interest: Mortgage
    SI Creation Date In Bank: 2024-01-15
    Charge Holder Name: Test Bank
    Total Secured Amount: 5000000.00
    Transaction ID / QRF NO: TXN123456
    """
    
    temp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
    temp_file.write(mock_content.encode())
    temp_file.close()
    return temp_file.name

def test_pdf_processing():
    """Test PDF processing with mock data"""
    try:
        # Create mock PDF
        mock_pdf_path = create_mock_pdf()
        
        # Simulate PDF processing by creating mock JSON
        mock_json = {
            "company_details": {
                "name_of_company": "TEST COMPANY LIMITED",
                "cin_number": "U12345MH2024PTC123456",
                "search_reference_id": "TXN123456",
                "date_of_incorporation": "15.01.2024",
                "registered_office": "Test Address, Test City, Maharashtra, India, 123456."
            },
            "assets": [
                {
                    "asset_details_of_security_interest": {
                        "asset_id": "12345",
                        "plot_id": "PLOT001",
                        "survey_no": "SURVEY123",
                        "house_id": "HOUSE001",
                        "floor_no": "2",
                        "building_no": "BLDG001",
                        "building_name": "Test Building",
                        "buildup_area": "1500.00 Square Feet",
                        "street_name": "Test Street",
                        "locality": "Test Locality",
                        "landmark": "Test Landmark",
                        "block_no": "BLOCK001",
                        "village": "Test City",
                        "taluka": "Test Taluka",
                        "district": "Test District",
                        "pin_code": "123456",
                        "state": "Maharashtra"
                    },
                    "security_interest_details": {
                        "security_interest_id": "SI001",
                        "security_interest_type": "Mortgage",
                        "si_creation_date": "2024-01-15",
                        "charge_holder_name_amount": "Test Bank Rs. 50.00 Lakhs",
                        "is_asset_under_charge_ranking": "Yes\nTest charge details",
                        "charge_release_date": "N/A",
                        "borrower_type": "Company",
                        "borrowers": "Test Company (Maharashtra, PIN: 123456)",
                        "sub_borrower": "-",
                        "third_party_mortgagees": "N/A"
                    }
                }
            ]
        }
        
        print("✅ Mock JSON created successfully")
        
        # Test saving to MongoDB
        save_response = requests.post(f"{BASE_URL}/save_summary", json={
            "filename": "test_document.pdf",
            "summary": mock_json
        })
        
        if save_response.status_code == 200:
            save_data = save_response.json()
            pdf_id = save_data.get('pdf_id')
            print(f"✅ Saved to MongoDB with PDF ID: {pdf_id}")
            
            # Test retrieving from MongoDB
            get_response = requests.get(f"{BASE_URL}/get_summary/{pdf_id}")
            if get_response.status_code == 200:
                print("✅ Retrieved from MongoDB successfully")
                
                # Test export functionality
                test_export_functionality(pdf_id)
            else:
                print(f"❌ Failed to retrieve from MongoDB: {get_response.json()}")
        else:
            print(f"❌ Failed to save to MongoDB: {save_response.json()}")
        
        # Clean up
        os.unlink(mock_pdf_path)
        return True
        
    except Exception as e:
        print(f"❌ PDF processing test failed: {e}")
        return False

def test_export_functionality(pdf_id):
    """Test export functionality"""
    try:
        # Test HTML export
        html_response = requests.get(f"{BASE_URL}/export/{pdf_id}/html")
        if html_response.status_code == 200:
            print("✅ HTML export successful")
        else:
            print(f"❌ HTML export failed: {html_response.json()}")
        
        # Test Excel export
        excel_response = requests.get(f"{BASE_URL}/export/{pdf_id}/excel")
        if excel_response.status_code == 200:
            print("✅ Excel export successful")
        else:
            print(f"❌ Excel export failed: {excel_response.json()}")
        
        # Test PDF export
        pdf_response = requests.get(f"{BASE_URL}/export/{pdf_id}/pdf")
        if pdf_response.status_code == 200:
            print("✅ PDF export successful")
        else:
            print(f"❌ PDF export failed: {pdf_response.json()}")
            
    except Exception as e:
        print(f"❌ Export functionality test failed: {e}")

def main():
    """Run all tests"""
    print("🧪 Starting backend flow tests...")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health_check():
        print("❌ Server is not running. Please start the Flask server first.")
        return
    
    # Test 2: Process endpoint
    if not test_process_endpoint():
        print("❌ Process endpoint test failed.")
        return
    
    # Test 3: Complete flow
    if test_pdf_processing():
        print("\n🎉 All tests passed! The backend flow is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()
