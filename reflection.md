# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

--- When I first ran the game, I noticed the difficulty ranges made no sense — Normal was 0–100 but Hard was 0–50, which is easier, not harder. The attempts shown in the sidebar was 1 more than what the game actually allowed, causing inconsistency. The hints were backwards on some attempts because the secret number was being compared as a string on even attempts and as an integer on odd ones. Entering letters or non-numbers showed an error but still counted as an attempt, making the attempt counter go negative. After winning the first game, there was no way to start a new game.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

--- I used Claude for this project. When I asked AI to help me understand the code as an initial step, it explained each major helper function and its role in the game. It also proactively identified 6 obvious bugs before I even asked — that was a correct and helpful suggestion, which I verified by manually running the game and confirming each issue existed. One example where AI was slightly misleading was with the `check_guess` function: Claude's initial explanation implied the hint logic was simply swapped, but the deeper issue was that on even attempts the secret was cast to a string, causing lexicographic comparison — the pytest tests in `test_game_logic.py` (like `test_guess_too_high` and `test_guess_too_low`) helped confirm this by testing `check_guess` in isolation and revealing it returned the wrong outcome when the secret was passed as a string.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

--- To decide whether a bug was really fixed, I manually tested each case after making the change — for example, after fixing the hint direction, I entered a number higher than the secret and confirmed the message said "Go LOWER!" instead of "Go HIGHER!". For the string comparison bug, I tested on even attempts specifically by counting my guesses and verifying the outcome matched numeric logic, not alphabetical order (e.g., guessing 9 when the secret was 10 no longer incorrectly said "Too High"). I also tested the New Game button to confirm it reset attempts to 1 and generated a new secret within the correct difficulty range. Claude helped me understand the string-vs-integer comparison issue — it explained why `"9" > "10"` evaluates to `True` in Python due to lexicographic ordering, which clarified why the bug only appeared on even attempts.

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

--- The secret number kept changing because every time the user interacted with the app — clicking a button or typing in the input — Streamlit reruns the entire script from top to bottom, and `random.randint()` was being called every time without any guard, generating a brand new secret on each rerun. Think of Streamlit reruns like refreshing a webpage: every interaction reloads the whole page, so any variable you set normally gets reset unless you store it somewhere persistent. Session state (`st.session_state`) is that persistent storage — it works like a notebook that survives each refresh, so values you save there stick around between reruns. The fix was wrapping the secret generation in `if "secret" not in st.session_state:`, so the random number is only generated once at the start of a new game and stays the same for the rest of that session.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

--- One habit I want to carry forward is asking AI to explain the code before touching anything — understanding what each function is supposed to do made it much easier to spot where the logic was wrong rather than guessing. Next time I work with AI on a coding task, I would ask it to explain *why* a fix works, not just what to change, so I actually understand the reasoning and can apply it independently. This project changed how I think about AI-generated code: it showed me that AI can produce code that looks correct and runs without errors but still has subtle logical bugs, so I now treat AI output as a starting point that needs careful human review, not a finished product.
