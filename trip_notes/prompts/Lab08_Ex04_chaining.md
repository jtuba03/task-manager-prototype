I have a Trip Notes CLI app. Read src/ai_assistant.py first.
It has ask() and TRAVEL_SYSTEM_PROMPT already defined.

Add a new function to src/ai_assistant.py:

generate_trip_briefing(city: str, country: str, notes: list = None) -> dict

This function makes two sequential API calls (prompt chaining):

Call 1 — Overview:
  Build the prompt:
    base = f"Give a 3-sentence travel overview of {city}, {country}. Cover: what it's like to visit, best season to go, and one must-see attraction."
    If notes is not None and len(notes) > 0:
        notes_text = "\n".join(f"- {n}" for n in notes)
        prompt = base + f"\n\nPersonal notes about this trip:\n{notes_text}"
    Else:
        prompt = base
  Use: system_prompt=TRAVEL_SYSTEM_PROMPT

Call 2 — Packing list (uses Call 1 output as context):
  prompt: f"Based on this destination overview:\n{overview}\n\nWrite a 5-item packing list specific to {city}."
  Use: system_prompt=TRAVEL_SYSTEM_PROMPT

Return: {"overview": overview, "packing_list": packing_list}

If either call returns None (API error), return None.

Also update the if __name__ == "__main__" block to test generate_trip_briefing:
  result = generate_trip_briefing("Tokyo", "Japan")
  if result:
      print("Overview:", result["overview"])
      print("Packing list:", result["packing_list"])

Write the updated file directly to src/ai_assistant.py.
