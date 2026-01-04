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

    username = player["username"]
    print("\nHere are your assets that you can sell:\n")

    user_assets = {}

    for position, asset in assets.items():
        if asset.get("owner") == username and "buy_price" in asset:
            buy_price = asset["buy_price"]
            sell_price = buy_price // 2

            if(asset.get("house_num") or asset.get("hotel_num")):
                house=asset.get("house_num",0)
                hotel=asset.get("hotel_num",0)

                if(house > 0):
                   sell_price+=(asset.get("house_creating")//2)*house

                if(hotel==1 and house==0):
                    sell_price+=(asset.get("hotel_creating")//2)*hotel

            user_assets[str(position)] = sell_price

            
            if(asset.get("house_num") or asset.get("hotel_num")):

                print(
                    f"- Position {position} | {asset['name']} | House num:{asset['house_num']} | Hotel num:{asset['hotel_num']}"
                    f"Buy price: {buy_price}$ | Sell price: {sell_price}$"
                )

            else:
                print(
                    f"- Position {position} | {asset['name']} |"
                    f"Buy price: {buy_price}$ | Sell price: {sell_price}$"
                )

    if not user_assets:
        print("You don't own any assets to sell.")
        return

    while True:
        print(f"\nCurrent Money: {player['money']}$")
        prompt = input("Which one do you want to sell? type it's position: ").strip()

        if prompt not in user_assets:
            print("The position you typed is not in your assets. Please try again.")
            continue


        player["money"] += user_assets[prompt]

        if assets[prompt]["name"] in player["assets"]:
            player["assets"].remove(assets[prompt]["name"])

        assets[prompt]["owner"] = ""

        if "house_num" in assets[prompt]:
            assets[prompt]["house_num"] = 0

        if "hotel_num" in assets[prompt]:
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
            answer=input("Do you want to continue (yes/no):").strip().lower()

            if(answer=='yes' or answer=='no'):
                break
            else:
                continue
        
        if(answer=="no"):
            break

        else:
            continue




def sell_properties_to_resolve_bankrupt(debt):
    players, player, player_index = get_current_player()
    assets = load_assets()

    username = player["username"]
    print(f"\n💰 Current money: {player['money']}$ | Debt:{debt}$")
    print("\nHere are your assets that you can sell:\n")

    user_assets = {}

    total_value=0

    for position, asset in assets.items():
        if asset.get("owner") == username and "buy_price" in asset:
            buy_price = asset["buy_price"]
            sell_price = buy_price // 2

            if(asset.get("house_num") or asset.get("hotel_num")):
                house=asset.get("house_num",0)
                hotel=asset.get("hotel_num",0)

                if(house > 0):
                   sell_price+=(asset.get("house_creating")//2)*house

                if(hotel==1 and house==0):
                    sell_price+=(asset.get("hotel_creating")//2)*hotel
            
            total_value+=sell_price
            user_assets[str(position)] = sell_price

            
            if(asset.get("house_num") or asset.get("hotel_num")):

                print(
                    f"- Position {position} | {asset['name']} | House num:{asset['house_num']} | Hotel num:{asset['hotel_num']}"
                    f"Buy price: {buy_price}$ | Sell price: {sell_price}$"
                )

            else:
                print(
                    f"- Position {position} | {asset['name']} |"
                    f"Buy price: {buy_price}$ | Sell price: {sell_price}$"
                )
    if(total_value+player["money"] < debt):
        print("You can not pay the debt even if you sell of your assets. you will be Bankrupted!!")
        return

    if not user_assets:
        print("❌ No assets left to sell.")
        return False


    while True:
        print(f"\nCurrent Money: {player['money']}$")
        prompt = input("Which one do you want to sell? type it's position: ").strip()

        if prompt not in user_assets:
            print("The position you typed is not in your assets. Please try again.")
            continue



        player["money"] += user_assets[prompt]

        if assets[prompt]["name"] in player["assets"]:
            player["assets"].remove(assets[prompt]["name"])

        assets[prompt]["owner"] = ""

        if "house_num" in assets[prompt]:
            assets[prompt]["house_num"] = 0

        if "hotel_num" in assets[prompt]:
            assets[prompt]["hotel_num"] = 0


        players[player_index] = player
        save_players(players)
        save_assets(assets)

        print(f"\n✔ You sold {assets[prompt]['name']} for {user_assets[prompt]}$")

        del user_assets[prompt]

        
        print(f"\n💰 Current money: {player['money']}$ | Debt:{debt}$")

        if player["money"] >= debt:
            print("\n✅ You now have enough money to pay the debt.")
            break



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


    elif "Tax" in current_asset['name']:
        owner_name=None
        if("Income Tax" in current_asset['name']):
            rent=200

        elif("Luxury Tax" in current_asset['name']):
             rent=100

    elif current_asset["name"] in ("Water Works", "Electric Company"):
        utility_count = 0

        for asset in assets.values():
            if asset.get("owner") == owner_name and asset.get("name") in ("Water Works", "Electric Company"):
                utility_count += 1
        
        if(utility_count==1):
           rent = dice*4
        
        elif(utility_count==2):
            rent=dice*10

    if(owner_name!=None):
       print(f"\n💸 Rent required to pay to {owner_name}: {rent}$")

    else:
       print(f"\n💸 Tax required to pay is {rent}$.") 


    while player["money"] < rent:
        if(owner_name!=None):
           print(f"\nYou need {rent}$ to pay rent but you have only {player['money']}$.\nConsider selling properties.")

        else:
             print(f"\nYou need {rent}$ to pay tax but you have only {player['money']}$.\nConsider selling properties.")

        result=sell_properties_to_resolve_bankrupt(rent)

        players, player, player_index = get_current_player()

        if player["money"] >= rent:

            if(owner_name!=None):
               
               print(f"\n💰 You now have enough money ({player['money']}$) to pay the rent.")

            else:
                print(f"\n💰 You now have enough money ({player['money']}$) to pay the tax.")
            break

        if result is False:
            print("\n❌ No way to raise money.")
            break



    if player["money"] < rent:
        print(f"\n☠ {player['username']} is BANKRUPT!")

        if(owner_name!=None):

            for asset in assets.values():
                if asset.get("owner") == player["username"]:
                    asset["owner"] = owner_name
            
            owner["money"] += player["money"]

            player["money"] = 0
            player["status"] = "Bankrupt"
            player["assets"] = []
            players[player_index] = player
            players[owner_index] = owner


        else:
            for asset in assets.values():
                if asset.get("owner") == player["username"]:
                    asset["owner"] = ""

                if(asset.get('house_num') or asset.get('hotel_num')):
                    asset['house_num']=0
                    asset['hotel_num']=0
            
            player["money"] =0

            player["status"] = "Bankrupt"
            player["assets"] = []
            players[player_index] = player

        save_players(players)
        save_assets(assets)
        return
    
    if(owner_name!=None):

        player["money"] -= rent
        owner["money"] += rent

        players[player_index] = player
        players[owner_index] = owner

    else:
        player["money"] -= rent
        players[player_index] = player


    save_players(players)
    
    if(owner_name!=None):
      print(f"\n✅ {player['username']} paid {rent}$ rent to {owner_name}")

    else:
        print(f"\n✅ {player['username']} paid {rent}$ for taxes.")

    print(f"💰 Your new balance: {player['money']}$")
