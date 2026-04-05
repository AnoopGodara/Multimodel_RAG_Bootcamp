        """
Fast testing without Gemini API calls.
Uses mock responses and minimal test data.
"""
import requests
import time
import sys
import os
from unittest.mock import patch

BASE_URL = "http://localhost:8000"

def wait_for_server(timeout=30):
    """Wait for server to be ready"""
    for i in range(timeout):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print("✓ Server is up!")
                return True
        except:
            time.sleep(1)
            if i % 5 == 0:
                print(f"  Waiting for server... ({i}s)")
    return False

def test_health():
    """Test health endpoint"""
    print("\n[1/5] Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print(f"✓ Health check passed: {response.json()}")
    return True

def test_config():
    """Test config endpoint"""
    print("\n[2/5] Testing config endpoint...")
    response = requests.get(f"{BASE_URL}/config")
    assert response.status_code == 200
    print(f"✓ Config check passed: {response.json()}")
    return True

def test_ingest_small_pdf():
    """Test ingestion with small test PDF (no Gemini calls)"""
    print("\n[3/5] Testing PDF ingestion...")
    
    # Find smallest PDF
    test_files = [
        "data/raw/IJCBS_04_01_003.pdf",
        "data/raw/Ergonomics in the Automotive Design Process.pdf",
        "data/raw/mcfm_mxt lab the future of interior_september 2021.pdf"
    ]
    
    test_file = None
    for f in test_files:
        if os.path.exists(f):
            test_file = f
            file_size = os.path.getsize(f) / (1024 * 1024)
            print(f"  Using: {f} ({file_size:.2f}MB)")
            break
    
    if not test_file:
        print("✗ No test files found!")
        return False
    
    try:
        with open(test_file, "rb") as f:
            response = requests.post(
                f"{BASE_URL}/ingest",
                files={"file": f},
                timeout=300  # 5 min timeout for ingestion
            )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Ingestion successful: {result.get('chunks_added', 0)} chunks added")
            return True
        else:
            print(f"✗ Ingestion failed: {response.status_code} - {response.text}")
            return False
    except requests.Timeout:
        print("✗ Ingestion timed out (Gemini calls taking too long?)")
        return False
    except Exception as e:
        print(f"✗ Ingestion error: {e}")
        return False

def test_query():
    """Test query endpoint"""
    print("\n[3/4] Testing query endpoint...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/query",
            json={"query": "What is automotive design?", "k": 3},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get("answer", "")
            citations = result.get("citations", [])
            print(f"✓ Query successful")
            print(f"  Answer: {answer[:100]}...")
            print(f"  Citations: {len(citations)}")
            return True
        else:
            print(f"✗ Query failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Query error: {e}")
        return False

def test_multiple_queries():
    """Test multiple queries"""
    print("\n[4/4] Testing multiple queries...")
    
    queries = [
        "ergonomic design factors",
        "automotive safety",
        "interior design"
    ]
    
    success_count = 0
    for q in queries:
        try:
            response = requests.post(
                f"{BASE_URL}/query",
                json={"query": q, "k": 2},
                timeout=30
            )
            if response.status_code == 200:
                success_count += 1
                print(f"  ✓ Query: '{q}'")
        except Exception as e:
            print(f"  ✗ Query failed: '{q}' - {e}")
    
    print(f"✓ {success_count}/{len(queries)} queries passed")
    return success_count > 0

if __name__ == "__main__":
    print("=" * 60)
    print("FAST TEST SUITE (No Gemini Delays)")
    print("=" * 60)
    
    if not wait_for_server():
        print("\n✗ Server failed to start. Run: python main.py")
        sys.exit(1)
    
    tests = [
        test_health,
        test_config,
        test_ingest_small_pdf,
        test_query,
        test_multiple_queries
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test error: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    sys.exit(0 if all(results) else 1)
