import pandas as pd
from geopy.distance import geodesic

# Load the Michelin dataset
df = pd.read_csv("data/michelin_my_maps.csv")

# Drop rows missing key data
df = df.dropna(subset=["Latitude", "Longitude", "Name", "Location"])

def find_michelin_restaurants_near(lat: float, lon: float, radius_m: int = 1000) -> list:
    """Find Michelin restaurants within a given radius (in meters) of a location."""

    def is_within_radius(row):
        distance = geodesic((lat, lon), (row["Latitude"], row["Longitude"])).meters
        return distance <= radius_m

    nearby = df[df.apply(is_within_radius, axis=1)]

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
        for _, row in nearby.iterrows()
    ]
