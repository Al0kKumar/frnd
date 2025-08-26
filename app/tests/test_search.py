import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.routes.search_routes import search_hotels
from app.utils.load_hotels import load_hotels_mock

# load 1M mock hotels before running tests
load_hotels_mock(num_hotels=1_000_000, num_cities=100)

def test_search_by_city():
    city = "City5"
    results = search_hotels(city=city, name=None, limit=100)
    assert all(h.city.lower() == city.lower() for h in results)
    assert len(results) <= 100  #  limit

def test_search_by_name():
    name = "Hotel12345"
    results = search_hotels(city=None, name=name, limit=10)
    assert all(h.name.lower() == name.lower() for h in results)
    assert len(results) <= 10

def test_search_by_city_and_name():
    city = "City12"
    name = "Hotel112"
    results = search_hotels(city=city, name=name, limit=10)
    for h in results:
        assert h.city.lower() == city.lower()
        assert h.name.lower() == name.lower()
    assert len(results) <= 10

def test_search_no_filters():
    results = search_hotels(city=None, name=None, limit=50)
    assert len(results) == 50  # limit 
