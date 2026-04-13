I have a Trip Notes CLI app. Read src/main.py and src/ai_assistant.py first.

src/main.py has a working menu with options [1]–[6].
src/ai_assistant.py has generate_trip_briefing(city, country, notes=None).

Update src/main.py to add option [7] Trip Briefing:

1. Add generate_trip_briefing to the import from src.ai_assistant.

2. Add "[7] Trip Briefing" to the menu display.

3. Add a handler for choice "7":
   a. Get all trips: destinations = collection.get_all()
   b. If empty, print "No trips saved yet." and return to menu
   c. Print numbered list:
      for i, dest in enumerate(destinations, 1):
          print(f"  [{i}] {dest.name}, {dest.country}")
   d. Input: "Select trip number: " (convert to int, subtract 1 for index)
   e. If the number is out of range, print "Invalid selection." and return to menu
   f. Get selected trip: dest = destinations[index]
   g. Print: f"Generating briefing for {dest.name}..."
   h. Call: result = generate_trip_briefing(dest.name, dest.country, dest.notes)
   i. If result is None: print "Briefing failed. Check your API connection." and return
   j. Print:
      print(f"\n--- {dest.name} Briefing ---")
      print(f"Overview:\n{result['overview']}")
      print(f"\nPacking List:\n{result['packing_list']}")

Write the updated file directly to src/main.py.
