import csv
import os

def load_special_exhibitions():
    # Navigate from app/services/ to the project root:
    # os.path.dirname(__file__) -> artwalk-backend/app/services
    # os.path.dirname(os.path.dirname(__file__)) -> artwalk-backend/app
    # os.path.dirname(os.path.dirname(os.path.dirname(__file__))) -> artwalk-backend
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(base_dir, 'data', 'exhibitions_today.csv')
    specials = {}

    with open(path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["gallery"].lower().strip()
            specials[name] = {
                "label": row["label"],
                "title": row["title"],
                "thumbnail": row["thumbnail"]
            }

    return specials