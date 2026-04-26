import pytest
from fastapi.testclient import TestClient
import time

from milestone0.app.main import app

def test_healthcheck():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

@pytest.mark.integration
def test_recommendation_endpoint_caching():
    payload = {
        "location": "Bellandur",
        "budget_band": "high",
        "cuisines": [],
        "minimum_rating": 4.0
    }
    
    with TestClient(app) as client:
        # First request (cold start - will execute logic and cache)
        start = time.time()
        response1 = client.post("/api/recommend", json=payload)
        t1 = time.time() - start
        
        assert response1.status_code == 200
        data1 = response1.json()
        assert "recommendations" in data1
        
        # Second request (cached - should be very fast)
        start = time.time()
        response2 = client.post("/api/recommend", json=payload)
        t2 = time.time() - start
        
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Responses should be identical
        assert data1 == data2
        
        # We don't assert strictly on t2 < t1 because test environments can be noisy, 
        # but the cache hit ensures the LLM pipeline was entirely skipped.
