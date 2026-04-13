import sys
import os

# Fix the import path so it works when run from the movie_review/ root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Movie, Watchlist
from src.storage import load_data, save_data

def display_movies(movies: list[Movie], title: str):
    print(f"
--- {title} ---")
    if not movies:
        print("No movies found.")
        return
    for movie in movies:
        status = "Watched" if movie.watched else "Unwatched"
        print(f"🎬 {movie.title} | Rating: {movie.rating}/10 | {status}")

def main():
    watchlist = load_data()

    while True:
        print("
=== Movie Reviewer ===")
        print("[1] unwatched")
        print("[2] top rated")
        print("[3] random pick")
        print("[4] Quit")

        choice = input("Select an option (1-4): ")

        if choice == "1":
            unwatched_movies = watchlist.unwatched()
            display_movies(unwatched_movies, "Unwatched Movies")

        elif choice == "2":
            top_movies = watchlist.top_rated()
            display_movies(top_movies, "Top Rated Movies")

        elif choice == "3":
            movie = watchlist.random_pick()
            if movie:
                print("
--- Random Pick ---")
                status = "Watched" if movie.watched else "Unwatched"
                print(f"🎲 {movie.title} | Rating: {movie.rating}/10 | {status}")
            else:
                print("
No movies in your watchlist yet.")

        elif choice == "4":
            save_data(watchlist)
            print("Watchlist saved. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid input. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
