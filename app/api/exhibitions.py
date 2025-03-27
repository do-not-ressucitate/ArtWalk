from fastapi import APIRouter
import os
import csv

router = APIRouter()

@router.get("/exhibitions")
def get_curated_exhibitions():
    """
    Return special-interest galleries curated from GalleriesNow.
    Reads from exhibitions_today.csv.
    """
    data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'exhibitions_today.csv')
    exhibitions = []

    if os.path.exists(data_path):
        with open(data_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                exhibitions.append({
                    "name": row["gallery"],
                    "address": row["address"],
                    "city": row["city"],
                    "label": row["label"],
                    "title": row["title"],
                    "thumbnail": row["thumbnail"],
                })

    return {"exhibitions": exhibitions}