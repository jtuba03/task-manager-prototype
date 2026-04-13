In my Trip Notes project, src/main.py already has a menu with options [1] through [7].

src/ai_assistant.py now has both ask() and rag_ask().
src/rag.py has build_index(force=False) and search_guides().

Add these options to src/main.py:

[8] Search my guides  (under the -- AI -- section)
  - Display label: "[8] Search my guides"
  - Prompt the user: "Your question: "
  - Call rag_ask(question) from src.ai_assistant
  - Print the returned answer
  - Note: search_guides() inside rag_ask() automatically builds the index
    if chroma_db/ is empty — no manual step needed

[R] Rebuild search index  (below the -- AI -- section, next to [Q] Quit)
  - Display label: "[R] Rebuild search index"
  - Handler: elif choice.lower() == "r":
  - Print: "Rebuilding index from guides/..."
  - Call build_index(force=True) from src.rag
  - Print: "Done. Use [8] to search your updated guides."

Required imports to add:
  from src.ai_assistant import rag_ask
  from src.rag import build_index

Menu display should look like:
  -- Data --
  [1] Add destination       [2] List all destinations
  [3] Mark as visited       [4] Show statistics

  -- AI --
  [6] Ask AI                [7] Trip Briefing
  [8] Search my guides

  [R] Rebuild search index
  [Q] Quit

Keep all existing menu options [1]–[7] and [Q] completely unchanged.
Write the updated file directly to src/main.py.
