I have a Trip Notes CLI app. Read src/main.py first.

src/main.py currently has a menu loop with options [1]–[5], where [5] is Exit.

Make the following two changes to src/main.py. Do NOT change any other logic.

---

CHANGE 1 — Replace number exit with Q key:
- Remove [5] from the menu display
- Replace the choice == "5" handler with: if choice.lower() == "q": break

---

CHANGE 2 — Reformat the menu display into visual groups:

  === Trip Notes ===

  -- Data --
  [1] Add destination
  [2] List all destinations
  [3] Mark as visited
  [4] Show statistics

  -- AI --
  (coming soon)

  [Q] Quit

Keep exactly this structure. The "-- AI --" section is intentionally empty for now — AI options will be added in the next exercise.

---

Write the updated file directly to src/main.py.
