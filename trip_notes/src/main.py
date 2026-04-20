import sys
import os

# Fix the import path so it works when run from the trip_notes/ root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Destination, TripCollection
from src.storage import load_trips, save_trips
from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT, generate_trip_briefing, rag_ask
from src.rag import build_index

def main():
    collection = load_trips()

    while True:
        print("\n=== Trip Notes ===")
        print("\n-- Data --")
        print("[1] Add destination")
        print("[2] List all destinations")
        print("[3] Mark as visited")
        print("[4] Show statistics")
        print("\n-- AI --")
        print("[6] Ask AI a travel question")
        print("[7] Trip Briefing")
        print("[8] Search my guides")
        print("\n[R] Rebuild search index")
        print("[Q] Quit")

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
                    status = "Visited" if trip.visited else "Wishlist"
                    print(f"{i}. {trip.name} ({trip.country}) - Budget: ${trip.budget:.2f} [{status}]")
                    if trip.notes:
                        print(f"   Notes: {', '.join(trip.notes)}")

        elif choice == "3":
            if len(collection) == 0:
                print("No trips to mark.")
                continue
            
            for i, trip in enumerate(collection.get_all(), 1):
                print(f"{i}. {trip.name}")
            
            try:
                idx = int(input("Enter a number: "))
                trip = collection.get_by_index(idx - 1)
                collection.mark_visited(idx - 1)
                save_trips(collection)
                print(f"Marked {trip.name} as visited!")
            except (ValueError, IndexError):
                print("Invalid selection.")

        elif choice == "4":
            if len(collection) == 0:
                print("No trips saved yet.")
            else:
                print("\n=== Trip Statistics ===")
                print(f"Total trips: {len(collection)}")
                print(f"Total budget: ${collection.total_budget():.2f}")
                print(f"Average budget: ${collection.average_budget():.2f}")
                counts = collection.count_by_country()
                top_c = collection.top_country()
                print(f"Top country: {top_c} ({counts.get(top_c, 0)} trips)")
                print("Trips by country:")
                for country, count in counts.items():
                    print(f"  {country}: {count}")

        elif choice == "6":
            question = input("Your question: ")
            response = ask(question, system_prompt=TRAVEL_SYSTEM_PROMPT)
            if response is None:
                print("Error: Could not get a response from the AI.")
                continue
            
            print(f"\nAI Response:\n{response}")
            
            save_note = input("\nSave this as a note on a trip? (y/n): ").lower()
            if save_note == "y":
                if len(collection) == 0:
                    print("No trips saved yet.")
                else:
                    for i, trip in enumerate(collection.get_all(), 1):
                        print(f"{i}. {trip.name}")
                    
                    try:
                        idx = int(input("Trip number: "))
                        trip = collection.get_by_index(idx - 1)
                        trip.add_note(response)
                        save_trips(collection)
                        print(f"Saved as a note on {trip.name}.")
                    except (ValueError, IndexError):
                        print("Invalid selection.")

        elif choice == "7":
            destinations = collection.get_all()
            if not destinations:
                print("No trips saved yet.")
                continue
            
            print("\nSelect a trip for briefing:")
            for i, dest in enumerate(destinations, 1):
                print(f"  [{i}] {dest.name}, {dest.country}")
            
            try:
                idx = int(input("Select trip number: "))
                if not (1 <= idx <= len(destinations)):
                    print("Invalid selection.")
                    continue
                
                dest = destinations[idx - 1]
                print(f"Generating briefing for {dest.name}...")
                result = generate_trip_briefing(dest.name, dest.country, dest.notes)
                
                if result is None:
                    print("Briefing failed. Check your API connection.")
                    continue
                
                print(f"\n--- {dest.name} Briefing ---")
                print(f"Overview:\n{result['overview']}")
                print(f"\nPacking List:\n{result['packing_list']}")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "8":
            question = input("Your question: ")
            response = rag_ask(question)
            if response is None:
                print("Error: Could not get a response from the AI.")
                continue
            print(f"\nAI Response:\n{response}")

        elif choice.lower() == "r":
            print("Rebuilding index from guides/..." )
            build_index(force=True)
            print("Done. Use [8] to search your updated guides.")

        elif choice.lower() == "q":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
