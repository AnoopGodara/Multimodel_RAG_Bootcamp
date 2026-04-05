import requests
import time
import sys
import os

BASE_URL = "http://localhost:8000"

def wait_for_server():
    for _ in range(30):
        try:
            requests.get(f"{BASE_URL}/health")
            return True
        except:
            time.sleep(2)
    return False

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.json()}")
    return response.status_code == 200

def test_config():
    response = requests.get(f"{BASE_URL}/config")
    print(f"Config Check: {response.json()}")
    return response.status_code == 200

def test_ingest(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(f"{BASE_URL}/ingest", files={"file": f})
    print(f"Ingest Result: {response.json()}")
    return response.status_code == 200

def test_query(query_text):
    response = requests.post(f"{BASE_URL}/query", json={"query": query_text})
    print(f"Query Result: {response.json()}")
    return response.status_code == 200

if __name__ == "__main__":
    if not wait_for_server():
        print("Server failed to start")
        sys.exit(1)
    
    test_health()
    test_config()
    test_ingest("data/raw/IJCBS_04_01_003.pdf")
    test_query("What is the automotive design focus in this document?")
