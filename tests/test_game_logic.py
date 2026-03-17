from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

# --- check_guess ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_guess_by_one_above():
    # Edge case: guess is just 1 above the secret
    assert check_guess(51, 50) == "Too High"

def test_guess_by_one_below():
    # Edge case: guess is just 1 below the secret
    assert check_guess(49, 50) == "Too Low"

def test_winning_guess_at_boundary_low():
    # Win at the lowest possible value
    assert check_guess(1, 1) == "Win"

def test_winning_guess_at_boundary_high():
    # Win at the highest possible value
    assert check_guess(100, 100) == "Win"


# --- get_range_for_difficulty ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100

def test_unknown_difficulty_defaults():
    # Unknown difficulty should fall back to the widest range
    low, high = get_range_for_difficulty("Impossible")
    assert low == 1
    assert high == 100


# --- parse_guess ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_none_input():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_float_string():
    # Float strings should be truncated to int
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None


# --- update_score ---

def test_score_win_first_attempt():
    # Win on attempt 1 should give maximum points (100)
    result = update_score(0, "Win", 1)
    assert result == 100

def test_score_win_second_attempt():
    # Win on attempt 2: 100 - 10*(2-1) = 90
    result = update_score(0, "Win", 2)
    assert result == 90

def test_score_win_minimum_points():
    # Win on attempt 10: 100 - 10*9 = 10 (minimum)
    result = update_score(0, "Win", 10)
    assert result == 10

def test_score_win_floors_at_10():
    # Win on attempt 20 would be negative, but floors at 10
    result = update_score(0, "Win", 20)
    assert result == 10

def test_score_too_low_deducts():
    # Too Low always deducts 5
    result = update_score(50, "Too Low", 3)
    assert result == 45

def test_score_unchanged_on_unknown_outcome():
    # Unknown outcome should not change the score
    result = update_score(50, "Unknown", 1)
    assert result == 50
