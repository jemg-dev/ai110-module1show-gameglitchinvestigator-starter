import pytest

from logic_utils import check_guess, update_score

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




@pytest.mark.parametrize("attempt_number", [1, 2, 3, 4])
def test_too_high_always_costs_points(attempt_number):
    # Regression: "Too High" used to award +5 on even-numbered attempts
    assert update_score(0, "Too High", attempt_number) == -5


@pytest.mark.parametrize("attempt_number", [1, 2, 3, 4])
def test_too_low_always_costs_points(attempt_number):
    assert update_score(0, "Too Low", attempt_number) == -5
