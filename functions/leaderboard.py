import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLAYERS_FILE = os.path.join(BASE_DIR, "user", "players.json")
ASSETS_FILE = os.path.join(BASE_DIR, "asset", "assets.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "user", "leaderboard.json")


def load_players():
    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_assets():
    with open(ASSETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_player_score(player, assets_data):
    total_cash = player.get("money", 0)
    total_assets_value = 0
    land_count = 0
    for asset_key in player.get("assets", []):
        asset = assets_data.get(str(asset_key))
        if asset and "color" in asset:
            total_assets_value += asset.get("buy_price", 0)
            land_count += 1
    total_value = total_cash + total_assets_value
    return total_value, land_count, total_cash


def build_leaderboard():
    players = load_players()
    assets_data = load_assets()
    leaderboard = []
    for player in players:
        if not isinstance(player, dict) or "username" not in player:
            continue
        total_value, land_count, cash = calculate_player_score(player, assets_data)
        leaderboard.append({
            "username": player["username"],
            "total_value": total_value,
            "land_count": land_count,
            "cash": cash,
            "status": player.get("status", "In Progress")
        })
    leaderboard.sort(key=lambda x: (x["total_value"], x["land_count"], x["cash"]), reverse=True)
    for idx, player in enumerate(leaderboard, 1):
        player["rank"] = idx
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=4)
    return leaderboard


def run_leaderboard():
    leaderboard = build_leaderboard()
    print("\n======================= Monopoly Leaderboard =======================\n")
    for player in leaderboard:
        print(f"Rank: {player['rank']} | Username: {player['username']} | Cash: {player['cash']}$ | "
              f"Lands: {player['land_count']} | Status: {player['status']} | Total Value: {player['total_value']}$")
