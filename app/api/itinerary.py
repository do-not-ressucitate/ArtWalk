# Path: artwalk-backend/app/api/itinerary.py

from fastapi import APIRouter, Body
from typing import List
from geopy.distance import geodesic
from pydantic import BaseModel
from itertools import permutations
import random

router = APIRouter()

class Stop(BaseModel):
    name: str
    lat: float
    lon: float
    address: str = "Unknown"

class ItineraryRequest(BaseModel):
    user_lat: float
    user_lon: float
    available_time_hours: float
    theme: str  # e.g., "compact" or "cultural"
    stops: List[Stop]

@router.post("/itinerary")
def generate_itinerary(req: ItineraryRequest):
    print("🧭 Generating itinerary...")
    walking_speed_kmh = 3
    visit_time_min = 20

    all_routes = []
    user_start = Stop(name="Start", lat=req.user_lat, lon=req.user_lon)
    max_time_minutes = req.available_time_hours * 60

    for perm in permutations(req.stops):
        route = [user_start] + list(perm)
        total_distance_km = sum(
            geodesic((route[i].lat, route[i].lon), (route[i + 1].lat, route[i + 1].lon)).km
            for i in range(len(route) - 1)
        )
        walk_time_min = (total_distance_km / walking_speed_kmh) * 60
        visit_time_total = len(req.stops) * visit_time_min
        total_duration = walk_time_min + visit_time_total

        if total_duration <= max_time_minutes:
            all_routes.append({
                "route": [stop.model_dump() for stop in route],
                "distance_km": total_distance_km,
                "duration_min": total_duration
            })

    if not all_routes:
        sorted_stops = sorted(
            req.stops,
            key=lambda stop: geodesic((req.user_lat, req.user_lon), (stop.lat, stop.lon)).km
        )
        for i in range(len(sorted_stops), 1, -1):
            reduced_stops = sorted_stops[:i]
            trimmed_req = ItineraryRequest(
                user_lat=req.user_lat,
                user_lon=req.user_lon,
                available_time_hours=req.available_time_hours,
                theme=req.theme,
                stops=reduced_stops
            )
            result = generate_itinerary(trimmed_req)
            if result and "route" in result:
                return result

        return {"error": "⏳ Not enough time to visit even two galleries."}

    if req.theme == "compact":
        best_routes = sorted(all_routes, key=lambda r: r["duration_min"])
    elif req.theme == "cultural":
        best_routes = random.sample(all_routes, min(3, len(all_routes)))
    else:
        best_routes = all_routes

    return {
        "route": best_routes[0]["route"],
        "duration_min": round(best_routes[0]["duration_min"], 1),
        "distance_km": round(best_routes[0]["distance_km"], 2),
        "alternatives": [r["route"] for r in best_routes[1:3]]
    }
