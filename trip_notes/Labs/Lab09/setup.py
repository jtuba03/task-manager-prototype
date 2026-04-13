"""
Lab 09: RAG — Search Your Travel Guides — Setup
=================================================
Run this script from your CISC395 workspace root AFTER completing Lab 08.

Usage (from CISC395/ root):
    python Labs/Lab09/setup.py

OR download and run:
    curl -o setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab09/setup.py
    python setup.py
"""

import os
import sys
import urllib.request

BASE_URL = "https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab09/"
ZIP_URL  = "https://github.com/tisage/CISC395/archive/refs/heads/main.zip"


def download_file(url, dest):
    """Download a file and verify it is not empty or an HTML error page.
    Returns (success: bool, reason: str)."""
    try:
        urllib.request.urlretrieve(url, dest)
    except Exception as e:
        return False, str(e)

    if os.path.getsize(dest) == 0:
        os.remove(dest)
        return False, "empty file (server returned nothing)"

    try:
        with open(dest, "r", errors="ignore") as f:
            first = f.read(80).lstrip()
        if first.startswith("<"):
            os.remove(dest)
            return False, "blocked by network (received HTML instead of file)"
    except Exception:
        pass

    return True, None
SHARED_URL = "https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/shared/"

# Lab-specific files — downloaded from Lab09/
DOWNLOADS = [
    # Check script
    ("tests/check_rag_setup.py",              "tests/check_rag_setup.py"),
    # Prompt files
    ("prompts/Lab09_Ex02_rag.md",             "prompts/Lab09_Ex02_rag.md"),
    ("prompts/Lab09_Ex04_ragask.md",          "prompts/Lab09_Ex04_ragask.md"),
    ("prompts/Lab09_Ex04_menu.md",            "prompts/Lab09_Ex04_menu.md"),
    # Sample travel guides (txt, md, pdf — all formats supported by rag.py)
    ("guides/tokyo.txt",                      "guides/tokyo.txt"),
    ("guides/new_york_city.txt",              "guides/new_york_city.txt"),
    ("guides/san_francisco.md",               "guides/san_francisco.md"),
    ("guides/paris.md",                       "guides/paris.md"),
    ("guides/paris_5day_guide.pdf",           "guides/paris_5day_guide.pdf"),
    ("guides/japan_luxury.pdf",               "guides/japan_luxury.pdf"),
]

# Shared utilities — always downloaded fresh to get latest version
SHARED_DOWNLOADS = [
    ("check_progress.py", "tests/check_progress.py"),
]


def check_location():
    cwd = os.getcwd()
    if os.path.basename(cwd) in ("Lab09", "Labs"):
        print("WARNING: Run this from your CISC395 workspace root, not from inside Labs/.")
        print(f"  Current directory: {cwd}")
        print("  Try: cd ../.." if os.path.basename(cwd) == "Lab09" else "  Try: cd ..")
        print("  Then: python Labs/Lab09/setup.py")
        sys.exit(1)


def setup():
    check_location()

    root = "trip_notes"

    if not os.path.exists(root):
        print("ERROR: trip_notes/ not found.")
        print("Complete Lab 07 first to create the project, then run this setup.")
        sys.exit(1)

    print("Setting up Lab 09 in trip_notes/...")
    print()

    # Ensure directories exist
    for d in ["prompts", "tests", "guides"]:
        path = os.path.join(root, d)
        os.makedirs(path, exist_ok=True)
        if d == "guides":
            print(f"  ✓  trip_notes/guides/ ready")

    print()
    print("Downloading...")
    failed = []
    all_downloads = [(BASE_URL + r, l, False) for r, l in DOWNLOADS] + \
                    [(SHARED_URL + r, l, False) for r, l in SHARED_DOWNLOADS]

    for url, local, _ in all_downloads:
        dest = os.path.join(root, local)
        # For guides: skip if the file already exists (don't overwrite student work)
        if local.startswith("guides/") and os.path.exists(dest):
            print(f"  -  trip_notes/{local}  (already exists, skipped)")
            continue
        ok, reason = download_file(url, dest)
        if ok:
            print(f"  \u2713  trip_notes/{local}")
        else:
            print(f"  \u2717  trip_notes/{local}  ({reason})")
            failed.append(local)

    print()
    if failed:
        print(f"  {len(failed)} file(s) failed to download:")
        for f in failed:
            print(f"    - trip_notes/{f}")
        print()
        print("  Fix: Download the ZIP and copy the missing files manually:")
        print(f"    {ZIP_URL}")
        print("  Extract and copy the missing files from Lab09/ into trip_notes/.")
        print()

    print("Done! Lab 09 files ready in trip_notes/.")
    print()
    print("Next steps — follow Lab 09 Setup section in order:")
    print("  1. cd trip_notes")
    print("  2. pip install chromadb sentence-transformers pypdf")
    print("  3. pip freeze > ../requirements.txt")
    print("  4. python tests/check_rag_setup.py")
    print()
    print("  NOTE: Sample guides are in trip_notes/guides/ — add your own before Ex 2.")


def refresh():
    root = "trip_notes"
    if not os.path.exists(root):
        print("trip_notes/ not found. Run without --refresh first.")
        sys.exit(1)
    print("Refreshing Lab 09 files in trip_notes/...")
    all_downloads = [(BASE_URL + r, l) for r, l in DOWNLOADS] + \
                    [(SHARED_URL + r, l) for r, l in SHARED_DOWNLOADS]
    for url, local in all_downloads:
        dest = os.path.join(root, local)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        # For guides: skip if already exists even on refresh
        if local.startswith("guides/") and os.path.exists(dest):
            print(f"  -  trip_notes/{local}  (skipped)")
            continue
        ok, reason = download_file(url, dest)
        if ok:
            print(f"  \u2713  trip_notes/{local}")
        else:
            print(f"  \u2717  {local}  ({reason})")


if __name__ == "__main__":
    if "--refresh" in sys.argv:
        check_location()
        refresh()
    else:
        setup()
