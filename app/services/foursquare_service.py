import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")

HEADERS = {
    "Authorization": FOURSQUARE_API_KEY
}

CATEGORY_MAP = {
    "galleries": "4bf58dd8d48988d1e2931735",  # Contemporary Art Galleries
    "auctions": "12031",                      # Auction Houses
    "restaurants": "13065",                   # Fine Dining Restaurants
}

def search_places(lat: float, lon: float, category: str, radius: int = 3000):
    category_id = CATEGORY_MAP.get(category.lower())
    if not category_id:
        print(f"[Foursquare] Invalid category: {category}")
        return []

    url = "https://api.foursquare.com/v3/places/search"
    params = {
        "ll": f"{lat},{lon}",
        "categories": category_id,
        "radius": radius,
        "open_now": True,
        "limit": 20
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"[Foursquare] ✅ Success: {len(data.get('results', []))} places found.")
    except requests.exceptions.HTTPError as http_err:
        print(f"[Foursquare] ❌ HTTP error {response.status_code}: {response.text}")
        return []
    except Exception as e:
        print(f"[Foursquare] ❌ Unexpected error: {str(e)}")
        return []

    results = []
    for place in data.get("results", []):
        name = place.get("name")
        location = place.get("location", {})
        latlon = place.get("geocodes", {}).get("main", {})
        photo_url = get_photo(place.get("fsq_id"))

        results.append({
            "name": name,
            "address": location.get("formatted_address"),
            "lat": latlon.get("latitude"),
            "lon": latlon.get("longitude"),
            "thumbnail": photo_url,
            "type": category,
        })

    return results

def get_photo(place_id):
    url = f"https://api.foursquare.com/v3/places/{place_id}/photos"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if data:
            photo = data[0]
            return f"{photo['prefix']}original{photo['suffix']}"
    except Exception as e:
        print(f"[Foursquare] ⚠️ Photo fetch failed for {place_id}: {str(e)}")
    return None