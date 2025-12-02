#!/usr/bin/env python3
"""
Test script to verify the frontend-backend connection.
This script tests the Flask API endpoints.
"""

import requests
import json
import time

def test_api_connection():
    """Test the Flask API endpoints."""
    base_url = "http://localhost:5000"
    
    print("Testing Python Calculator API Connection...")
    print("=" * 60)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
        else:
            print("✗ Health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure Flask app is running.")
        print("  Run: python app.py")
        return False
    
    # Test calculation endpoints
    test_cases = [
        {"operation": "add", "operand1": 10, "operand2": 5, "expected": 15},
        {"operation": "subtract", "operand1": 10, "operand2": 3, "expected": 7},
        {"operation": "multiply", "operand1": 4, "operand2": 6, "expected": 24},
        {"operation": "divide", "operand1": 15, "operand2": 3, "expected": 5},
        {"operation": "power", "operand1": 2, "operand2": 3, "expected": 8},
    ]
    
    print("\nTesting calculation endpoints...")
    for i, test in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{base_url}/calculate",
                json={
                    "operation": test["operation"],
                    "operand1": test["operand1"],
                    "operand2": test["operand2"]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data["result"]
                if result == test["expected"]:
                    print(f"✓ Test {i}: {test['operand1']} {test['operation']} {test['operand2']} = {result}")
                else:
                    print(f"✗ Test {i}: Expected {test['expected']}, got {result}")
            else:
                print(f"✗ Test {i}: HTTP {response.status_code} - {response.text}")
        except Exception as e:
            print(f"✗ Test {i}: Error - {e}")
    
    # Test history endpoint
    try:
        response = requests.get(f"{base_url}/history")
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ History endpoint working - {len(data['history'])} calculations")
        else:
            print(f"\n✗ History endpoint failed - HTTP {response.status_code}")
    except Exception as e:
        print(f"\n✗ History endpoint error - {e}")
    
    # Test clear history endpoint
    try:
        response = requests.post(f"{base_url}/clear_history")
        if response.status_code == 200:
            print("✓ Clear history endpoint working")
        else:
            print(f"✗ Clear history endpoint failed - HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ Clear history endpoint error - {e}")
    
    print("\n" + "=" * 60)
    print("API testing completed!")
    print("Frontend should now be able to connect to the backend.")
    return True

if __name__ == "__main__":
    test_api_connection()