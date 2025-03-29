# app/api/places.py

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
    radius: int = Query(3000)
):
    print("🚦 API hit: /galleries")
    print(f"📍 Params received — lat: {lat}, lon: {lon}, location: {location}")

    if location:
        lat, lon = geocode_location(location)
        print(f"🧭 Geocoded location '{location}' → ({lat}, {lon})")

    if not (lat and lon):
        print("❌ No coordinates available after geocoding")
        return {"error": "Provide coordinates or a location name."}

    results = search_places(lat, lon, category="galleries", radius=radius)
    print(f"🎯 Found {len(results)} galleries near ({lat}, {lon})")
    return {"galleries": results}