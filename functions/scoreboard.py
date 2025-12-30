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

def calculate_total_asset_value(player, assets):
    total_value = 0
    for asset in assets.values():
        if asset.get("owner") == player["username"]:
            total_value += asset.get("price", 0)  
    return total_value

def build_scoreboard():
    players = load_players()
    assets = load_assets()

    scoreboard = []
    for player in players:
        
        if not isinstance(player, dict) or "username" not in player:
            continue  

        asset_value = calculate_total_asset_value(player, assets)
        total_value = player["money"] + asset_value
        num_assets = sum(1 for a in assets.values() if a.get("owner") == player["username"])

        scoreboard.append({
            "username": player["username"],
            "total_value": total_value,
            "num_assets": num_assets,
            "money": player["money"]
        })

    scoreboard.sort(key=lambda x: (-x["total_value"], -x["num_assets"], -x["money"]))

    return scoreboard

if __name__ == "__main__":
    scoreboard = build_scoreboard()
    print("===== Monopoly Scoreboard =====")
    for i, player in enumerate(scoreboard, 1):
        print(f"{i}. {player['username']} - Total Value: {player['total_value']} | Assets: {player['num_assets']} | Cash: {player['money']}")
