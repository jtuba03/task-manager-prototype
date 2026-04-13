In my Trip Notes project (run from trip_notes/):

- src/rag.py already exists with:
    search_guides(query: str, n_results: int = 3) -> list[str]
    (auto-builds the index if chroma_db/ is empty)

- src/ai_assistant.py already has:
    ask(prompt: str, system_prompt: str = None, temperature: float = 0.7, max_tokens: int = 1024) -> str

Add a function rag_ask(question: str) -> str to src/ai_assistant.py:

1. Import search_guides from src.rag
   (use: from src.rag import search_guides)

2. Call search_guides(question, n_results=3) to get relevant chunks

3. If chunks is empty or None:
   return "No guides found. Add .txt, .md, or .pdf files to guides/ and press [R] to rebuild the index."

4. Join chunks with "\n\n---\n\n" as separator to form context

5. Build this system prompt (use an f-string):
   "You are a travel assistant with access to the user's personal travel guides.
    Use the context below as your PRIMARY source. If the context contains relevant
    information, use it in your answer. If the context is insufficient, you may
    supplement with general knowledge but clearly indicate what comes from the guides
    and what is general advice. If the context has nothing relevant at all, say:
    I don't have specific guide information about that.

    Context from your travel guides:
    {context}"

6. Call ask(question, system_prompt=rag_system_prompt, max_tokens=2048) and return the result
   (max_tokens=2048 because the context is longer and the answer may be detailed)

Place rag_ask() after the existing ask() function.
Do not modify ask() or any existing code.
Write the updated file directly to src/ai_assistant.py.
