import os
import json


BASE_DIR = os.path.dirname(__file__)
PLAYERS_FILE = os.path.join(BASE_DIR, "user", "players.json")
SCOREBOARD_FILE = os.path.join(BASE_DIR, "asset", "scoreboard.json")


def load_json(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def end_game_if_finished():
    data = load_json(PLAYERS_FILE, ["In Progress", {"current_turn": 1}])

    if not isinstance(data, list) or len(data) < 3:
        return

    players_list = data[2:]

    active_players = [
        p for p in players_list
        if p.get("status") != "Bankrupt"
    ]

    
    if len(active_players) == 1:
        winner = active_players[0]

        for player in players_list:
            if player is winner:
                player["status"] = "Won"
            else:
                player["status"] = "Bankrupt"

        data[0] = "Over"

        
        data.pop(1)

        scoreboard_data = load_json(SCOREBOARD_FILE, [])
        scoreboard_data.append(data)

        save_json(SCOREBOARD_FILE, scoreboard_data)

        
        save_json(PLAYERS_FILE, [])

        return("Game ended successfully. Returning to the menu....")
