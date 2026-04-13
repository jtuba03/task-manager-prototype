# Lab 6: Vibe Coding with Git
## CISC 395 - Applied Generative AI and LLM Applications

**Points:** 100 points (+15 bonus)
**Submission:** Upload this completed `Lab06.md` file to Blackboard

---

## Prerequisites (Complete Before Starting)

These are setup steps — not graded, but required for the lab to work.

### 1. Git Installed and Configured

```bash
# Check if Git is installed
git --version
```

If you see a version number, Git is ready. If not:
- **Windows:** Download from https://git-scm.com/download/win (use default settings)
- **Mac:** Run `brew install git` or `xcode-select --install`

Then configure your identity (do this once):
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

Verify:
```bash
git config --list   # Should show your name and email
```

### 2. Python + Pygame Installed

```bash
python --version        # Must be Python 3.8 or higher
pip install pygame
```

### 3. GitHub Account

Sign up at https://github.com (free). Use your school email for GitHub Student benefits.

### 4. AI Tool Ready (Choose One)

- **Gemini CLI** in terminal: `gemini --version`
- **Gemini Web / ChatGPT** in browser: just open the website
- **GitHub Copilot Chat** in VS Code: `Ctrl+Shift+I`

---

## Git Quick Reference

| Command | What it does |
|---------|--------------|
| `git init` | Create new repository |
| `git status` | Check current state (use constantly!) |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Save a snapshot |
| `git log --oneline` | View commit history |
| `git push` | Upload to GitHub |
| `git push -u origin main` | First push only |

**Undo Cheat Sheet — when AI breaks your code:**

```
Code broken. What do I do?
   |
   +-- Haven't run git add?
   |       git restore game.py
   |
   +-- Already git add, but NOT committed?
   |       git restore --staged game.py
   |       git restore game.py
   |
   +-- Already committed?
           git revert HEAD       (safest — creates undo commit)
```

---

## Step 0: Download Lab Files

Open your terminal and run:

```bash
curl -o Lab06.zip "https://github.com/tisage/CISC395/raw/refs/heads/main/Lab06/Lab06.zip"
```

Extract the zip:

```bash
# Mac / Linux
unzip Lab06.zip

# Windows (PowerShell or Command Prompt)
tar -xf Lab06.zip
```

You should now have a `Lab06` folder containing:
```
Lab06/
├── Lab06.md           ← this file (your submission)
└── template/
    ├── game_design_prompt_snake.md
    ├── game_design_prompt_pingpong.md
    ├── game_design_prompt_breakout.md
    ├── game_design_prompt_flappybird.md
    ├── game_design_prompt_spaceshooter.md
    └── game_design_prompt_mazerunner.md
```

Navigate into the folder:
```bash
cd Lab06
```

---

## Step 1: Initialize Your Repository

Create a Git repository inside the `Lab06` folder:

```bash
git init
```

**Create a GitHub repository:**
1. Go to https://github.com → click **"+"** → **"New repository"**
2. Name it `lab06` (or any name you like)
3. Set it to **Public**
4. **Do NOT** check "Initialize with README"
5. Click **Create repository**

Copy the URL GitHub shows you (looks like `https://github.com/YOUR_USERNAME/lab06.git`), then connect:

```bash
git remote add origin https://github.com/YOUR_USERNAME/lab06.git
git branch -M main
```

---

## Step 2: Choose a Template + Commit "initial"

Open the `template/` folder and choose ONE game:

| Game | File | Difficulty |
|------|------|------------|
| **Snake** | `game_design_prompt_snake.md` | Easy |
| **Pong** | `game_design_prompt_pingpong.md` | Easy |
| **Breakout** | `game_design_prompt_breakout.md` | Medium |
| **Flappy Bird** | `game_design_prompt_flappybird.md` | Medium |
| **Space Shooter** | `game_design_prompt_spaceshooter.md` | Hard |
| **Maze Runner** | `game_design_prompt_mazerunner.md` | Hard |

> **Tip:** If this is your first time with Pygame, start with Snake or Pong.

Read through your chosen template to understand what the game will look like.

Now make your first commit:
```bash
git add .
git commit -m "initial"
git push -u origin main
```

Check GitHub — your files should be there.

---

## Step 3: Generate Your Game → Commit "first draft"

Open your chosen template file. Copy the **entire content** and paste it into your AI tool as a prompt.

**Using Gemini CLI:**
```bash
gemini
# Then paste the template content in the chat
```

**Using ChatGPT / Gemini Web:**
- Paste the template content directly into the chat

**Using GitHub Copilot in VS Code:**
- Press `Ctrl+Shift+I` → paste the template content

The AI will generate a complete Python game. Save the output as `game.py` inside your `Lab06` folder.

Test it immediately:
```bash
python game.py
```

