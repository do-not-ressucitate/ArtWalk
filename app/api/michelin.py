from fastapi import APIRouter, Query
from app.services.michelin_service import find_michelin_restaurants_near

router = APIRouter()

@router.get("/michelin")
def get_michelin_restaurants(
    lat: float = Query(..., description="User latitude"),
    lon: float = Query(..., description="User longitude"),
    radius: int = Query(900, description="Search radius in meters")
):
    """
    Returns a list of nearby Michelin restaurants within a given radius.
    """
    return find_michelin_restaurants_near(lat, lon, radius_m=radius)