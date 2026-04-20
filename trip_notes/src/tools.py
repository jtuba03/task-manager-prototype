import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import urllib.request
from src.rag import search_guides, ensure_index

def budget_breakdown(destination: str, days: int, budget_usd: float) -> str:
    """
    Type: Pure computation (no external calls)
    Calculates a daily budget breakdown.
    """
    daily_budget = budget_usd / days
    acc = daily_budget * 0.4
    food = daily_budget * 0.3
    trans = daily_budget * 0.15
    act = daily_budget * 0.15

    return (
        f"{days}-day {destination} budget (${budget_usd:.2f} total)\n"
        f"Daily: ${daily_budget:.2f}\n"
        f"  Accommodation : ${acc:.2f}\n"
        f"  Food          : ${food:.2f}\n"
        f"  Transport     : ${trans:.2f}\n"
        f"  Activities    : ${act:.2f}"
    )

def get_weather(city: str) -> str:
    """
    Type: External HTTP API call (no API key required)
    Fetches current weather from wttr.in.
    """
    formatted_city = city.replace(" ", "+")
    url = f"https://wttr.in/{formatted_city}?format=j1"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            current = data["current_condition"][0]
            temp_c = current["temp_C"]
            temp_f = current["temp_F"]
            description = current["weatherDesc"][0]["value"]
            return f"{city}: {description}, {temp_c}°C / {temp_f}°F"
    except Exception as e:
        return f"Could not fetch weather for {city}: {e}"

def search_guides_tool(query: str) -> str:
    """
    Type: Internal system call (uses this project's own rag.py)
    """
    ensure_index()
    chunks = search_guides(query, n_results=2)
    if not chunks:
        return "No relevant information found in guides."
    return "\n\n---\n\n".join(chunks)

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "budget_breakdown",
            "description": "Calculate a daily budget breakdown for a trip given destination, number of days, and total budget in USD",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string"},
                    "days": {"type": "integer"},
                    "budget_usd": {"type": "number"}
                },
                "required": ["destination", "days", "budget_usd"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current real-time weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_guides_tool",
            "description": "Search the local travel guides for tips, recommendations, or information about a destination",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]

if __name__ == "__main__":
    print("--- Testing budget_breakdown ---")
    print(budget_breakdown("Tokyo", 7, 1400.00))
    print("\n--- Testing get_weather ---")
    print(get_weather("Tokyo"))
    print("\n--- Testing search_guides_tool ---")
    print(search_guides_tool("things to do in Tokyo"))