**If it runs (even if buggy) — commit now:**
```bash
git add game.py
git commit -m "first draft"
git push
```

**If it crashes with an error** — go to Step 4 before committing.

> **Important:** The goal of "first draft" is just to have something generated, not necessarily working perfectly.

---

## Step 4: Debug Until It Runs

If `python game.py` shows an error or crashes:

**Option A — Ask AI to fix the error:**

Copy the error message and ask your AI:
```
This game.py gives the following error:
[paste the error here]

Please fix the code.
```

Replace `game.py` with the fixed version and test again.
Repeat until it runs.

**Option B — If the game still doesn't work after 3–4 attempts:**

Switch to a different (simpler) template. Roll back to "initial" first:

```bash
git revert HEAD      # This undoes "first draft", keeps your git history clean
git push
```

Then go back to Step 2, pick a different template, and start generating again.

---

**Once the game runs without crashing and you can play it:**

```bash
git add game.py
git commit -m "fix bug"
git push
```

> **If a change you make during customization breaks the game**, use the undo cheat sheet above. You can always `git restore game.py` to go back to the last working commit.

---

## Step 5: Customize the Details

Now make the game your own. Change at least **3 of the following**:

- Window size (width, height)
- Colors (snake color, background, food, player, etc.)
- Speed or frame rate
- Score values or rules
- Font size or text position
- Any other visual or gameplay detail you find in the code

For each change: edit the code, test it, then commit:

```bash
git add game.py
git commit -m "customize: [describe what you changed]"
git push
```

> **Example commit messages:**
> - `customize: change background to dark blue`
> - `customize: increase snake speed and food count`
> - `customize: add score display in top-right corner`

---

## Step 6: Verify Your Commit History

Before finishing, check that all required commits are present:

```bash
git log --oneline
```

You should see **at least these commits** (newest at the top):
```
xxxxxxx customize: [your change]
xxxxxxx fix bug
xxxxxxx first draft
xxxxxxx initial
```

If any are missing, go back and complete that step.

Push everything:
```bash
git push
```

---

## Bonus: Add a New Feature (+15 points)

Add one meaningful new feature to your game. This must be something that changes gameplay, not just a visual tweak.

**Ideas by game type:**

| Game | Feature Ideas |
|------|--------------|
| **Any** | Lives system, difficulty levels, high score display, title screen |
| **Snake** | Multiple food types worth different points, speed power-up |
| **Pong** | AI-controlled opponent paddle, score to win condition |
| **Breakout** | Indestructible bricks, ball speed increase per level |
| **Flappy Bird** | Coin collectibles, score multiplier |
| **Space Shooter** | Shield power-up, multiple enemy types |
| **Maze Runner** | Timer, enemy that chases the player |

When done:
```bash
git add game.py
git commit -m "add: [feature name]"
git push
```

---

## Reflection and Submission

Fill in your answers below. Then update your GitHub URL and submit this file to Blackboard.

---

**GitHub Repository URL:**
```
[PASTE YOUR GITHUB REPO URL HERE]
Example: https://github.com/yourname/lab06
```

---

**Q1. Which template did you choose? Why did you pick this game?**

```
[YOUR ANSWER]
```

---

**Q2. Describe your first draft: Did the game run on the first try? If not, what error appeared?**

```
[YOUR ANSWER]
```

---

**Q3. What was the hardest bug to fix? How did you solve it (AI prompt, manual fix, or rollback)?**

```
[YOUR ANSWER]
```

---

**Q4. What customizations did you make in Step 5? List all 3+ changes.**

```
1. [YOUR ANSWER]
2. [YOUR ANSWER]
3. [YOUR ANSWER]
```

---

**Q5. Did you need to roll back to "initial" and switch templates? If yes, explain what happened.**

```
[YOUR ANSWER — write "No" if you did not roll back]
```

---

**Q6. (Bonus only) What new feature did you add? Briefly describe how it works.**

```
[YOUR ANSWER — write "N/A" if you did not complete the bonus]
```

---

**Q7. What is one thing you learned from this lab?**

```
[YOUR ANSWER]
```

---

## Grading Rubric

| Item | Points | How it's checked |
|------|--------|-----------------|
| Commit "initial" exists | 10 | GitHub commit history |
| Commit "first draft" exists | 10 | GitHub commit history |
| Commit "fix bug" exists (game runs) | 15 | GitHub commit history + running game.py |
| Commit "customize: ..." exists | 15 | GitHub commit history |
| Game runs and is playable | 30 | Professor runs game.py |
| Reflection Q1–Q7 answered | 20 | This file |
| **Total** | **100** | |
| **Bonus: "add: ..." commit + new feature** | **+15** | GitHub commit history |

> **Note:** The professor will verify your GitHub commit history. Commits must be present with the correct messages. Do not create all commits at once at the end — the history shows when each commit was made.

---

*End of Lab 6*
