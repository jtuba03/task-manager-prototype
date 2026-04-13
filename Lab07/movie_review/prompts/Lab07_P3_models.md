# Role
Act as a Python software engineer.

# Task
Create the file `src/models.py`. This file must contain a Data Class for the individual items and a Collection Class to manage them.

# Requirements
1. **Movie Data Class**: Define a class (using `@dataclass` or a standard `__init__`) with:
   - `title` (str)
   - `watched` (bool)
   - `rating` (int or float)

2. **Watchlist Collection Class**: 
   - Attributes: A list to store Movie objects.
   - Method `unwatched()`: Returns a list of all movies where `watched` is False.
   - Method `top_rated()`: Returns a list of all movies sorted by `rating` in descending order.
   - Method `random_pick()`: Returns one randomly selected Movie object from the list.

# Constraints
- Use clean, PEP 8 compliant code.
- Ensure the sorting logic in `top_rated` does not mutate the original list order permanently.
- Include type hints for all method signatures.
