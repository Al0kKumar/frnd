from typing import List, Dict
from app.models.hotel import Hotel

# In-memory data structures for storage of hotels for search feature
hotels_list: List[Hotel] = []      # array
city_map: Dict[str, List[Hotel]] = {}   # map
name_map: Dict[str, List[Hotel]] = {}   # map

def load_hotels_mock(num_hotels: int = 1_000_000, num_cities: int = 100):
    """
    fill hotels_list, city_map, and name_map with mock data
    num_hotels: total number of hotels
    num_cities: number of unique cities
    """
    global hotels_list, city_map, name_map
    hotels_list.clear()
    city_map.clear()
    name_map.clear()

    for i in range(num_hotels):
        city_name = f"City{i % num_cities}"        
        hotel_name = f"Hotel{i}"                  
        hotel = Hotel(id=i, name=hotel_name, city=city_name)
        hotels_list.append(hotel)

        
        city_map.setdefault(city_name.lower(), []).append(hotel)
        
        name_map.setdefault(hotel_name.lower(), []).append(hotel)

    print(f"Loaded {num_hotels} hotels into memory with {num_cities} unique cities.")

