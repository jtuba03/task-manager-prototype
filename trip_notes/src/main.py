import sys
import os

# Fix the import path so it works when run from the trip_notes/ root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Destination, TripCollection
from src.storage import load_trips, save_trips

def main():
    collection = load_trips()

    while True:
        print("\n=== Trip Notes ===")
        print("[1] Add destination")
        print("[2] View all destinations")
        print("[3] Search by country")
        print("[4] Add note to a destination")
        print("[5] Quit")

        choice = input("Select an option: ")

        if choice == "1":
            name = input("Enter destination name: ")
            country = input("Enter country: ")
            try:
                budget = float(input("Enter budget: "))
                trip = Destination(name=name, country=country, budget=budget)
                collection.add(trip)
                save_trips(collection)
                print("Destination added!")
            except ValueError:
                print("Invalid budget. Please enter a number.")

        elif choice == "2":
            if len(collection) == 0:
                print("No trips saved yet.")
            else:
                for i, trip in enumerate(collection.get_all(), 1):
                    print(f"{i}. {trip.name} ({trip.country}) - Budget: ${trip.budget:.2f}")
                    if trip.notes:
                        print(f"   Notes: {', '.join(trip.notes)}")

        elif choice == "3":
            country = input("Enter country to search: ")
            results = collection.search_by_country(country)
            if not results:
                print(f"No trips found in {country}.")
            else:
                for trip in results:
                    print(f"- {trip.name} - Budget: ${trip.budget:.2f}")

        elif choice == "4":
            if len(collection) == 0:
                print("No trips to add notes to.")
                continue
            
            for i, trip in enumerate(collection.get_all(), 1):
                print(f"{i}. {trip.name}")
            
            try:
                idx = int(input("Select trip number to add note: "))
                trip = collection.get_by_index(idx - 1)
                note = input("Enter note: ")
                trip.add_note(note)
                save_trips(collection)
                print("Note added!")
            except (ValueError, IndexError):
                print("Invalid selection.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
