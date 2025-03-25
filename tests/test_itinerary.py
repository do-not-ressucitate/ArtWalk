import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_itinerary():
    # Set up a dummy user location (e.g., Paris) and two stops.
    user_lat = 48.8566
    user_lon = 2.3522
    stops = [
        {"name": "Gallery A", "lat": 48.8570, "lon": 2.3525},
        {"name": "Gallery B", "lat": 48.8575, "lon": 2.3530}
    ]
    
    response = client.post(
        f"/itinerary?user_lat={user_lat}&user_lon={user_lon}",
        json=stops
    )
    
    assert response.status_code == 200, response.text
    data = response.json()
    assert "route" in data
    # Check that the returned route is a list and includes the user start point.
    assert isinstance(data["route"], list)
    assert data["route"][0]["name"] == "User Start"