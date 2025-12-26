import json
import os

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


def next_turn():
    players = load_players()
    total_players = len(players) - 2

    current = players[1]["current_turn"]
    current += 1
    if current > total_players:
        current = 1

    players[1]["current_turn"] = current
    save_players(players)


def get_current_block(player):
    assets = load_assets()
    return assets.get(str(player["position"]))



def ownership():
    players, player, index = get_current_player()
    assets = load_assets()

    pos = str(player["position"])
    block = assets.get(pos)


    if "buy_price" not in block:
        print("This block cannot be purchased.")
        return


    if block["owner"]==player["username"]:
        print(f"{block['name']} is one of your Properties.")
        return
    

    if block["owner"] is not None and block["owner"] != player["username"]:
        print(f"{block['name']} belongs to {block['owner']}.")
        return


    if player["money"] < block["buy_price"]:
        print(f"Your Money is not enough to Purchase {block['name']}")
        return
    

    while True:
        choice = input(f"\n{player['username']} buy {block['name']} for {block['buy_price']}? (yes/no): ").lower()

        if(choice=="no" or choice=="yes"):
            break

        else:
            continue

    if choice == "yes":
        player["money"] -= block["buy_price"]
        player["assets"].append(pos)
        block["owner"] = player["username"]

        players[index] = player
        assets[pos] = block

        save_players(players)
        save_assets(assets)
        print(f"{block['name']} bought by {player['username']} ✔")

    else:
        pass



