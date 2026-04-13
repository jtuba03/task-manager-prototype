import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class Movie:
    """Movie data class for individual movies."""
    title: str
    watched: bool
    rating: float

class Watchlist:
    """Watchlist collection class to manage a list of Movie objects."""
    def __init__(self):
        self._movies: list[Movie] = []

    def add(self, movie: Movie) -> None:
        """Adds a Movie object to the watchlist."""
        self._movies.append(movie)

    def unwatched(self) -> list[Movie]:
        """Returns a list of all movies where watched is False."""
        return [m for m in self._movies if not m.watched]

    def top_rated(self) -> list[Movie]:
        """Returns a list of all movies sorted by rating in descending order (non-mutating)."""
        return sorted(self._movies, key=lambda m: m.rating, reverse=True)

    def random_pick(self) -> Optional[Movie]:
        """Returns one randomly selected Movie object, or None if the list is empty."""
        if not self._movies:
            return None
        return random.choice(self._movies)

    def __len__(self) -> int:
        """Returns the number of movies in the watchlist."""
        return len(self._movies)
