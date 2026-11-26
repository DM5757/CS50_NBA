# NBA Expansion Draft Simulator

#### Video Demo: https://youtu.be/GYcshMyj_Vw

## Description

For my CS50P final project, I created an NBA Expansion Draft Simulator using Python. The idea is to become the general manager of a new NBA franchise and build a five-player roster by drafting players from existing teams.

I chose this project because I enjoy basketball and wanted to practice object-oriented programming (OOP).

The simulator includes 150 players from 30 NBA teams. Each team has five listed players, but the three highest-rated are protected. This leaves 60 players available to draft.

The user has a fictional $150 million salary cap and can only select one player from each NBA team. Players can be filtered by position and drafted using their IDs.

After each pick, the program displays the current roster, average rating, team classification, and remaining budget. Once five players are selected, the team is evaluated as a Rebuilding team, Play-in contender, Playoff contender, or Championship contender. Users can also restart or quit the game.

## Project Files

**project.py**

This is the main file containing the simulator. It uses two classes: `Player`, which stores player information and checks eligibility, and `ExpansionTeam`, which manages the roster, salary cap, and drafting rules.

It also includes functions for loading players, calculating average ratings, classifying teams, and running the game.

**get_players.py**

This script uses NBA2KAPI to collect player information, assign fictional salaries based on overall ratings, and mark the top three players from each team as protected. It generates the dataset used by the simulator.

**players.csv**

Contains the 150 players, including their names, teams, positions, overall ratings, salaries, and protection status.

**test_project.py**

Contains nine pytest tests covering calculations, CSV loading, and drafting restrictions such as protected players, duplicate teams, salary caps, and roster limits.

## Design Choices

I used OOP to separate player information from team management and keep the drafting rules organized.

I chose CSV storage instead of making API requests during gameplay. This allows the simulator to run offline without an API key.

The salary cap and team classifications are fictional and were added to make drafting more interesting without making the project too complicated.

## How to Run

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the simulator:

```bash
python project.py
```

Run the tests:

```bash
python -m pytest test_project.py
```

## API Key

The `get_players.py` script requires an NBA2KAPI key to generate or update the dataset. Create a `.env` file in the project directory containing:

```text
NBA2K_API_KEY=your_api_key_here
```

The API key is not required to run `project.py`, since the player data is already stored in `players.csv`.