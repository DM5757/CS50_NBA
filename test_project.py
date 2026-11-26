import pytest
from project import(
    Player,
    ExpansionTeam,
    load_players,
    calculate_average,
    classify_team
)



def test_classify_team():
    assert classify_team(70) == "Rebuilding team"
    assert classify_team(77) == "Play-in contender"
    assert classify_team(83) == "Playoff contender"
    assert classify_team(95) == "Championship contender"
    assert classify_team(75) == "Play-in contender"
    assert classify_team(80) == "Playoff contender"
    assert classify_team(85) == "Championship contender"

def test_calculate_average():
    players = [
        Player(1, "Player A", "Team A", "PG", 20, 80, False),
        Player(2, "Player B", "Team B", "SG", 30, 90, False),
        Player(3, "Player C", "Team C", "SF", 12, 70, False)
    ]
    assert calculate_average(players) == 80

def test_calculate_average_empty():
    with pytest.raises(ValueError):
        calculate_average([])

def test_load_players():
    players = load_players()
    assert len(players) == 150
    assert all(isinstance(player, Player) for player in players)
    assert sum(player.is_eligible() for player in players) == 60

def test_draft_player():
    team = ExpansionTeam("Test Franchise")

    player = Player(1, "Player A", "Team A", "PG", 20, 85, False)

    team.draft_player(player)

    assert len(team.roster) == 1
    assert team.remaining_budget() == 130

def test_protected_player():
    team = ExpansionTeam("Test Franchise")
    player = Player(1, "Player A", "Team A", "PG", 20, 85, True)

    with pytest.raises(ValueError):
        team.draft_player(player)

    assert len(team.roster) == 0

def test_team_duplicate():
    team = ExpansionTeam("Test Franchise")
    player1 = Player(1, "Player A", "Team A", "PG", 20, 85, False)
    player2 = Player(2, "Player B", "Team A", "SG", 12, 78, False)
    team.draft_player(player1)

    with pytest.raises(ValueError):
        team.draft_player(player2)
    
    assert len(team.roster) == 1

def test_salary_cap():
    team = ExpansionTeam("Test Franchise", 10)
    player = Player(1, "Player A", "Team A", "PG", 20, 85, False)

    with pytest.raises(ValueError):
        team.draft_player(player)

    assert len(team.roster) == 0
    
def test_roster_limits():
    team = ExpansionTeam("Test Franchise")
    player1 = Player(1, "Player A", "Team A", "PG", 20, 85, False)
    player2 = Player(2, "Player B", "Team B", "SF", 12, 76, False)
    player3 = Player(3, "Player C", "Team C", "C", 20, 85, False)
    player4 = Player(4, "Player D", "Team D", "SG", 12, 78, False)
    player5 = Player(5, "Player E", "Team E", "PF", 12, 77, False)
    player6 = Player(6, "Player F", "Team F", "C", 12, 76, False)

    team.draft_player(player1)
    team.draft_player(player2)
    team.draft_player(player3)
    team.draft_player(player4)
    team.draft_player(player5)

    with pytest.raises(ValueError):
        team.draft_player(player6)
    assert len(team.roster) == 5