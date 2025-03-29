import requests

def geocode_location(location_name: str):
    print(f"🛰️  Geocoding '{location_name}'...")

    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": location_name, "format": "json", "limit": 1},
        headers={"User-Agent": "ArtWalkApp/1.0 (pantalon@gmail.com)"}
    )

    data = response.json()

    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        print(f"📌 Geocoded '{location_name}' to lat={lat}, lon={lon}")
        return lat, lon
    else:
        print(f"❌ Failed to geocode '{location_name}'")
        return None, None