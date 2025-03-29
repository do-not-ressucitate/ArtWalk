import requests

def geocode_location(location: str):
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": location, "format": "json", "limit": 1},
        headers={"User-Agent": "ArtWalkApp/1.0 (pantalon@gmail.com)"}
    )

def geocode_location(location_name: str):
    print(f"🛰️  Geocoding '{location_name}'...")
    # existing geocode logic...
    if lat and lon:
        print(f"📌 Geocoded '{location_name}' to lat={lat}, lon={lon}")
    else:
        print(f"❌ Failed to geocode '{location_name}'")
    return lat, lon

    data = response.json()  # This should now work
    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    return None, None
