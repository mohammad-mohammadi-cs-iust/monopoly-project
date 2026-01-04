import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLAYERS_FILE = os.path.join(BASE_DIR, "user", "players.json")
ASSETS_FILE = os.path.join(BASE_DIR, "asset", "assets.json")

def load_players():
    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_assets():
    with open(ASSETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_scoreboard():
    players = load_players()

    scoreboard = []
    for player in players:
        
        if not isinstance(player, dict) or "username" not in player:
            continue  

        assets_name = player['assets']

        assets_name=", ".join(assets_name)

        scoreboard.append({
            "username": player["username"],
            "assets_name": assets_name,
            "money": player["money"],
            "status":player['status'],
            "player_num":player['player_number'],
            "position":player['position'],
            "prison":True if player['prison'] > 0 else False
        })

    current_player=[]

    for item in scoreboard:
        if(players[1]['current_turn']==item['player_num']):
           current_player.append(item)
           scoreboard.remove(item)

    return scoreboard,current_player

def run_scoreboard():
    scoreboard,current_player = build_scoreboard()
    print("\n========================== Monopoly Scoreboard ======================\n")
    for i, player in enumerate(scoreboard, 1):
            print(f"{i}. Username: {player['username']} | Cash: {player['money']} | Player Position:{player['position']} | Assets: {player['assets_name']} | Status: {player['status']} | Prison Status:{player['prison']}")
    
    print("\n========================== Current Turn player ======================\n")
    for player in current_player:
        print(f"Info: Username: {player['username']} | Cash: {player['money']} | Player Position:{player['position']} | Assets: {player['assets_name']} | Status: {player['status']} | Prison Status:{player['prison']}")

run_scoreboard()