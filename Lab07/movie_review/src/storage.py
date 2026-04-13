import os
import json
from dataclasses import asdict
from .models import Movie, Watchlist

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "movies.json")

def load_data() -> Watchlist:
    """Loads Watchlist from JSON file. Returns empty if file missing."""
    watchlist = Watchlist()
    if not os.path.exists(DATA_PATH):
        return watchlist
    
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
            for d in data:
                watchlist.add(Movie(**d))
    except (json.JSONDecodeError, TypeError):
        # Return empty watchlist if file is corrupted
        return watchlist
    return watchlist

def save_data(watchlist: Watchlist) -> None:
    """Saves Watchlist to a JSON file, creating the directory if it does not exist."""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    # Assuming Watchlist has a way to get all movies or we use internal _movies for simplicity
    # Since I added _movies in the previous step, I'll access it. 
    # Better yet, I should add a get_all() to Watchlist in models.py if I were to follow best practices, 
    # but I will use the internal list for now to match the provided structure.
    list_of_dicts = [asdict(m) for m in watchlist._movies]
    with open(DATA_PATH, "w") as f:
        json.dump(list_of_dicts, f, indent=2)
