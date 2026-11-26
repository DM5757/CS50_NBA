
import requests
import csv
import os
from dotenv import load_dotenv


def get_salary(rating):
    if rating < 75:
        return 6
    elif rating <= 79:
        return 12
    elif rating <= 84:
        return 20
    elif rating <= 89:
        return 30
    else:
        return 45


load_dotenv()
api_key = os.getenv("NBA2K_API_KEY")

if not api_key:
    raise ValueError("NBA2K_API_KEY not found in .env")

headers = {
    "X-API-Key": api_key
}

# Get all current NBA teams
response = requests.get(
    "https://api.nba2kapi.com/api/teams",
    params={"teamType": "curr"},
    headers=headers,
    timeout=15
)

response.raise_for_status()
teams = response.json()["data"]

# Collect players from every team
all_players = []

for team in teams:
    team_name = team["teamName"]
    if team_name == "Free Agency":
        continue
    response = requests.get(
        "https://api.nba2kapi.com/api/players",
        params={
            "teamType": "curr",
            "team": team_name,
            "sort": "overall:desc",
            "limit": 5
        },
        headers=headers,
        timeout=15
    )

    response.raise_for_status()
    players = response.json()["data"]

    if len(players) != 5:
        raise ValueError(
            f"Expected 5 players for {team_name}, got {len(players)}"
        )

    # Top 3 are protected, bottom 2 are draftable
    for index, player in enumerate(players):
        player_info = {
            "name": player["name"],
            "team": player["team"],
            "position": player["positions"][0],
            "salary": get_salary(player["overall"]),
            "overall": player["overall"],
            "protected": "Yes" if index < 3 else "No"
        }

        all_players.append(player_info)

    print(f"Collected 5 players from {team_name}")

# Check the collected dataset
if len(all_players) != 150:
    raise ValueError(
        f"Expected 150 players, got {len(all_players)}"
    )

# Write everything to CSV
with open("players.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "id", "name", "team", "position",
        "salary", "overall", "protected"
    ]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for player_id, player in enumerate(all_players, start=1):
        row = {
            "id": player_id,
            **player
        }

        writer.writerow(row)

print(f"\nSuccessfully saved {len(all_players)} players to players.csv")
print("Protected:", sum(p["protected"] == "Yes" for p in all_players))
print("Available:", sum(p["protected"] == "No" for p in all_players))