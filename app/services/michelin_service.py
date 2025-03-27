import pandas as pd
from geopy.distance import geodesic
import os

# Load and clean Michelin data at module load time
csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'michelin_my_maps.csv')
df = pd.read_csv(csv_path)
df = df.dropna(subset=["Latitude", "Longitude", "Name", "Location"])

def find_michelin_restaurants_near(lat: float, lon: float, radius_m: int = 1000) -> list:
    """
    Return Michelin restaurants within a given radius (in meters) of a location.
    """

    def is_within_radius(row):
        user_location = (lat, lon)
        restaurant_location = (row["Latitude"], row["Longitude"])
        distance = geodesic(user_location, restaurant_location).meters
        return distance <= radius_m

    filtered = df[df.apply(is_within_radius, axis=1)]

    return [
        {
            "name": row["Name"],
            "address": row["Address"],
            "location": row["Location"],
            "lat": row["Latitude"],
            "lon": row["Longitude"],
            "award": row["Award"],
            "green_star": bool(row["GreenStar"]),
            "cuisine": row["Cuisine"],
            "url": row["Url"],
        }
        for _, row in filtered.iterrows()
    ]