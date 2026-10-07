import pytest

from logic_utils import check_guess

#FIX: Removed previous test cases because entire string to int comparison was removed in core logic. Updated with new tests

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome is "Too High" and hint says go lower
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome is "Too Low" and hint says go higher
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_hint_direction_matches_outcome():
    # Regression: hints used to be swapped (too high -> "Go HIGHER!")
    assert "HIGHER" not in check_guess(60, 50)[1]
    assert "LOWER" not in check_guess(40, 50)[1]


from streamlit.testing.v1 import AppTest

NORMAL_ATTEMPT_LIMIT = 6  # app.py: Normal difficulty allows 6 attempts


def _new_app(secret=50):
    at = AppTest.from_file("app.py").run()
    at.session_state["secret"] = secret
    return at


def _submit_guess(at, guess):
    at.text_input(key="guess_input_Normal").set_value(str(guess))
    at.button[0].click()  # "Submit Guess"
    return at.run()


def test_game_ends_after_max_attempts():
    # Guessing wrong every time should end the game on the final allowed attempt
    at = _new_app(secret=50)
    for _ in range(NORMAL_ATTEMPT_LIMIT):
        assert at.session_state["status"] == "playing"
        at = _submit_guess(at, 1)

    assert at.session_state["attempts"] == NORMAL_ATTEMPT_LIMIT
    assert at.session_state["status"] == "lost"
    assert any("Out of attempts" in e.value for e in at.error)


def test_no_more_guesses_accepted_after_game_over():
    # Once the game is lost, extra submissions must not count as attempts
    at = _new_app(secret=50)
    for _ in range(NORMAL_ATTEMPT_LIMIT):
        at = _submit_guess(at, 1)

    at = _submit_guess(at, 2)

    assert at.session_state["attempts"] == NORMAL_ATTEMPT_LIMIT
    assert at.session_state["status"] == "lost"
    assert any("Game over" in e.value for e in at.error)


def test_game_not_over_before_max_attempts():
    # One attempt short of the limit, the game should still be playable
    at = _new_app(secret=50)
    for _ in range(NORMAL_ATTEMPT_LIMIT - 1):
        at = _submit_guess(at, 1)

    assert at.session_state["status"] == "playing"
