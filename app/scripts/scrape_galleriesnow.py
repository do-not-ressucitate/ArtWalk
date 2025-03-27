import requests
from bs4 import BeautifulSoup
import csv
import os

# URL to scrape
url = "https://www.galleriesnow.net/whats-on-today/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Send request and parse HTML
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

results = []

# Extract events by city
for section in soup.select('div.buffer-default'):
    city_tag = section.find('h2')
    city = city_tag.text.strip() if city_tag else "Unknown"

    events = section.select('li.event-item')
    for event in events:
        paragraphs = event.select('.event-information p')

        label = paragraphs[0].text.strip() if len(paragraphs) > 0 else "No label"
        title = paragraphs[1].text.strip() if len(paragraphs) > 1 else "No title"

        # Extract gallery name and address
        gallery_and_address = paragraphs[3].text.strip() if len(paragraphs) > 3 else "No gallery info"
        if "," in gallery_and_address:
            parts = gallery_and_address.split(",", 1)
            gallery_name = parts[0].strip()
            address = parts[1].strip()
        else:
            gallery_name = gallery_and_address
            address = "No address"

        # Extract image
        thumbnail = event.select_one('.display-event-image img')
        thumbnail_url = thumbnail['src'] if thumbnail and 'src' in thumbnail.attrs else "No thumbnail"

        results.append({
            "city": city,
            "label": label,
            "title": title,
            "gallery": gallery_name,
            "address": address,
            "thumbnail": thumbnail_url
        })

# ✅ Ensure the data/ directory exists
data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
os.makedirs(data_dir, exist_ok=True)

# ✅ Save to exhibitions_today.csv
csv_path = os.path.join(data_dir, 'exhibitions_today.csv')
with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["city", "label", "title", "gallery", "address", "thumbnail"])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Saved {len(results)} exhibitions to {csv_path}")