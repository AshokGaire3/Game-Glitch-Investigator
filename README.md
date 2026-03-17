# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game Purpose

A number guessing game built with Streamlit where the player tries to guess a secret number within a limited number of attempts. The game supports three difficulty levels (Easy: 1–20, Normal: 1–50, Hard: 1–100), provides higher/lower hints after each guess, tracks a running score, and shows guess history. The twist: the original AI-generated code shipped with several bugs that made the game unwinnable.

### Bugs Found

1. **Secret number reset on every rerun** — `random.randint()` was called unconditionally at the top of the script, so every button click (which triggers a Streamlit rerun) generated a new secret.
2. **Backwards hints on even attempts** — the secret was cast to a string on even attempts, causing lexicographic comparison (e.g., `"9" > "10"` → `True`), flipping the "Too High"/"Too Low" direction.
3. **Difficulty ranges were inverted** — Normal was 0–100 but Hard was 0–50, making Hard easier than Normal.
4. **Attempt counter off-by-one** — the sidebar displayed 1 more attempt than the game actually allowed.
5. **Invalid input still consumed an attempt** — entering letters or non-numbers showed an error but incremented the attempt counter.
6. **No way to restart after winning** — once the game was won there was no path to start a new game.

### Fixes Applied

- Wrapped the secret generation in `if "secret" not in st.session_state:` so it only runs once per game session.
- Fixed `check_guess` in `logic_utils.py` to always compare integers, removing the string-cast path.
- Corrected difficulty ranges in `get_range_for_difficulty` so Hard (1–100) is genuinely harder than Normal (1–50).
- Aligned the sidebar attempt display with the actual `attempt_limit` value.
- Moved the attempt increment inside the valid-input branch so invalid entries don't cost attempts.
- Added a working "New Game" button that resets `st.session_state` and calls `st.rerun()`.

## 📸 Demo

![Winning game screenshot](assets/demo_win.png)

> The fixed game correctly tracks the secret number, shows accurate Higher/Lower hints, and displays a win message with the final score.

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
