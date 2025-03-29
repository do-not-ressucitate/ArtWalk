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
    """
    Return open-now art galleries near the user using Foursquare.
    Supports either GPS coordinates or a location name.
    """
    # Always prefer geocoding if a location string is provided
    if location:
        lat, lon = geocode_location(location)

    if not (lat and lon):
        return {"error": "Provide coordinates or a location name."}

    results = search_places(lat, lon, category="galleries", radius=radius)
    return {"galleries": results}