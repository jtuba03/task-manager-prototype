import os
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
import pypdf

# CONSTANTS
GUIDES_DIR = "guides"
DB_PATH = "chroma_db"
COLLECTION = "trip_guides"
CHUNK_SIZE = 200  # words
CHUNK_OVERLAP = 30  # words

def read_file(path: str) -> str:
    """
    Read file content based on extension:
    - .txt and .md: open(path, encoding='utf-8').read()
    - .pdf: use pypdf.PdfReader, join text from all pages
    Return the full text as a single string.
    """
    path_obj = Path(path)
    suffix = path_obj.suffix.lower()
    text = ""
    try:
        if suffix in [".txt", ".md"]:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        elif suffix == ".pdf":
            reader = pypdf.PdfReader(path)
            pages_text = [page.extract_text() for page in reader.pages if page.extract_text()]
            text = "\n".join(pages_text)
        else:
            return "" # Unsupported file type

        if not text or not text.strip():
            print(f"Warning: {path_obj.name} has no extractable text (scanned PDF?), skipping.")
            return ""
        
        return text

    except Exception as e:
        print(f"Warning: could not read {path_obj.name}: {e}")
        return ""

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping word-based chunks.
    """
    words = text.split()
    if not words:
        return []
    
    chunks = []
    step = chunk_size - overlap
    # Ensure step is at least 1 to avoid infinite loop
    if step <= 0:
        step = 1

    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        chunk = " ".join(chunk_words)
        if chunk.strip():
            chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
            
    return chunks

def build_index(force: bool = False):
    """
    Build the vector index from files in GUIDES_DIR.
    """
    guides_path = Path(GUIDES_DIR)
    if not guides_path.exists():
        print(f"Error: {GUIDES_DIR}/ folder not found.")
        return

    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION)

    if force:
        # Delete all documents if force is True
        # Since Chroma doesn't have a simple 'delete all' without filters in some versions,
        # we might need to delete by IDs or delete the collection and recreate.
        # But instructions say "delete all existing documents in the collection".
        # If collection exists, we can delete it and recreate it to be sure.
        try:
            client.delete_collection(name=COLLECTION)
            collection = client.create_collection(name=COLLECTION)
        except Exception:
            # Collection might not exist yet
            collection = client.get_or_create_collection(name=COLLECTION)

    files = list(guides_path.glob("*.txt")) + list(guides_path.glob("*.md")) + list(guides_path.glob("*.pdf"))
    if not files:
        print(f"Warning: no supported files found in {GUIDES_DIR}/.")
        return

    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    total_chunks = 0
    files_with_chunks = 0

    for file_path in files:
        content = read_file(str(file_path))
        if not content:
            continue
        
        chunks = chunk_text(content)
        if not chunks:
            continue
        
        stem = file_path.stem
        ids = [f"{stem}_chunk_{i}" for i in range(len(chunks))]
        
        # In Chroma, we can check if IDs exist or just try to add.
        # Instructions: "Skip any chunk whose id already exists in the collection (unless force=True)"
        
        final_chunks = []
        final_ids = []
        
        if not force:
            # Check for existing IDs
            existing = collection.get(ids=ids)
            existing_ids = set(existing['ids'])
            for chunk, cid in zip(chunks, ids):
                if cid not in existing_ids:
                    final_chunks.append(chunk)
                    final_ids.append(cid)
        else:
            final_chunks = chunks
            final_ids = ids

        if final_chunks:
            # Embed chunks
            embeddings = model.encode(final_chunks).tolist()
            collection.add(
                ids=final_ids,
                documents=final_chunks,
                embeddings=embeddings
            )
            total_chunks += len(final_chunks)
            files_with_chunks += 1

    print(f"Indexed {total_chunks} chunks from {files_with_chunks} files.")

def ensure_index() -> object:
    """
    Ensure the collection exists and is populated.
    """
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION)
    
    if collection.count() == 0:
        print(f"No index found. Building from {GUIDES_DIR}/...")
        build_index()
        # Re-fetch collection after building
        collection = client.get_or_create_collection(name=COLLECTION)
        
    return collection

def search_guides(query: str, n_results: int = 3) -> list[str]:
    """
    Search the collection using embeddings.
    """
    collection = ensure_index()
    if collection.count() == 0:
        return []
    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    vector = model.encode([query]).tolist()
    
    n_results = min(n_results, collection.count())
    results = collection.query(
        query_embeddings=vector,
        n_results=n_results
    )
    
    return results["documents"][0] if results["documents"] else []

if __name__ == "__main__":
    build_index()
