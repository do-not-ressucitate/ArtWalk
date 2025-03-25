# app/main.py
import logging
import sys
from typing import Optional, List, Dict  # Added missing imports
from fastapi import FastAPI, Query, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from geopy.distance import geodesic
from itertools import permutations
import uvicorn
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Optionally, integrate Sentry (ensure you have sentry-sdk installed)
# pip install sentry-sdk
# import sentry_sdk
# from sentry_sdk.integrations.fastapi import FastApiIntegration
# sentry_sdk.init(
#     dsn="YOUR_SENTRY_DSN",
#     integrations=[FastApiIntegration()],
#     traces_sample_rate=1.0,
# )

# Import rate limiting middleware using slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import PlainTextResponse

limiter = Limiter(key_func=get_remote_address)

# Import functions from services and utilities
from app.utils.geocode import geocode_location
from app.services.foursquare_service import search_places, get_photo
from app.services.michelin_service import find_michelin_restaurants_near
from app.services.galleriesnow_service import load_special_exhibitions

app = FastAPI()
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return PlainTextResponse(str(exc), status_code=429)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your actual frontend domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Hello from ArtWalk backend!"}

@app.get("/michelin")
async def get_michelin_restaurants(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: int = Query(1000)
):
    results = find_michelin_restaurants_near(lat, lon, radius)
    return {"restaurants": results}

@app.get("/places")
async def get_places(
    category: str = Query(..., description="Type of place (galleries, auctions, restaurants)"),
    location: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None)
):
    if location and not (lat and lon):
        lat, lon = geocode_location(location)
    if not (lat and lon):
        return {"error": "Please provide either coordinates or a location name."}
    results = search_places(lat, lon, category)
    return {"results": results}

# Apply rate limiting to protect this endpoint (5 requests per minute per IP)
@app.get("/exhibitions")
@limiter.limit("5/minute")
async def get_exhibitions(
    request: Request,  # Added parameter for rate limiting
    location: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    radius: int = Query(1000)
):
    if location and not (lat and lon):
        lat, lon = geocode_location(location)
    if not (lat and lon):
        return {"error": "Please provide either coordinates or a location name."}
    
    # Step 1: Get open-now galleries via Foursquare
    places_data = search_places(lat, lon, category="galleries", radius=radius)
    
    # Step 2: Load special exhibitions (from CSV at data/exhibitions_today.csv)
    specials = load_special_exhibitions()
    
    # Step 3: Enhance data with distance and special exhibition info
    enhanced = []
    for p in places_data:
        name_key = p["name"].lower().strip()
        special = specials.get(name_key)
        distance = geodesic((lat, lon), (p["lat"], p["lon"])).meters
        p.update({
            "distance": round(distance),
            "special": special["label"] if special else None,
            "exhibition": special["title"] if special else None,
            "special_thumbnail": special["thumbnail"] if special else None
        })
        enhanced.append(p)
    
    # Step 4: Sort by distance
    enhanced.sort(key=lambda x: x["distance"])
    return {"exhibitions": enhanced}

# Define a Pydantic model for itinerary stops
class Stop(BaseModel):
    name: str
    lat: float
    lon: float

@app.post("/itinerary")
async def generate_itinerary(
    user_lat: float = Query(..., description="User's current latitude"),
    user_lon: float = Query(..., description="User's current longitude"),
    stops: List[Stop] = Body(..., description="List of selected galleries with their names and coordinates")
):
    """
    Generate an optimized itinerary based on the user's location and selected galleries.
    """
    # Convert stops to dictionaries using model_dump() (Pydantic V2 recommended)
    stops_data = [stop.model_dump() for stop in stops]
    # Combine user's starting point with the stops
    all_points = [{"name": "User Start", "lat": user_lat, "lon": user_lon}] + stops_data

    def total_distance(route):
        return sum(
            geodesic(
                (route[i]["lat"], route[i]["lon"]),
                (route[i + 1]["lat"], route[i + 1]["lon"])
            ).meters
            for i in range(len(route) - 1)
        )

    # Generate all possible itineraries (permutations)
    possible_routes = permutations(stops_data)
    
    # Find the route with the shortest total distance
    optimal_route = min(
        possible_routes,
        key=lambda route: total_distance([all_points[0]] + list(route))
    )

    # Prepend the user's start point to the route
    optimal_route = [all_points[0]] + list(optimal_route)
    return {"route": optimal_route}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080)