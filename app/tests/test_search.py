import sys
import os
from fastapi.testclient import TestClient

# Ensure correct path resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.main import app
from app.utils.load_hotels import load_hotels_mock

client = TestClient(app)

# Load mock data before tests
load_hotels_mock(num_hotels=1_000_000, num_cities=100)

def test_search_by_city():
    city = "City5"
    response = client.get("/search", params={"city": city, "limit": 100})
    results = response.json()
    assert all(h["city"].lower() == city.lower() for h in results)
    assert len(results) <= 100

def test_search_by_name():
    name = "Hotel12345"
    response = client.get("/search", params={"name": name, "limit": 10})
    results = response.json()
    assert all(h["name"].lower() == name.lower() for h in results)
    assert len(results) <= 10

def test_search_by_city_and_name():
    city = "City12"
    name = "Hotel112"
    response = client.get("/search", params={"city": city, "name": name, "limit": 10})
    results = response.json()
    for h in results:
        assert h["city"].lower() == city.lower()
        assert h["name"].lower() == name.lower()
    assert len(results) <= 10

def test_search_no_filters():
    response = client.get("/search", params={"limit": 50})
    results = response.json()
    assert len(results) == 50
