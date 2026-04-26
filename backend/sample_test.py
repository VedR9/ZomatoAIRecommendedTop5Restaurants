import time
import json
from fastapi.testclient import TestClient
from milestone0.app.main import app

payload = {
    "location": "Indiranagar",
    "budget_band": "medium",
    "cuisines": ["Cafe", "Desserts"],
    "minimum_rating": 4.2
}

print("Starting sample test using FastAPI TestClient...")
print(f"Request Payload: {json.dumps(payload, indent=2)}")

# The context manager triggers the lifespan event to load the dataset
print("\nLoading dataset and initializing app...")
with TestClient(app) as client:
    print("\n--- FIRST REQUEST (COLD START) ---")
    start = time.time()
    response1 = client.post("/api/recommend", json=payload)
    latency1 = time.time() - start
    print(f"Status: {response1.status_code}")
    print(f"Time Taken: {latency1:.2f} seconds")
    print("Recommendations:")
    for rec in response1.json().get("recommendations", []):
        print(f"  #{rec['rank']} {rec['restaurant_name']} - {rec['reasoning']}")
    
    print("\n--- SECOND REQUEST (CACHED) ---")
    start = time.time()
    response2 = client.post("/api/recommend", json=payload)
    latency2 = time.time() - start
    print(f"Status: {response2.status_code}")
    print(f"Time Taken: {latency2:.4f} seconds")
    print("Recommendations:")
    for rec in response2.json().get("recommendations", []):
        print(f"  #{rec['rank']} {rec['restaurant_name']} - {rec['reasoning']}")
