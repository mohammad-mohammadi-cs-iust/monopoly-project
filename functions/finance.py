import os
import json

BASE_DIR = os.path.dirname(__file__)
players_path = os.path.join(BASE_DIR, "user", "players.json")
assets_path = os.path.join(BASE_DIR, "asset", "assets.json")

def load_players():
    with open(players_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_players(players):
    with open(players_path, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=4)


def load_assets():
    with open(assets_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_assets(assets):
    with open(assets_path, "w", encoding="utf-8") as f:
        json.dump(assets, f, indent=4)


def get_current_player():
    players = load_players()
    current_turn = players[1]["current_turn"]

    for i in range(2, len(players)):
        if players[i]["player_number"] == current_turn:
            return players, players[i], i

    return None, None, None


def sell_properties():
    players, player, _ = get_current_player()
    assets = load_assets()

    username = player["username"]

    print("\nHere are your assets that you can sell:\n")

    has_any_asset = False

    for position, asset in assets.items():

        if asset.get("owner") == username and "buy_price" in asset:

            buy_price = asset["buy_price"]
            sell_price = buy_price // 2

            print(f"- Position {position} | {asset['name']} | "
                  f"Buy price: {buy_price}$ | Sell price: {sell_price}$")

            has_any_asset = True

    if not has_any_asset:
        print("You don't own any assets to sell.")
