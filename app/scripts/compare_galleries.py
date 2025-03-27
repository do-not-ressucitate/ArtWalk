import os
import csv
import sys

# ───────────────────────────────
# File paths
# ───────────────────────────────

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

galleriesnow_path = os.path.join(base_dir, 'exhibitions_today.csv')
foursquare_path = os.path.join(base_dir, 'foursquare_galleries.csv')
output_path = os.path.join(base_dir, 'combined_galleries.csv')

# ───────────────────────────────
# Load CSVs
# ───────────────────────────────

def load_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        return list(csv.DictReader(file))

galleriesnow_data = load_csv(galleriesnow_path)
foursquare_data = load_csv(foursquare_path)

# ───────────────────────────────
# Normalize names and match
# ───────────────────────────────

# Extract and normalize gallery names from exhibitions_today.csv
special_names = set()
for row in galleriesnow_data:
    name = row.get("gallery", "").strip().lower()
    if name:
        special_names.add(name)

# Compare with Foursquare galleries
combined = []
for gallery in foursquare_data:
    fsq_name = gallery.get("name", "").strip().lower()
    is_special = fsq_name in special_names
    gallery["special_interest"] = str(is_special)
    combined.append(gallery)

# ───────────────────────────────
# Save combined results
# ───────────────────────────────

with open(output_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "name", "address", "lat", "lon", "thumbnail", "type", "special_interest"
    ])
    writer.writeheader()
    writer.writerows(combined)

print(f"🎯 Done! Saved combined gallery data with tags to: {output_path}")