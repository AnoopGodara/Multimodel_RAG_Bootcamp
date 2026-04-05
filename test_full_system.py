import requests
import time
import sys
import os

BASE_URL = "http://localhost:8000"

def wait_for_server():
    print("Waiting for server to start...")
    for _ in range(60):
        try:
            requests.get(f"{BASE_URL}/health")
            print("Server is up!")
            return True
        except:
            time.sleep(2)
    return False

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_config():
    response = requests.get(f"{BASE_URL}/config")
    print(f"Config Check: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_ingest(file_path):
    print(f"Ingesting {file_path}...")
    with open(file_path, "rb") as f:
        response = requests.post(f"{BASE_URL}/ingest", files={"file": f})
    print(f"Ingest Result: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_query(query_text):
    print(f"Querying: {query_text}...")
    response = requests.post(f"{BASE_URL}/query", json={"query": query_text})
    print(f"Query Result: {response.status_code} - {response.json()}")
    return response.status_code == 200

if __name__ == "__main__":
    if not wait_for_server():
        print("Server failed to start")
        sys.exit(1)
    test_health()
    
    files = [
        "data/raw/IJCBS_04_01_003.pdf",
        "data/raw/Ergonomics in the Automotive Design Process.pdf"
    ]
    
    for f in files:
        if os.path.exists(f):
            test_ingest(f)
        else:
            print(f"File {f} not found")
    
    queries = [
        "What are the key ergonomic factors in automotive design?",
        "What is the future of car interiors according to the MXT lab document?",
        "Explain the dashboard usability study results."
    ]
    
    for q in queries:
        test_query(q)
