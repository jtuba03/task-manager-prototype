import sys
import os

# Fix the import path so it works when run from the trip_notes/ root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from src.storage import load_trips
from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT, client, MODEL, rag_ask
from src.rag import ensure_index
from src.tools import run_agent, TOOL_DEFINITIONS

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
    ensure_index()

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
        st.subheader("Search My Guides")
        st.caption("Answers grounded in your guides/ documents.")

        for message in st.session_state["search_history"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        search_input = st.chat_input("Search your guides...", key="search_input")
        if search_input:
            st.session_state["search_history"].append({"role": "user", "content": search_input})
            with st.spinner("Searching guides..."):
                response = rag_ask(search_input)
            if response is None:
                response = "No response returned from the search assistant."
            st.session_state["search_history"].append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)

        if st.button("Clear search", key="clear_search"):
            st.session_state["search_history"] = []
            st.rerun()

    with agent_tab:
        st.subheader("AI Travel Agent")
        st.caption("The agent uses tools: budget calculation, live weather, and guide search.")

        agent_input = st.text_area(
            "Your question",
            placeholder="e.g. I have $1200 for 8 days in Tokyo. Check the weather and break down my budget.",
            key="agent_input",
            height=150,
        )

        answer = None
        if st.button("Ask the Agent") and agent_input.strip():
            st.session_state["agent_history"].append({"question": agent_input.strip(), "answer": ""})
            with st.spinner("Agent is working..."):
                answer = run_agent(agent_input.strip())
            if answer is None:
                answer = "Agent did not return a response."
            st.session_state["agent_history"][-1]["answer"] = answer

        if answer is not None:
            st.markdown(answer)

        with st.expander("Tools available to this agent"):
            for tool in TOOL_DEFINITIONS:
                tool_name = tool.get("function", {}).get("name")
                if tool_name:
                    st.write(f"- {tool_name}")

        st.markdown("---")
        st.markdown("### Previous queries this session:")
        for entry in reversed(st.session_state["agent_history"]):
            question = entry.get("question", "")
            answer_text = entry.get("answer", "")
            label = question if len(question) <= 60 else question[:57] + "..."
            with st.expander(label):
                st.markdown(answer_text)


if __name__ == "__main__":
    main()
