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

- [This is simple web game where a player has to guess a number with a range. There are three difficulties (easy, normal, and hard). Each mode difficulty is set with the number of attempts allowed and the range of number possible to guess. The smaller the range of numbers, the higher the chaances of guessing correctly. Likewise, the more attempts you have, the higher the chance that you guess correctly within those attempts.] Describe the game's purpose.

- [The hints provided during guess are misleading. If your guess is too low, the hint suggets to go lower and vice versa. Moreover, the difficulty scaling does not make sense. The 'normal' mode ranges from 1 to 100 as possible target numbers, however, the 'hard' mode range from 1 to 50, which is easier to guess a target number. Moreover, The 'easy' mode has less attempts than the 'normal' mode. It should be the opposite where the easier mode, gives you more chances to guess correctly. Furthermore, the allowed attempts actually allowed is n - 1 from what is shown in the left side menu

Also selecting a difficulty in the left side menu does not update the range of numbers to guess from during the actual game.

My first attempt at a fix was fixing the hint to suggest the opposite of what it was saying, so if a number is low, the player actually needs to choose higher and vice versa. I prompted Claude Code multiple tasks in a single prompt. I asked it fix the bug in def check_guess and move it to the logic_utils.py. When it did so, it also pointed out another bug in the app.py file. There was a bug where in even-numbered attempts, the 'secret' number was converted to a string. Therefore when a guess was compared to the secret, an exception caught this error, and would result in default logic where a secret number of 10 and a guess of 9 would result in a hint saying "Too High, Go Lower" because it compares the digits in order from left to right, when in reality, the opposite hint should be given] Detail which bugs you found. 

- [I prompted the AI to do the simple changes such as reframing/rescaling the difficulty appropriately for each level. For example, make the normal difficulty from 1 to 50 instead of 1 to 100 which makes more sense to be reserved for the difficult level. Similary. The normal difficutly had 8 attempts whereas the easy difficulty had 6. This did not make sense given the nature of each level so I swapped them. I also identified that the hints given were wrong. When I prompted Claude Code to fix it, it did fix it, but also identified other potential bugs that existed in the app.py file. It pointed out how there was a check for if an attempt was even-numbered or not, and that if it was, the secret number would be turned into a string, which led to a comparision of two different data types, which was caught by a try-catch block that further defaulted to incorrect logic that would lead to incorrect hints. However, I did not understand this at first, so I prompted Claude Code to explain its reasoning and give an example of a test case that would result in a incorrect hint. It gave the example of 9 and 10. Say that our secret was 10 and 9 was an even-numbered guess, eventually the logic would compare "9" > "10" which would result in the hint saying to go lower, not higher because the string comparison would compare the first character of each string. Claude code suggested to remove the uneccessary even-numbered guess check and subsequently the try-catch code. I then asked Claude code to make these concrete test case and test other normal integer insertions such as to verify the undershot guess yield a "Go higher" hint and vice versa. I had also noticed that the actual allowed attempts was n - 1 where n is the supposed allowed attempts. The fix was to change the attempts starting point from 1 to 0. However, this also affected the scoring for the game. It seemed as though Claude Code was apprehensive/cautious about this fix because of the change to the scoring. So instead of getting a score of 70 on a successful first guess, it would now change to a score of 80. I pushed back on this apprehensiveness and affirmed that it was okay, that a higher score made sense in this context given what the objective of the game was. There were a few other simples changes made, such as removing hard coded strings such as to reflect the dyanamic ranges depending on the difficulty when asking to make a guess from {low} to {high} instead of from 1 to 100 regardless of the difficulty.] Explain what fixes you applied.

## 🔧 Bugs Found and Fixes Applied

Full reproduction evidence (inputs, expected vs. actual, console output) is in [reflection.md](reflection.md), section 1.

