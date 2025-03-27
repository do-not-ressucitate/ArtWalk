import logging
import sys
from typing import List
from fastapi import FastAPI, Query, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from geopy.distance import geodesic
from itertools import permutations
from pydantic import BaseModel
import uvicorn

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Rate limiting via slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# FastAPI app instance
app = FastAPI()
app.state.limiter = limiter

# Rate limit error handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return PlainTextResponse(str(exc), status_code=429)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Customize for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base route
@app.get("/")
async def root():
    logger.info("✅ Root pinged")
    return {"message": "Hello from ArtWalk backend!"}

# ------------------------------
# ✅ REGISTER YOUR API ROUTERS
# ------------------------------
from app.api import places, michelin, exhibitions

app.include_router(places.router)
app.include_router(michelin.router)
app.include_router(exhibitions.router)

# ------------------------------
# ✅ ITINERARY OPTIMIZATION LOGIC
# ------------------------------

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
    Generate an optimized itinerary from user's location through selected galleries.
    """
    stops_data = [stop.model_dump() for stop in stops]
    all_points = [{"name": "User Start", "lat": user_lat, "lon": user_lon}] + stops_data

    def total_distance(route):
        return sum(
            geodesic(
                (route[i]["lat"], route[i]["lon"]),
                (route[i + 1]["lat"], route[i + 1]["lon"])
            ).meters
            for i in range(len(route) - 1)
        )

    possible_routes = permutations(stops_data)
    optimal_route = min(
        possible_routes,
        key=lambda route: total_distance([all_points[0]] + list(route))
    )

    optimal_route = [all_points[0]] + list(optimal_route)
    return {"route": optimal_route}

# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080)