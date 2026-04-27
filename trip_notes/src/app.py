import sys
import os

# Fix the import path so it works when run from the trip_notes/ root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from src.storage import load_trips
from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT, client, MODEL

MAX_TURNS = 8


def init_session_state() -> None:
    if "trips" not in st.session_state:
        st.session_state["trips"] = load_trips()
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "search_history" not in st.session_state:
        st.session_state["search_history"] = []
    if "agent_history" not in st.session_state:
        st.session_state["agent_history"] = []
    if "briefing" not in st.session_state:
        st.session_state["briefing"] = None


def build_briefing_prompt(trip_name: str, country: str, notes: list[str]) -> str:
    notes_text = "\n".join(f"- {note}" for note in notes)
    return (
        f"Create a travel briefing for {trip_name}, {country}. "
        "Include a short overview and a concise packing list. "
        "Use the following personal notes as part of the briefing:\n"
        f"{notes_text}"
    )


def main() -> None:
    st.set_page_config(page_title="Trip Notes AI", page_icon="✈️", layout="wide")

    init_session_state()

    st.sidebar.title("✈️ Trip Notes AI")
    st.sidebar.caption("Powered by Atlas, your travel AI")

    trip_collection = st.session_state["trips"]
    all_trips = trip_collection.get_all()
    trip_names = [trip.name for trip in all_trips] or ["(no trips yet)"]

    selected_trip_name = st.sidebar.selectbox("📍 Current trip", trip_names)
    selected_trip = None
    if all_trips and selected_trip_name != "(no trips yet)":
        selected_trip = next((trip for trip in all_trips if trip.name == selected_trip_name), None)

    if selected_trip:
        if selected_trip.notes:
            with st.sidebar.expander(f"📋 Notes ({len(selected_trip.notes)})"):
                for note in selected_trip.notes:
                    st.write(f"- {note}")
        else:
            st.sidebar.caption("No notes yet for this trip.")
    else:
        st.sidebar.caption("No trips yet. Add a trip in the CLI first.")

    if st.sidebar.button("Generate Briefing"):
        if selected_trip and selected_trip.notes:
            prompt = build_briefing_prompt(
                selected_trip.name,
                selected_trip.country,
                selected_trip.notes,
            )
            with st.spinner("Generating briefing..."):
                briefing = ask(prompt, system_prompt=TRAVEL_SYSTEM_PROMPT)
            if briefing is None:
                st.sidebar.error("Failed to generate briefing. Check your API connection.")
            else:
                st.session_state["briefing"] = briefing
        else:
            st.sidebar.warning("Add some notes first.")

    if st.session_state["briefing"]:
        st.sidebar.markdown("### Briefing")
        st.sidebar.markdown(st.session_state["briefing"])

    chat_tab, search_tab, agent_tab = st.tabs(["💬 Chat", "🔍 Search", "🤖 Agent"])

    with chat_tab:
        st.subheader("Atlas — Your Travel AI")
        st.caption("Ask me anything about travel.")

        for message in st.session_state["chat_history"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        user_input = st.chat_input("Ask Atlas anything...")
        if user_input:
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            trimmed_history = st.session_state["chat_history"][-(MAX_TURNS * 2):]
            messages = [
                {"role": "system", "content": TRAVEL_SYSTEM_PROMPT},
                *trimmed_history,
            ]
            with st.spinner("Atlas is thinking..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                )
            assistant_content = response.choices[0].message.content
            if assistant_content is None:
                assistant_content = ""
            st.session_state["chat_history"].append({"role": "assistant", "content": assistant_content})
            with st.chat_message("assistant"):
                st.write(assistant_content)

        if st.button("Clear chat", key="clear_chat"):
            st.session_state["chat_history"] = []
            st.rerun()

    with search_tab:
        st.info("Coming soon — Exercise 3")

    with agent_tab:
        st.info("Coming soon — Exercise 4")


if __name__ == "__main__":
    main()