| Bug | Fix | Why it works |
|-----|-----|--------------|
| Hints were backwards (`Too High` said "Go HIGHER!") | `check_guess` moved to `logic_utils.py`; messages swapped to "Go LOWER!" for a high guess and "Go HIGHER!" for a low guess | The hint now points toward the secret |
| On even-numbered attempts the secret was cast to a `str`, so `check_guess` fell into its `TypeError` fallback and compared strings (`"9" > "10"`) | Removed the `attempts % 2` check in `app.py` and the `try/except` fallback in `check_guess` | The secret is always an int, so comparisons are numeric on every attempt |
| Attempts allowed was `n - 1` (counter started at 1) | `attempts` now starts at `0` | The game allows exactly the number of guesses shown in the sidebar (this also moves a first-guess win from 70 to 80 points, which I accepted) |
| Easy had fewer attempts than Normal; Normal/Hard ranges were swapped | Easy 8 / Normal 6 attempts; Normal 1-50, Hard 1-100 | Difficulty now scales the way the names suggest |
| A "Too High" guess *added* 5 points on even-numbered attempts | Removed the `attempt_number % 2` branch in `update_score`; `Too High` always costs 5 | Every wrong guess now costs the same, no matter which attempt it is (covered by `test_too_high_always_costs_points`) |
| Switching difficulty mid-game kept the old secret (e.g. 40 on Easy's 1-20 range), so the game could become unwinnable | `app.py` remembers the current difficulty in session state and calls a shared `reset_game(low, high)` when it changes (New Game uses the same helper) | Each difficulty always starts a fresh game with a secret inside its own range |
| Prompt text always said "between 1 and 100" | Uses `{low}` and `{high}` from the selected difficulty | Text matches the real range |
| New Game kept the old won/lost state, score and history | New Game now resets `status`, `score` and `history`, and rolls the secret from the difficulty's range | A new game really is a clean state |

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User enters a guess of 1
2. Game return go HIGHER
3. User enters a guess of 22
4. Game return go LOWER
5. User enters a guess of 21
6. Game returns Correct!
7. User tries another guess
8. Game returns Already Won. Start new game to play again
9. New Game begins and previous state reset

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
collecting ... collected 12 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  8%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 16%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 25%]
tests/test_game_logic.py::test_hint_direction_matches_outcome PASSED     [ 33%]
tests/test_game_logic.py::test_too_high_always_costs_points[1] PASSED    [ 41%]
tests/test_game_logic.py::test_too_high_always_costs_points[2] PASSED    [ 50%]
tests/test_game_logic.py::test_too_high_always_costs_points[3] PASSED    [ 58%]
tests/test_game_logic.py::test_too_high_always_costs_points[4] PASSED    [ 66%]
tests/test_game_logic.py::test_too_low_always_costs_points[1] PASSED     [ 75%]
tests/test_game_logic.py::test_too_low_always_costs_points[2] PASSED     [ 83%]
tests/test_game_logic.py::test_too_low_always_costs_points[3] PASSED     [ 91%]
tests/test_game_logic.py::test_too_low_always_costs_points[4] PASSED     [100%]

============================== 12 passed in 0.03s ==============================
```

### Post-fix game session

The same scripted session used to reproduce the bugs (see reflection.md, section 1), run against the fixed `app.py` with Streamlit's `AppTest` runner. The app ran with no exceptions:

```
===== FIXED app (current working tree) =====

[1] Normal difficulty, secret=50: header + sidebar text
  sidebar: ['Range: 1 to 50', 'Attempts allowed: 6']
  info   : Guess a number between 1 and 50. Attempts left: 6

[2] Normal, secret=50: guess 1 (too low) then 51 (too high)
  guess=    1 -> attempts=1 score=-5 status=playing | ['Go HIGHER!']
  guess=   51 -> attempts=2 score=-10 status=playing | ['Go LOWER!']

[3] Normal, secret=10: guess 9 on the 1st submit (an even attempt in the starter)
  guess=    9 -> attempts=1 score=-5 status=playing | ['Go HIGHER!']

[4] Easy, secret=7: info text and how many guesses are really allowed
  sidebar: ['Range: 1 to 20', 'Attempts allowed: 8']
  info   : Guess a number between 1 and 20. Attempts left: 8
  (guessing 1 eight times: status stays "playing" for guesses 1-7, "lost" on guess 8)
  guess=    1 -> attempts=8 score=-40 status=lost | ['Go HIGHER!', 'Out of attempts! The secret was 7. Score: -40']

[5] Normal, secret=10: win, then press New Game, then guess again
  guess=   10 -> attempts=1 score=80 status=won | ['Correct!', 'You won! The secret was 10. Final score: 80']
  after New Game: status=playing score=0 history=[]
  guess after New Game -> ['Go HIGHER!']

[6] Normal, secret=40: one wrong guess, then switch Difficulty to Easy (range 1-20)
  Normal, secret=40, after 1 wrong guess: attempts=1 score=-5
  switched to Easy -> secret=17 attempts=0 score=0 history=[] status=playing
    info: Guess a number between 1 and 20. Attempts left: 8
  (cycling Hard, Easy, Normal, Hard, Easy: every secret landed inside its difficulty's range, 0 exceptions)
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
