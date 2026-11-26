import csv

class Player:
    def __init__(self, id: int, name: str, team: str, position: str, salary: int, overall: int, protected: bool):
        self.id = id
        self.name = name
        self.team = team
        self.position = position
        self.salary = salary
        self.overall = overall
        self.protected = protected

    def __str__(self):
        return f"ID: {self.id:3} | {self.name:25} | {self.position:2} | {self.team:25} | OVR: {self.overall} | ${self.salary} million"
    
    def is_eligible(self):
        return not self.protected

class ExpansionTeam:

    def __init__(self, name, salary_cap = 150):
        self.name = name
        self.roster = []
        self.salary_cap = salary_cap

    def __str__(self):
        return f"{self.name} has {len(self.roster)} players"

    def remaining_budget(self):
        payroll = 0

        for player in self.roster:
            payroll+=player.salary

        return self.salary_cap - payroll

    def draft_player(self, player: Player):
        if len(self.roster) >= 5:
            raise ValueError("Roster is full")
        elif not player.is_eligible():
            raise ValueError("player is protected")
        elif player.salary > self.remaining_budget():
            raise ValueError("Salary cap exceeded")
        for p in self.roster:
            if p.team == player.team:
                raise ValueError("Other player is drafted from the same team")
        self.roster.append(player)

    def display_roster(self):
        if not self.roster:
            return

        print(f"\n========== {self.name.upper()} ==========")
        print(f"Roster: {len(self.roster)}/5 players")
        print("------------------------------------")

        for player in self.roster:
            print(f"{player.position:3} | {player.name:25} | OVR {player.overall} | ${player.salary}M")

        average = calculate_average(self.roster)

        print("------------------------------------")
        print(f"Average rating: {average:.1f}")
        print(f"Current classification: {classify_team(average)}")
        print(f"Remaining budget: ${self.remaining_budget()}M")
        print("====================================\n")

def load_players():
    plers = []
    with open("players.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            protected_bool = True if row["protected"] == "Yes" else False
            pler = Player(
                int(row["id"]),
                row["name"],
                row["team"],
                row["position"],
                int(row["salary"]),
                int(row["overall"]),
                protected_bool
                )
            plers.append(pler)

    return plers

def calculate_average(players):
    if len(players) == 0:
        raise ValueError
    return sum(player.overall for player in players)/len(players)

# Average rating	Classification
# 85–100	Championship contender
# 80–84.99	Playoff contender
# 75–79.99	Play-in contender
# Below 75	Rebuilding team

def classify_team(average_rating):
    if average_rating < 75:
        return "Rebuilding team"
    elif average_rating<80:
        return "Play-in contender"
    elif average_rating<85:
        return "Playoff contender"
    else:
        return "Championship contender"


def show_intro():
    print("""
========================================
     NBA EXPANSION DRAFT SIMULATOR
========================================

WELCOME, GENERAL MANAGER!

The NBA is expanding, and you have been
selected to build a brand-new franchise.

YOUR MISSION:
Draft 5 players from existing NBA teams
and build the strongest roster possible.

DRAFT RULES:
- 30 NBA teams, 5 listed players each.
- Top 3 players per team are protected.
- Only 2 players per team are draftable.
- Maximum 1 player from each NBA team.
- Maximum roster size: 5 players.
- Salary cap: $150 million.

TEAM CLASSIFICATION:
85+   : Championship contender
80-84 : Playoff contender
75-79 : Play-in contender
<75   : Rebuilding team

COMMANDS:
PG, SG, SF, PF, C : Filter by position
ALL               : Show every position
R                 : Restart the draft
Q                 : Quit the game

========================================
         LET THE DRAFT BEGIN!
========================================
""")

def main():

    players_display = load_players()

    show_intro()

    while True:
        new_team = ExpansionTeam(input("Expansion team name: "))

        while len(new_team.roster)<5:
            try:
                position = input("Choose position: PG, SG, SF, PF, C, ALL, R (restart) or Q (quit): ").strip().upper()
                if position == "Q":
                    print("Thanks for playing")
                    return
                if position == "R":
                    print("Restarting draft...")
                    break
                valid_positions = ["PG", "SG", "SF", "PF", "C", "ALL"]
                if position not in valid_positions:
                    raise ValueError("Invalid position. Choose PG, SG, SF, PF, C or ALL.") 
                print("\nAvailable players:")

                for player in players_display:
                    used_team = any(
                        drafted.team == player.team
                        for drafted in new_team.roster
                    )
                    if player.is_eligible() and not used_team:
                        if position =="ALL" or player.position == position:
                            print(player)
                            
                player_id = int(input("Enter a player's id to draft them: "))

                for player in players_display:
                    if player.id == player_id:
                        if position != "ALL" and player.position!=position:
                            raise ValueError("Player does not match the selected position")
                        new_team.draft_player(player)
                        break
                else:
                    raise ValueError("Player ID not found")
                new_team.display_roster()

            except ValueError as error:
                print(f"Cannot draft player: {error}")

        if len(new_team.roster) != 5:
            continue

        average = calculate_average(new_team.roster)
        print("\n========== DRAFT COMPLETE ==========")
        print(f"team: {new_team.name}")
        print(f"Average rating: {average:.1f}")
        print(f"Classification: {classify_team(average)}")
        print(f"Total salary: ${new_team.salary_cap - new_team.remaining_budget()}M")
        print(f"Remaining budget: ${new_team.remaining_budget()}M")
        print("====================================")

        while True:
            play_again = input("Start another expansion draft? (Y/N): ").strip().upper()

            if play_again == "Y":
                break
            elif play_again == "N":
                print("Thanks for playing!")
                return
            else:
                print("Invalid choice. Please enter Y or N.")

if __name__ == "__main__":
    main()      