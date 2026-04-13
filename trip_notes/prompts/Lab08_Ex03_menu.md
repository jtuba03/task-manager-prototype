I have a Trip Notes CLI app. Read src/main.py and src/ai_assistant.py first.

src/main.py already has:
- A grouped menu: [1]–[4] under "-- Data --", an empty "-- AI --" section, and [Q] Quit
- Exit handled by: if choice.lower() == "q": break

src/ai_assistant.py has: ask() and TRAVEL_SYSTEM_PROMPT.

Add ONE option to the "-- AI --" section of src/main.py:

---

Add to imports at the top:
  from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT

Add "[6] Ask AI a travel question" to the -- AI -- section of the menu display.

Handler for choice "6":
  a. Input: "Your question: "
  b. Call ask(question, system_prompt=TRAVEL_SYSTEM_PROMPT)
  c. If result is None: print an error message and continue
  d. Print the AI response
  e. Ask: "Save this as a note on a trip? (y/n): "
  f. If "y":
     - Print all saved trips numbered (use collection.get_all())
     - If no trips: print "No trips saved yet." and skip saving
     - Input: "Trip number: " (int, subtract 1 for index)
     - Get the trip with collection.get_by_index(index)
     - Call trip.add_note(response)
     - Call save_trips(collection)
     - Print: "Saved as a note on [trip name]."

---

Write the updated file directly to src/main.py.
