import json
import os
import random
from functions.finance import save_players, sell_properties_to_resolve_bankrupt, load_assets, save_assets

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
players_path = os.path.join(BASE_DIR, "user", "players.json")
assets_path = os.path.join(BASE_DIR, "asset", "assets.json")

def load_players():
    with open(players_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_current_player():
    players = load_players()
    current_turn = players[1]["current_turn"]
    for i in range(2, len(players)):
        if players[i]["player_number"] == current_turn:
            return players, players[i], i
    return None, None, None

def is_player_in_prison():
    players, player, index = get_current_player()
    return player['prison'] != 0

def get_free_from_jail_card(players, player, index):
    player['prison'] = 0
    if "get_out_of_jail" in player['assets']:
        player['assets'].remove("get_out_of_jail")
    players[index] = player
    save_players(players)
    print("You successfully got free from prison. Now roll the dice to continue.")

def try_to_get_double(players, player, index):
    for attempt in range(1, 4):
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        print(f"\n-----Attempt {attempt}-----")
        print(f"Dice rolled: {dice1} and {dice2}")
        if dice1 == dice2:
            player['prison'] = 0
            players[index] = player
            save_players(players)
            print("You successfully got free from prison.")
            print(f"Move forward by {dice1 + dice2} steps.")
            return dice1, dice2
    print("Failed to get doubles. Remain in prison for next turn.")
    return None

def fifty_dollar_to_pay(players, player, index):
    if player['money'] < 50:
        sell_properties_to_resolve_bankrupt(50)
    if player['money'] >= 50:
        player['money'] -= 50
        player['prison'] = 0
        players[index] = player
        save_players(players)
        print("You successfully paid $50 and got free from prison. Now roll the dice.")
    else:
        print(f"\n☠ {player['username']} is BANKRUPT!")
        assets = load_assets()
        for asset in assets.values():
            if asset.get("owner") == player["username"]:
                asset["owner"] = ""
            if asset.get("house_num") or asset.get("hotel_num"):
                asset['house_num'] = 0
                asset['hotel_num'] = 0
        player["money"] = 0
        player["status"] = "Bankrupt"
        player["assets"] = []
        players[index] = player
        save_players(players)
        save_assets(assets)

def manage_prison():
    players, player, index = get_current_player()
    if not is_player_in_prison():
        print("You are not in prison.")
        return

    print(f"This is turn {player['prison']} that you are in prison.")
    if player['prison'] == 3:
        print("The only way to get out of prison is to pay $50 and roll the dice.")
        fifty_dollar_to_pay(players, player, index)
        return

    choices = []
    if "get_out_of_jail" in player['assets']:
        choices.append("Use Get out of Jail card")
    choices.append("Try for doubles")
    choices.append("Pay $50")

    print("\nOptions to get free from jail:")
    for i, option in enumerate(choices, 1):
        print(f"{i}. {option}")

    while True:
        prompt = input("Choose an option (number): ").strip()
        if prompt.isdigit():
            prompt = int(prompt)
            if 1 <= prompt <= len(choices):
                break
        print("Invalid input. Enter a valid number.")

    choice = choices[prompt - 1]
    if choice == "Use Get out of Jail card":
        get_free_from_jail_card(players, player, index)
    elif choice == "Try for doubles":
        result = try_to_get_double(players, player, index)
        if result:
            dice1, dice2 = result
            player['position'] = (player['position'] + dice1 + dice2) % 40
            players[index] = player
            save_players(players)
    elif choice == "Pay $50":
        fifty_dollar_to_pay(players, player, index)

    if player['prison'] == 0:
        print("You are now free from prison. Continue your turn.")

    players[index] = player
    save_players(players)
