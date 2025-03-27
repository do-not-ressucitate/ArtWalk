import os
import csv
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services.foursquare_service import search_places
from app.utils.geocode import geocode_location


# ─────────────────────────────────────────────────────────────
# Option 1: Use lat/lon directly (e.g., user is geolocated)
# Option 2: Use place name (e.g., "SoHo NYC") from input
# ─────────────────────────────────────────────────────────────

def get_lat_lon_from_input():
    if len(sys.argv) == 3:
        # CLI: user provided lat and lon
        return float(sys.argv[1]), float(sys.argv[2])
    elif len(sys.argv) == 2:
        # CLI: user provided a place name
        location_name = sys.argv[1]
        print(f"🌍 Geocoding: {location_name}")
        lat, lon = geocode_location(location_name)
        if lat and lon:
            return lat, lon
        else:
            raise ValueError("❌ Could not geocode location.")
    else:
        raise ValueError("❌ Please provide a location name OR lat lon.\nUsage:\n  python save_foursquare_galleries.py 'Paris' OR\n  python save_foursquare_galleries.py 48.85 2.35")

# ─────────────────────────────────────────────────────────────

# Input handler
lat, lon = get_lat_lon_from_input()
CATEGORY = "galleries"

print(f"📡 Fetching open galleries near ({lat}, {lon}) from Foursquare...")
galleries = search_places(lat=lat, lon=lon, category=CATEGORY)

# Ensure data directory exists
data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
os.makedirs(data_dir, exist_ok=True)

# Save to CSV
csv_path = os.path.join(data_dir, 'foursquare_galleries.csv')
with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "address", "lat", "lon", "thumbnail", "type"])
    writer.writeheader()
    writer.writerows(galleries)

print(f"✅ Saved {len(galleries)} galleries to {csv_path}")