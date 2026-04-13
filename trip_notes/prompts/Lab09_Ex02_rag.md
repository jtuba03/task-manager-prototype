I am extending a Python CLI project called Trip Notes.

Project structure (all commands run from trip_notes/):
  trip_notes/
  ├── guides/        ← travel guide files (.txt, .md, .pdf)
  ├── chroma_db/     ← will be created automatically
  └── src/
      └── rag.py     ← this file to create

Create src/rag.py with the following:

---

CONSTANTS at the top:
  GUIDES_DIR  = "guides"
  DB_PATH     = "chroma_db"
  COLLECTION  = "trip_guides"
  CHUNK_SIZE  = 200   # words
  CHUNK_OVERLAP = 30  # words

---

def read_file(path: str) -> str:
  Read file content based on extension:
  - .txt and .md: open(path, encoding="utf-8").read()
  - .pdf: use pypdf.PdfReader, join text from all pages
  Return the full text as a single string.
  If reading fails for any reason, print a warning like:
    "Warning: could not read [filename]: [error]"
  and return "".
  After extracting text, if the result is empty or only whitespace, print:
    "Warning: [filename] has no extractable text (scanned PDF?), skipping."
  and return "".

---

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> list[str]:
  Split text into overlapping word-based chunks.
  - Split text into words
  - Build chunks of `chunk_size` words
  - Each chunk starts `chunk_size - overlap` words after the previous one
  - Return only non-empty chunks

---

def build_index(force: bool = False):
  - If GUIDES_DIR does not exist: print "Error: guides/ folder not found." and return
  - Create a ChromaDB PersistentClient at DB_PATH
  - Get or create collection named COLLECTION
  - If force=True: delete all existing documents in the collection
  - Scan GUIDES_DIR for files with extensions .txt, .md, .pdf
  - If no files found: print "Warning: no supported files found in guides/." and return
  - For each file:
      - Read with read_file()
      - If read_file() returned "" (empty): skip this file, do not count it
      - Chunk with chunk_text()
      - If no chunks produced: skip this file
      - Embed all chunks using SentenceTransformer("all-MiniLM-L6-v2")
      - Add to collection with ids like "{stem}_chunk_{i}" (use Path(file).stem)
      - Skip any chunk whose id already exists in the collection (unless force=True)
  - After all files: print "Indexed N chunks from M files."
    (N = total chunks added this run, M = number of files that produced at least one chunk)

---

def ensure_index() -> object:
  - Create a ChromaDB PersistentClient at DB_PATH
  - Get or create collection named COLLECTION
  - If collection.count() == 0:
      print "No index found. Building from guides/..."
      call build_index()
  - Return the collection

---

def search_guides(query: str, n_results: int = 3) -> list[str]:
  - Call ensure_index() to get the collection
  - If collection.count() == 0: return []
  - Embed the query using SentenceTransformer("all-MiniLM-L6-v2")
  - Cap n_results to collection.count() to avoid ChromaDB errors:
      n_results = min(n_results, collection.count())
  - Query collection: collection.query(query_embeddings=[vector], n_results=n_results)
  - Return results["documents"][0]  (list of matching text strings)

---

Under if __name__ == "__main__":
  Call build_index() to build and test the index.

---

Dependencies: chromadb, sentence_transformers, pypdf, pathlib, os
All paths are relative to trip_notes/ (the working directory when running the app).
Do not hardcode absolute paths.
