"""
Simple test script for the RAG API
Run this after starting the Flask server to test all endpoints
"""

import requests
import json

# BASE_URL = "http://localhost:5000"
BASE_URL = "https://myaiassistant-ijpe.onrender.com"

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*50)
    print("Testing Health Check Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_query(query_text="which department mohabbat study?", top_k=3):
    """Test query endpoint with LLM summarization"""
    print("\n" + "="*50)
    print("Testing Query Endpoint (with LLM)")
    print("="*50)
    
    payload = {
        "query": query_text,
        "top_k": top_k
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Query: {query_text}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_search(query_text="mohabbat", top_k=3):
    """Test search endpoint without LLM"""
    print("\n" + "="*50)
    print("Testing Search Endpoint (raw results)")
    print("="*50)
    
    payload = {
        "query": query_text,
        "top_k": top_k
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/search",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Query: {query_text}")
        
        data = response.json()
        if response.status_code == 200:
            print(f"\nFound {len(data.get('results', []))} results:")
            for i, result in enumerate(data.get('results', [])[:2], 1):
                print(f"\nResult {i}:")
                print(f"  Distance: {result.get('distance')}")
                print(f"  Text Preview: {result.get('text', '')[:100]}...")
        else:
            print(f"Response: {json.dumps(data, indent=2)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid requests"""
    print("\n" + "="*50)
    print("Testing Error Handling")
    print("="*50)
    
    # Test 1: Missing query
    print("\n1. Testing missing query parameter:")
    try:
        response = requests.post(
            f"{BASE_URL}/api/query",
            json={},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Empty query
    print("\n2. Testing empty query:")
    try:
        response = requests.post(
            f"{BASE_URL}/api/query",
            json={"query": ""},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Invalid top_k
    print("\n3. Testing invalid top_k:")
    try:
        response = requests.post(
            f"{BASE_URL}/api/query",
            json={"query": "test", "top_k": 100},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all tests"""
    print("\n" + "#"*50)
    print("RAG API Test Suite")
    print("#"*50)
    
    results = {
        "Health Check": test_health(),
        "Query Endpoint": test_query(),
        "Search Endpoint": test_search(),
    }
    
    # Error handling tests (not counted in pass/fail)
    test_error_handling()
    
    # Summary
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")

if __name__ == "__main__":
    main()
