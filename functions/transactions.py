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



def build_houses_and_hotels():
    print("\nNow it's your turn to Build houses and hotels in your properties!!")
    players, player, index = get_current_player()
    assets = load_assets()

    
    def can_build_on_color(color):
        owned_blocks=[]
        total_blocks=[]

        for b in assets.values():
            if(b.get("color")==color and b.get("owner")==player["username"]):
                owned_blocks.append(b)

            if(b.get("color")==color):
                total_blocks.append(b)

        return len(owned_blocks) == len(total_blocks), owned_blocks
    
    colors=set()

    for m in assets.values():
        if(m.get("color") and m.get("owner")==player["username"]):
            colors.add(m.get("color"))
    
    for color in colors:
        full_ownership, blocks = can_build_on_color(color)

        if full_ownership:

            print(f"\n--------Color Group:{color}---------")

            print(f"\nYou own all {color} properties. You can build houses/hotels!")

            def get_houses(block):
                return block.get("house_num", 0)
            
            blocks.sort(key=get_houses)


            for block in blocks:
                houses = block.get("house_num", 0)
                hotel = block.get("hotel_num", 0)
                print(f"-{block['name']}: House number={houses}, Hotel number={hotel} ,House price={block.get('house_creating')},Hotel price={block.get('hotel_creating')}")


            while True:

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

                if selected.get("hotel_num", 0)==1:
                    print("This property already has a hotel.")
                    continue


                while True:

                    build_choice = input("Build house or hotel? (house/hotel/skip): ").lower()


                    min_houses = min(block.get("house_num", 0) for block in blocks)
                    
                    if build_choice=='house' and selected.get("house_num", 0) > min_houses:
                        print(f"\nYou must build houses evenly across all properties of {color} color.")
                        continue

                    elif build_choice in ("house", "hotel", "skip"):
                        break

                    


                    print("Please type 'house', 'hotel', or 'skip'.")


                if build_choice == "skip":
                    continue


                if build_choice == "house":

                    if selected.get("house_num", 0) < 4:

                        cost = selected.get("house_price", 50)

                        if player["money"] >= cost:

                            player["money"] -= cost

                            selected["house_num"] = selected.get("house_num", 0) + 1

                            print(f"Built 1 house on {selected['name']} ✔")

                        else:
                            print("Not enough money to build house.")

                    else:

                        print("Already 4 houses. Consider building a hotel.")

                elif build_choice == "hotel":

                    if selected.get("house_num", 0) == 4 and selected.get("hotel_num", 0)==0:

                        cost = selected.get("hotel_price", 200)

                        if player["money"] >= cost:

                            player["money"] -= cost

                            selected["hotel_num"] = 1

                            selected["house_num"] = 0

                            print(f"Built a hotel on {selected['name']} ✔")
                        else:
                            print("Not enough money to build hotel.")
                    else:
                        print("You need 4 houses first to build a hotel.")

                assets[str(selected["position"])] = selected

    players[index] = player
    save_players(players)
    save_assets(assets)
                
    


def play_turn():
    players, player, _ = get_current_player()
    print(f"\n🎲 {player['username']}'s turn")

    ownership()
    build_houses_and_hotels()
    next_turn()