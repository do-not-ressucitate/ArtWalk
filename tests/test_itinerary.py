import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_itinerary():
    payload = {
        "user_lat": 48.8566,
        "user_lon": 2.3522,
        "available_time_hours": 6,
        "theme": "compact",
        "stops": [
            {"name": "Gallery A", "lat": 48.8570, "lon": 2.3525},
            {"name": "Gallery B", "lat": 48.8575, "lon": 2.3530}
        ]
    }

    response = client.post("/itinerary", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "route" in data
    assert len(data["route"]) >= 3  # includes user start