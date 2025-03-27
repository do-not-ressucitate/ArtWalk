import requests

resp = requests.get("https://artwalk-backend.fly.dev/michelin?lat=48.8566&lon=2.3522&radius=3000")
print(resp.status_code, resp.json())