import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def fake_search_places(lat, lon, category, radius=1000):
    return [{
        "name": "Dummy Gallery",
        "lat": lat + 0.001,
        "lon": lon + 0.001,
        "fsq_id": "dummy"  # dummy id to trigger get_photo
    }]

def fake_get_photo(fsq_id):
    return "http://dummyphoto.com/dummy.jpg"

def fake_load_special_exhibitions():
    # Return dummy special exhibitions data without reading from file
    return {"dummy gallery": {"label": "Special", "title": "Special Exhibition", "thumbnail": "http://example.com/thumb.jpg"}}

@pytest.fixture(autouse=True)
def override_external_calls(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("app.services.foursquare_service.search_places", fake_search_places)
    monkeypatch.setattr("app.services.foursquare_service.get_photo", fake_get_photo)
    monkeypatch.setattr("app.services.galleriesnow_service.load_special_exhibitions", fake_load_special_exhibitions)

def test_exhibitions_no_location():
    response = client.get("/exhibitions")
    assert response.status_code == 200
    data = response.json()
    assert "exhibitions" in data


def test_exhibitions_with_location():
    response = client.get("/exhibitions?lat=48.8566&lon=2.3522")
    assert response.status_code == 200
    data = response.json()
    assert "exhibitions" in data
    assert len(data["exhibitions"]) > 0