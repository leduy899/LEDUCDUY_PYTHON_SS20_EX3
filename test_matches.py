import pytest
from main import determine_winner

def test_team_a_wins():
    match = {
        "match_id": "M01",
        "team_a": "T1",
        "team_b": "GenG",
        "score_a": 2,
        "score_b": 0,
        "status": "Completed"
    }
    assert determine_winner(match) == "T1"

def test_draw():
    match = {
        "match_id": "M02",
        "team_a": "JDG",
        "team_b": "BLG",
        "score_a": 1,
        "score_b": 1,
        "status": "Completed"
    }
    assert determine_winner(match) == "Draw"

def test_pending():
    match = {
        "match_id": "M03",
        "team_a": "G2",
        "team_b": "FNC",
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
    assert determine_winner(match) == "Not Started"
    
def test_key_error():
    """Test case (Bonus): Bẫy lỗi dữ liệu bị thiếu key"""
    match_missing_score = {
        "match_id": "M04",
        "team_a": "DK",
        "team_b": "KT",
        "status": "Completed"
    }
    assert determine_winner(match_missing_score) == "Data Error"
