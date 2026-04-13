I am extending a Python CLI project called Trip Notes.

Project structure (all commands run from inside trip_notes/):
  trip_notes/
  ├── src/main.py         (menu with options [1]–[5], already working)
  ├── src/models.py       (Destination @dataclass, TripCollection)
  ├── src/storage.py      (load_trips, save_trips)
  ├── .env                (contains OPENROUTER_API_KEY)
  └── requirements.txt    (openai and python-dotenv are installed)

Read src/models.py first so you know the existing class structure.

Then create src/ai_assistant.py with the following:

1. Imports and setup:
   - from dotenv import load_dotenv, find_dotenv
   - import os, openai
   - from openai import OpenAI
   - call load_dotenv(find_dotenv()) at module level
     (find_dotenv() searches upward from trip_notes/ to find CISC395/.env)

2. Client and model constant:
   client = OpenAI(
       api_key=os.getenv("OPENROUTER_API_KEY"),
       base_url="https://openrouter.ai/api/v1",
   )
   MODEL = "openrouter/free"

3. A constant TRAVEL_SYSTEM_PROMPT (str) that defines a knowledgeable,
   concise travel assistant focused on practical, budget-friendly advice
   for student travelers. Keep answers under 200 words. Be specific —
   name places, not generalities.

4. A function:
   ask(user_message, system_prompt=None, temperature=0.7, max_tokens=1024) -> str | None
   - Builds messages list: system message first (if system_prompt provided), then user
   - Calls client.chat.completions.create(
         model=MODEL,
         messages=messages,
         temperature=temperature,
         max_tokens=max_tokens,
         timeout=30,
     )
   - Returns response.choices[0].message.content (str or None)
   - If content is None: return "" (empty string, not None)
   - Handles these exceptions with a friendly print and returns None:
       openai.AuthenticationError
       openai.RateLimitError
       openai.APIConnectionError
       openai.APITimeoutError

5. Under if __name__ == "__main__":
   result = ask("What is the best time of year to visit Japan?",
                system_prompt=TRAVEL_SYSTEM_PROMPT)
   print(result)

Do not add an if __name__ == "__main__" block to any other file.
Write the file directly to src/ai_assistant.py.
