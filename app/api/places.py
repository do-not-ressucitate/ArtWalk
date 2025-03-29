from fastapi import APIRouter, Query
from typing import Optional
from app.services.foursquare_service import search_places
from app.utils.geocode import geocode_location

router = APIRouter()

@router.get("/galleries")
def get_live_galleries(
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    location: Optional[str] = Query(None),
    radius: int = Query(1000)
):
    print("📍 /galleries endpoint hit")
    print(f"🔍 Incoming query: lat={lat}, lon={lon}, location={location}, radius={radius}")

    if location:
        lat, lon = geocode_location(location)
        print(f"📌 Geocoded '{location}' → lat={lat}, lon={lon}")

    if not (lat and lon):
        print("❌ Missing location data.")
        return {"error": "Provide coordinates or a location name."}

    results = search_places(lat, lon, category="galleries", radius=radius)
    print(f"✅ Fetched {len(results)} galleries from Foursquare")
    return {"galleries": results}