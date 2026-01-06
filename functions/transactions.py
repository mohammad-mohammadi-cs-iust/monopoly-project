import json
import os

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

    if block is None or "buy_price" not in block or block["buy_price"] <= 0:
        print(f"{block.get('name','This block')} cannot be purchased. Move on.")
        return

    if block.get("owner") == player["username"]:
        print(f"{block['name']} is already one of your properties.")
        return

    if block.get("owner") not in (None, ""):
        print(f"{block['name']} belongs to {block['owner']}.")
        return

    if player["money"] < block["buy_price"]:
        print(f"You don't have enough money to buy {block['name']} (${block['buy_price']}).")
        return

    while True:
        choice = input(f"\nDo you want to buy {block['name']} for ${block['buy_price']}? (yes/no): ").strip().lower()
        if choice in ("yes", "no"):
            break
        print("Please type 'yes' or 'no'.")

    if choice == "yes":
        player["money"] -= block["buy_price"]
        if block['name'] not in player["assets"]:
            player["assets"].append(block['name'])
        block["owner"] = player["username"]
        players[index] = player
        assets[pos] = block
        save_players(players)
        save_assets(assets)
        print(f"\n✔ {block['name']} bought successfully by {player['username']} for ${block['buy_price']}.")
    else:
        print(f"You chose not to buy {block['name']}.")





def build_houses_and_hotels():
    players, player, index = get_current_player()
    built_this_turn = False

    def can_build_on_color(color):
        assets = load_assets()
        owned_blocks = []
        total_blocks = []
        for b in assets.values():
            if b.get("color") == color and b.get("owner") == player["username"]:
                owned_blocks.append(b)
            if b.get("color") == color:
                total_blocks.append(b)
        return len(owned_blocks) == len(total_blocks), owned_blocks

    colors = set()
    assets = load_assets()
    for m in assets.values():
        if m.get("color") and m.get("owner") == player["username"]:
            colors.add(m.get("color"))

    possible_to_build = False
    for color in colors:
        full_ownership, blocks = can_build_on_color(color)
        if full_ownership:
            possible_to_build = True
            break

    if not possible_to_build:
        print("\n❌ You cannot build houses or hotels because you don't own a complete color set.")
        return

    print("\n🏗️ Now it's your turn to build houses or hotels on your properties!")
    for color in colors:
        if built_this_turn:
            break
        full_ownership, blocks = can_build_on_color(color)
        if not full_ownership:
            continue
        print(f"\n--------Color Group: {color}---------")
        print(f"\nYou own all {color} properties. You can build houses/hotels!")
        blocks.sort(key=lambda b: b.get("house_num", 0))
        for block in blocks:
            houses = block.get("house_num", 0)
            hotel = block.get("hotel_num", 0)
            print(f"- {block['name']}: House number={houses}, Hotel number={hotel}, House price={block.get('house_creating')}, Hotel price={block.get('hotel_creating')}")

        while True:
            assets = load_assets()
            full_ownership, blocks = can_build_on_color(color)
            if not blocks:
                print("You no longer own a full color set. Cannot build.")
                break

            choice = input("Which property do you want to build on? (name/skip): ").strip()
            if choice.lower() == "skip":
                break

            selected = None
            for block in blocks:
                if block["name"].lower() == choice.lower():
                    selected = block
                    break
            if not selected:
                print("Invalid property name.")
                continue
            if selected.get("hotel_num", 0) == 1:
                print("This property already has a hotel.")
                continue

            build_choice = input("Build house or hotel? (house/hotel/skip): ").lower()
            if build_choice == "skip":
                break

            min_houses = min(block.get("house_num", 0) for block in blocks)

            if build_choice == "house":
                if selected.get("house_num", 0) >= 4:
                    print("Already 4 houses. Consider building a hotel.")
                    continue
                if selected.get("house_num", 0) > min_houses:
                    print(f"You must build houses evenly across all {color} properties.")
                    continue
                cost = selected.get("house_creating", 50)
                if player["money"] < cost:
                    print("Not enough money to build a house.")
                    break
                player["money"] -= cost
                selected["house_num"] = selected.get("house_num", 0) + 1
                assets[str(selected["position"])] = selected
                save_assets(assets)
                built_this_turn = True
                print(f"✅ Built 1 house on {selected['name']}")
                break

            elif build_choice == "hotel":
                if selected.get("house_num", 0) < 4:
                    print("You need 4 houses first to build a hotel.")
                    continue
                if selected.get("hotel_num", 0) == 1:
                    print("This property already has a hotel.")
                    continue
                cost = selected.get("hotel_creating", 200)
                if player["money"] < cost:
                    print("Not enough money to build a hotel.")
                    break
                player["money"] -= cost
                selected["hotel_num"] = 1
                selected["house_num"] = 0
                assets[str(selected["position"])] = selected
                save_assets(assets)
                built_this_turn = True
                print(f"✅ Built 1 hotel on {selected['name']}")
                break

    players[index] = player
    save_players(players)




def play_turn():
    players, player, _ = get_current_player()
    print(f"\n🎲 {player['username']}'s turn")

    ownership()
    build_houses_and_hotels()
    next_turn()