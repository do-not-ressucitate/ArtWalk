import requests

def geocode_location(location: str):
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": location, "format": "json", "limit": 1},
        headers={"User-Agent": "ArtWalkApp/1.0 (pantalon@gmail.com)"}
    )

    data = response.json()  # This should now work
    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    return None, None
