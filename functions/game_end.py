import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLAYERS_FILE = os.path.join(BASE_DIR, "user", "players.json")
ASSETS_FILE = os.path.join(BASE_DIR, "asset", "assets.json")
SCOREBOARD_FILE = os.path.join(BASE_DIR, "user", "scoreboard.json")


def load_json(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def reset_assets():
    assets = load_json(ASSETS_FILE, {})
    if not isinstance(assets, dict):
        return

    for asset in assets.values():
        if "owner" in asset:
            asset["owner"] = ""
        if "house_num" in asset:
            asset["house_num"] = 0
        if "hotel_num" in asset:
            asset["hotel_num"] = 0

    save_json(ASSETS_FILE, assets)


def calculate_player_value(player, assets_data):
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


def end_game_if_finished():
    data = load_json(PLAYERS_FILE, ["In Progress", {"current_turn": 1}])
    if not isinstance(data, list) or len(data) < 3:
        return

    players_list = data[2:]
    active_players = [p for p in players_list if p.get("status") != "Bankrupt"]

    if len(active_players) == 1:
        winner = active_players[0]

        for player in players_list:
            player["status"] = "Won" if player is winner else "Bankrupt"

        assets_data = load_json(ASSETS_FILE, {})

        for player in players_list:
            total_value, land_count, cash = calculate_player_value(player, assets_data)
            player["total_value"] = total_value
            player["land_count"] = land_count
            player["cash"] = cash

        players_list.sort(
            key=lambda p: (p["total_value"], p["land_count"], p["cash"]),
            reverse=True
        )

        for idx, player in enumerate(players_list, 1):
            player["rank"] = idx

        final_data = ["Over"] + players_list

        scoreboard_data = load_json(SCOREBOARD_FILE, [])
        scoreboard_data.append(final_data)

        save_json(SCOREBOARD_FILE, scoreboard_data)
        save_json(PLAYERS_FILE, [])

        reset_assets()

        return "Game ended successfully. Returning to the menu...."


def show_leaderboard(game_index=-1):
    scoreboard_data = load_json(SCOREBOARD_FILE, [])
    if not scoreboard_data:
        print("No finished games found.")
        return

    game_data = scoreboard_data[game_index]
    if game_data[0] != "Over":
        print("This game has not ended yet.")
        return

    print("\n======================= Monopoly Leaderboard =======================\n")
    for player in game_data[1:]:
        print(
            f"Rank: {player['rank']} | Username: {player['username']} | "
            f"Cash: {player['cash']}$ | Lands: {player['land_count']} | "
            f"Status: {player['status']} | Total Value: {player['total_value']}$"
        )
    print("\n====================================================================\n")
