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
    players, player, player_index = get_current_player()
    assets = load_assets()

    username = player["username"]
    print("\nHere are your assets that you can sell:\n")

    user_assets = {}
    name_to_position = {}

    for position, asset in assets.items():
        if asset.get("owner") == username and "buy_price" in asset:
            buy_price = asset["buy_price"]
            sell_price = buy_price // 2

            user_assets[asset["name"]] = sell_price
            name_to_position[asset["name"]] = position

            print(
                f"- Position {position} | {asset['name']} | "
                f"Buy price: {buy_price}$ | Sell price: {sell_price}$"
            )

    if not user_assets:
        print("You don't own any assets to sell.")
        return

    while True:
        print(f"\nCurrent Money: {player['money']}$")
        prompt = input("Which one do you want to sell?: ").strip()

        if prompt not in user_assets:
            print("The property you typed is not in your assets. Please try again.")
            continue

        player["money"] += user_assets[prompt]

        if prompt in player["assets"]:
            player["assets"].remove(prompt)

        position = name_to_position[prompt]
        assets[position]["owner"] = ""

        if "house_num" in assets[position]:
            assets[position]["house_num"] = 0
        if "hotel_num" in assets[position]:
            assets[position]["hotel_num"] = 0


        players[player_index] = player
        save_players(players)
        save_assets(assets)

        print(f"\n✔ You sold {prompt} for {user_assets[prompt]}$")

        del user_assets[prompt]
        del name_to_position[prompt]

        if not user_assets:
            print("You have no more assets to sell.")
            break
        
        print(f"\n💰 Current money: {player['money']}$")

        while True:
            answer=input("Do you want to continue (yes/no):").strip().lower()

            if(answer=='yes' or answer=='no'):
                break
            else:
                continue
        
        if(answer=="no"):
            break

        else:
            continue


def resolve_bankrupt(position , dice):
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

    if not owner:
        return

    rent = 0

    if "rent" in current_asset:
        house_num = current_asset.get("house_num", 0)
        hotel_num= current_asset.get("hotel_num", 0)

        if(hotel_num==1 and house_num==0):
           rent = current_asset["rent"][-1]

        else:
            rent = current_asset["rent"][house_num]

    elif "RailRoad" in current_asset["name"]:
        railroad_count = 0
        for asset in assets.values():
            if asset.get("owner") == owner_name and "RailRoad" in asset.get("name"):
                railroad_count += 1
        rent = railroad_count * 25

    elif current_asset["name"] in ("Water Works", "Electric Company"):
        utility_count = 0

        for asset in assets.values():
            if asset.get("owner") == owner_name and asset.get("name") in ("Water Works", "Electric Company"):
                utility_count += 1
        
        if(utility_count==1):
           rent = dice*4
        
        elif(utility_count==2):
            rent=dice*10


    print(f"\n💸 Rent required: {rent}$")


    while player["money"] < rent:
        print(f"\nYou need {rent}$ to pay rent but you have only {player['money']}$.\nConsider selling properties.")
        sell_properties()

        players, player, player_index = get_current_player()

        if player["money"] >= rent:
            print(f"\n💰 You now have enough money ({player['money']}$) to pay the rent.")
            break

        if player["money"] < rent:
            print("\n❌ You still cannot pay the rent.")
            break



    if player["money"] < rent:
        print(f"\n☠ {player['username']} is BANKRUPT!")

        for asset in assets.values():
            if asset.get("owner") == player["username"]:
                asset["owner"] = owner_name

        player["money"] = 0
        player["status"] = "Bankrupt"
        player["assets"] = []
        players[player_index] = player
        save_players(players)
        save_assets(assets)
        return

    player["money"] -= rent
    owner["money"] += rent

    players[player_index] = player
    players[owner_index] = owner

    save_players(players)

    print(f"\n✅ {player['username']} paid {rent}$ rent to {owner_name}")
    print(f"💰 Your new balance: {player['money']}$")
