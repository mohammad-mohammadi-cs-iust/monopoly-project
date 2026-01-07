import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
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
    players, player, player_index = get_current_player()
    assets = load_assets()

    player_backup = player.copy()
    assets_backup = {k: v.copy() for k, v in assets.items()}

    username = player["username"]
    user_assets = {}

    for position, asset in assets.items():
        if asset.get("owner") == username and "buy_price" in asset:
            buy_price = asset["buy_price"]
            house_num = asset.get("house_num", 0)
            hotel_num = asset.get("hotel_num", 0)
            house_creating = asset.get("house_creating", 0)
            hotel_creating = asset.get("hotel_creating", 0)
            total_spent = buy_price + (house_num * house_creating) + (hotel_num * hotel_creating)
            sell_price = total_spent // 2
            user_assets[str(position)] = sell_price

            if house_num or hotel_num:
                print(f"- Position {position} | {asset['name']} | House num: {house_num} | Hotel num: {hotel_num} | Buy price: {buy_price}$ | Sell price: {sell_price}$")
            else:
                print(f"- Position {position} | {asset['name']} | Buy price: {buy_price}$ | Sell price: {sell_price}$")

    if not user_assets:
        print("You don't own any assets to sell.")
        return

    while user_assets:
        print(f"\nCurrent Money: {player['money']}$")
        print("Type 'cancel' if you don't want to sell anything.")
        prompt = input("Which one do you want to sell? Type its position: ").strip()

        if prompt.lower() == "cancel":
            print("✔ You chose not to sell any assets.")
            players[player_index] = player_backup
            save_players(players)
            save_assets(assets_backup)
            return

        if prompt not in user_assets:
            print("The position you typed is not in your assets. Please try again.")
            continue

        player["money"] += user_assets[prompt]
        if assets[prompt]["name"] in player["assets"]:
            player["assets"].remove(assets[prompt]["name"])
        assets[prompt]["owner"] = ""
        assets[prompt]["house_num"] = 0
        assets[prompt]["hotel_num"] = 0

        players[player_index] = player
        save_players(players)
        save_assets(assets)

        print(f"\n✔ You sold {assets[prompt]['name']} for {user_assets[prompt]}$")

        del user_assets[prompt]

        if not user_assets:
            print("You have no more assets to sell.")
            break

        print(f"\n💰 Current money: {player['money']}$")

        while True:
            answer = input("Do you want to continue selling (yes/no)? ").strip().lower()
            if answer in ("yes", "no"):
                break
        if answer == "no":
            break





def sell_properties_to_resolve_bankrupt(players, player, player_index,debt):
    assets = load_assets()
    username = player["username"]

    user_assets = {}
    total_value = 0

    for position, asset in assets.items():
        if asset.get("owner") == username and "buy_price" in asset:
            sell_price = asset["buy_price"] // 2
            house = asset.get("house_num", 0)
            hotel = asset.get("hotel_num", 0)

            sell_price += (house * asset.get("house_creating", 0)) // 2
            sell_price += (hotel * asset.get("hotel_creating", 0)) // 2

            total_value += sell_price
            user_assets[str(position)] = sell_price

    if total_value + player["money"] < debt:
        print("❌ You cannot pay the debt even if you sell all assets. BANKRUPT!")

        player["money"] = 0
        player["status"] = "Bankrupt"
        player["assets"] = []

        for asset in assets.values():
            if asset.get("owner") == username:
                asset["owner"] = ""
                asset["house_num"] = 0
                asset["hotel_num"] = 0

        players[player_index] = player
        save_players(players)
        save_assets(assets)
        
        return False

    if not user_assets:
        print("❌ No assets left to sell.")
        return False

    while player["money"] < debt and user_assets:
        print(f"\n💰 Current money: {player['money']}$ | Debt: {debt}$")
        print("Your sellable assets:")
        for pos, price in user_assets.items():
            print(f"- Position {pos} | Sell price: {price}$ | Name: {assets[pos]['name']}")

        prompt = input("Which asset to sell? Type position or 'cancel': ").strip()

        if prompt.lower() == "cancel":
            print("❌ You chose not to sell any assets.")
            return False

        if prompt not in user_assets:
            print("❌ Invalid position. Try again.")
            continue


        sold_price = user_assets[prompt]
        player["money"] += sold_price

        if assets[prompt]["name"] in player.get("assets", []):
            player["assets"].remove(assets[prompt]["name"])
        assets[prompt]["owner"] = ""
        assets[prompt]["house_num"] = 0
        assets[prompt]["hotel_num"] = 0

        del user_assets[prompt]

        players[player_index] = player
        save_players(players)


        save_assets(assets)
        print(f"✔ Sold {assets[prompt]['name']} for {sold_price}$")

    players[player_index]=player

    save_players(players)

    return player["money"] >= debt



def resolve_bankrupt(position, dice):
    players, player, player_index = get_current_player()
    assets = load_assets()

    current_asset = assets.get(str(position))
    if not current_asset or "owner" not in current_asset:
        return

    owner_name = current_asset.get("owner")
    if owner_name == "" or owner_name == player["username"]:
        return

    owner = None
    owner_index = None
    for i in range(2, len(players)):
        if players[i]["username"] == owner_name:
            owner = players[i]
            owner_index = i
            break

    rent = 0

    if "rent" in current_asset:
        house_num = current_asset.get("house_num", 0)
        hotel_num = current_asset.get("hotel_num", 0)
        rent = current_asset["rent"][-1] if hotel_num else current_asset["rent"][house_num]
    elif "RailRoad" in current_asset["name"]:
        rent = sum(1 for a in assets.values() if a.get("owner") == owner_name and "RailRoad" in a.get("name")) * 25
    elif "Tax" in current_asset["name"]:
        rent = 200 if "Income Tax" in current_asset["name"] else 100
    elif current_asset["name"] in ("Water Works", "Electric Company"):
        utility_count = sum(1 for a in assets.values() if a.get("owner") == owner_name and a.get("name") in ("Water Works", "Electric Company"))
        rent = dice * 4 if utility_count == 1 else dice * 10

    print(f"\n💸 Rent/Tax to pay: {rent}$")


    if player["money"] < rent:
        print(f"⚠ You need {rent}$ but have only {player['money']}$")
        result = sell_properties_to_resolve_bankrupt(players,player,player_index,rent)
        if not result:

            print(f"\n☠ {player['username']} is BANKRUPT!")
            for asset in assets.values():
                if asset.get("owner") == player["username"]:
                    asset["owner"] = owner_name if owner_name else ""
                    asset["house_num"] = 0
                    asset["hotel_num"] = 0
            if owner:
                owner["money"] += player["money"]
                players[owner_index] = owner
            player["money"] = 0
            player["status"] = "Bankrupt"
            player["assets"] = []
            players[player_index] = player
            save_players(players)
            save_assets(assets)
            return


    player["money"] -= rent
    if owner:
        owner["money"] += rent
        players[owner_index] = owner

    players[player_index] = player
    save_players(players)
    save_assets(assets)

    if owner:
        print(f"✅ {player['username']} paid {rent}$ rent to {owner['username']}")
    else:
        print(f"✅ {player['username']} paid {rent}$ tax")

    print(f"💰 New balance: {player['money']}$")
