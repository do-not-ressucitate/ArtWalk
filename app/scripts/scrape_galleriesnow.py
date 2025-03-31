import requests
from bs4 import BeautifulSoup
import csv
import os
import logging
from datetime import datetime

# Setup logging
log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'scraper.log')
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_scraper():
    url = "https://www.galleriesnow.net/whats-on-today/"
    headers = { "User-Agent": "Mozilla/5.0" }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        logging.error(f"❌ Failed to fetch or parse GalleriesNow page: {e}")
        return

    results = []

    for section in soup.select('div.buffer-default'):
        city_tag = section.find('h2')
        city = city_tag.text.strip() if city_tag else "Unknown"

        events = section.select('li.event-item')
        for event in events:
            paragraphs = event.select('.event-information p')
            label = paragraphs[0].text.strip() if len(paragraphs) > 0 else "No label"
            title = paragraphs[1].text.strip() if len(paragraphs) > 1 else "No title"

            gallery_and_address = paragraphs[3].text.strip() if len(paragraphs) > 3 else "No gallery info"
            if "," in gallery_and_address:
                parts = gallery_and_address.split(",", 1)
                gallery_name = parts[0].strip()
                address = parts[1].strip()
            else:
                gallery_name = gallery_and_address
                address = "No address"

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

    try:
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        os.makedirs(data_dir, exist_ok=True)

        csv_path = os.path.join(data_dir, 'exhibitions_today.csv')
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(...)
            writer.writeheader()
            writer.writerows(results)

        logging.info(f"✅ Successfully saved {len(results)} exhibitions to exhibitions_today.csv")
        print(f"✅ Saved {len(results)} exhibitions to {csv_path}")
    except Exception as e:
        logging.error(f"❌ Failed to save exhibitions CSV: {e}")
        print(f"❌ CSV write failed: {e}")

if __name__ == "__main__":
    run_scraper()