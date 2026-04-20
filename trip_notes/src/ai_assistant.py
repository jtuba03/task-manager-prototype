import os
import sys
from dotenv import load_dotenv, find_dotenv
import openai
from openai import OpenAI
from src.rag import search_guides

# Find and load the .env file (searching upwards from trip_notes/)
load_dotenv(find_dotenv())

# Client setup for OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

MODEL = "openrouter/free"

# A knowledgeable, concise travel assistant focused on practical, budget-friendly advice for student travelers.
TRAVEL_SYSTEM_PROMPT = (
    "You are a knowledgeable and concise travel assistant specialized in practical, "
    "budget-friendly advice for student travelers. Your answers must be under 200 words. "
    "Be specific and name specific places, avoid generalities."
)

def ask(user_message, system_prompt=None, temperature=0.7, max_tokens=1024):
    """
    Calls the OpenRouter API with the given user_message and optional system_prompt.
    Returns the response content (str or empty string if None).
    Returns None if an API error occurs.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=30,
            extra_body={"reasoning": {"enabled": True}}
        )
        content = response.choices[0].message.content
        if content is None:
            return ""
        return content

    except (openai.AuthenticationError, openai.RateLimitError, 
            openai.APIConnectionError, openai.APITimeoutError) as e:
        print(f"API Error: {e}")
        return None


def rag_ask(question: str) -> str:
    """
    Search the user's travel guides and answer using the retrieved context.
    """
    chunks = search_guides(question, n_results=3)
    if not chunks:
        return "No guides found. Add .txt, .md, or .pdf files to guides/ and press [R] to rebuild the index."

    context = "\n\n---\n\n".join(chunks)
    rag_system_prompt = (
        "You are a travel assistant with access to the user's personal travel guides. "
        "Use the context below as your PRIMARY source. If the context contains relevant "
        "information, use it in your answer. If the context is insufficient, you may "
        "supplement with general knowledge but clearly indicate what comes from the guides "
        "and what is general advice. If the context has nothing relevant at all, say: "
        "I don't have specific guide information about that.\n\n"
        "Context from your travel guides:\n"
        f"{context}"
    )

    return ask(question, system_prompt=rag_system_prompt, max_tokens=2048)

def generate_trip_briefing(city: str, country: str, notes: list = None) -> dict:
    """
    Builds a trip briefing using prompt chaining:
    1. Overview of the destination.
    2. Packing list based on the overview.
    """
    # Call 1: Overview
    base = f"Give a 3-sentence travel overview of {city}, {country}. Cover: what it's like to visit, best season to go, and one must-see attraction."
    if notes and len(notes) > 0:
        notes_text = "\n".join(f"- {n}" for n in notes)
        overview_prompt = base + f"\n\nPersonal notes about this trip:\n{notes_text}"
    else:
        overview_prompt = base
    
    overview = ask(overview_prompt, system_prompt=TRAVEL_SYSTEM_PROMPT)
    if overview is None:
        return None
    
    # Call 2: Packing List
    packing_prompt = f"Based on this destination overview:\n{overview}\n\nWrite a 5-item packing list specific to {city}."
    packing_list = ask(packing_prompt, system_prompt=TRAVEL_SYSTEM_PROMPT)
    if packing_list is None:
        return None
    
    return {"overview": overview, "packing_list": packing_list}

if __name__ == "__main__":
    print("--- Testing ask() ---")
    result = ask("What is the best time of year to visit Japan?",
                system_prompt=TRAVEL_SYSTEM_PROMPT)
    if result is not None:
        print(result)
    
    print("\n--- Testing generate_trip_briefing() ---")
    briefing = generate_trip_briefing("Tokyo", "Japan")
    if briefing:
        print("Overview:", briefing["overview"])
        print("\nPacking list:", briefing["packing_list"])
    else:
        print("Failed to get a briefing from the AI.")
