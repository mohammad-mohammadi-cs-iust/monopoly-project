import json
import os
import random

from functions.finance import (
    save_players,
    sell_properties_to_resolve_bankrupt,
)

def normalize_position(pos):
    pos = pos % 40
    return 40 if pos == 0 else pos


JAIL_FREE_CARD = "Get Out Of Jail Free"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
players_path = os.path.join(BASE_DIR, "user", "players.json")


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


def is_player_in_prison(player):
    return player.get("prison", 0) > 0


def get_free_from_jail_card(players, player, index):
    player["prison"] = 0
    if JAIL_FREE_CARD in player.get("assets", []):
        player["assets"].remove(JAIL_FREE_CARD)
    players[index] = player
    save_players(players)
    print("✅ You used a Get Out of Jail Free card.")
    return True


def try_to_get_double(players, player, index):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)

    print(f"🎲 Dice rolled: {dice1} and {dice2}")

    if dice1 == dice2:
        player["prison"] = 0
        player["position"] = normalize_position(player["position"] + dice1 + dice2)
        players[index] = player
        save_players(players)
        print("🎉 Double rolled! You are free from jail.")
        return dice1, dice2

    return None


def fifty_dollar_to_pay():
    players, player, index = get_current_player()

    if player["money"] < 50:
        result = sell_properties_to_resolve_bankrupt(players, player, index, 50)
        if not result:
            return False

        players, player, index = get_current_player()

    player["money"] -= 50
    player["prison"] = 0
    players[index] = player
    save_players(players)
    print("💵 You paid $50 and got free from jail.")
    return True


def manage_prison():
    players, player, index = get_current_player()
    if not players:
        return "error"

    if not is_player_in_prison(player):
        return "free"

    print(f"\n🚔 Jail turn {player['prison']}")


    if player["prison"] >= 3:
        print("⛔ 3 turns passed. You must pay $50.")
        if fifty_dollar_to_pay():
            return "paid"
        return "bankrupt"

    options = []

    if JAIL_FREE_CARD in player.get("assets", []):
        options.append("Use Get Out of Jail Free card")

    options.append("Try for doubles")
    options.append("Pay $50")

    print("\nOptions:")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")

    while True:
        choice = input("Choose option: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            choice = options[int(choice) - 1]
            break

    if choice == "Use Get Out of Jail Free card":
        get_free_from_jail_card(players, player, index)
        return "freed"

    if choice == "Try for doubles":
        result = try_to_get_double(players, player, index)
        if result:
            return "rolled"

    if choice == "Pay $50":
        if fifty_dollar_to_pay():
            return "paid"
        return "bankrupt"


    player["prison"] += 1
    players[index] = player
    save_players(players)
    print("❌ Still in jail.")
    return "stay"
