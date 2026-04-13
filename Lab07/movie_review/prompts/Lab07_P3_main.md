# Role
Act as a Python developer.

# Task
Create the file `src/main.py`. This is the entry point for a Movie Reviewer app.

# Context
You must first read and understand the `Watchlist` and `Movie` classes defined in `src/models.py`. This file will also interact with a `storage.py` module (assume it has `load_data` and `save_data` functions) to persist the list to a JSON file in the `data/` folder.

# Requirements
1. **Imports**: Import the necessary classes from `models.py` and functions from `storage.py`.
2. **Menu Loop**: Implement a `while True` loop that displays the following menu:
   - [1] unwatched
   - [2] top rated
   - [3] random pick
   - [4] Quit
3. **User Interaction**:
   - Handle user input for options 1-4.
   - For [1], [2], and [3], call the appropriate method from the `Watchlist` instance and print the results in a clean, readable format.
   - For [4], save the data via the storage module and exit the program.

# Constraints
- Validate that the user input is a valid integer between 1 and 4.
- Use an f-string to format the output of the movie lists clearly.