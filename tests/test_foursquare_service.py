import pytest
from app.services.foursquare_service import search_places

@pytest.mark.skipif(
    True, reason="Only run manually to test Foursquare live data"
)
def test_search_places_sf_returns_results():
    # Coordinates for San Francisco
    lat = 37.7749
    lon = -122.4194
    category = "galleries"

    results = search_places(lat, lon, category)

    assert isinstance(results, list), "Expected result to be a list"
    if results:
        print(f"✅ {len(results)} galleries found.")
        assert "name" in results[0], "Missing 'name' in gallery result"
        assert "address" in results[0], "Missing 'address' in gallery result"
    else:
        print("⚠️ No galleries returned — check API key, filters, or time of day.")