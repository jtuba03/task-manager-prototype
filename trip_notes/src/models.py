from dataclasses import dataclass, field
from datetime import date

@dataclass
class Destination:
    name: str
    country: str
    budget: float
    notes: list[str] = field(default_factory=list)
    date_added: str = field(default_factory=lambda: date.today().isoformat())
    visited: bool = False

    def add_note(self, note: str) -> None:
        """Appends note to self.notes."""
        self.notes.append(note)

class TripCollection:
    def __init__(self):
        self._trips: list[Destination] = []

    def add(self, destination: Destination) -> None:
        """Adds a destination object to the collection."""
        self._trips.append(destination)

    def get_all(self) -> list[Destination]:
        """Returns a list of all destinations."""
        return self._trips

    def search_by_country(self, country: str) -> list[Destination]:
        """Returns a list of destinations matching the country (case-insensitive)."""
        return [t for t in self._trips if t.country.lower() == country.lower()]

    def get_by_index(self, index: int) -> Destination:
        """Returns a destination object by its index."""
        return self._trips[index]

    def get_wishlist(self) -> list[Destination]:
        """Returns a list of destinations where visited is False."""
        return [t for t in self._trips if not t.visited]

    def get_visited(self) -> list[Destination]:
        """Returns a list of destinations where visited is True."""
        return [t for t in self._trips if t.visited]

    def mark_visited(self, index: int) -> None:
        """Sets the destination at the given index to visited=True."""
        self._trips[index].visited = True

    def total_budget(self) -> float:
        """Returns sum of budget for all trips. Returns 0.0 if empty."""
        return sum(t.budget for t in self._trips) if self._trips else 0.0

    def average_budget(self) -> float:
        """Returns average budget. Returns 0.0 if empty."""
        return self.total_budget() / len(self._trips) if self._trips else 0.0

    def top_country(self) -> str:
        """Returns the country name that appears most often in the collection.
        Returns 'No trips yet' if empty."""
        if not self._trips:
            return "No trips yet"
        counts = self.count_by_country()
        return max(counts, key=counts.get)

    def count_by_country(self) -> dict[str, int]:
        """Returns a dict mapping country name -> number of trips to that country."""
        counts = {}
        for t in self._trips:
            counts[t.country] = counts.get(t.country, 0) + 1
        return counts

    def __len__(self) -> int:
        """Returns the number of destinations in the collection."""
        return len(self._trips)
