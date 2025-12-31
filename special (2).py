import random
from functions.finance import sell_properties_to_resolve_bankrupt,load_assets,save_assets

chance_cards = [
    {"name": "Advance to GO", "description": "Move to GO and collect $200", "move_to": 1, "money": 200},
    {"name": "Go to Jail", "description": "Go directly to Jail", "move_to": 11, "prison": 1},
    {"name": "Advance to Illinois Avenue", "description": "Move to Illinois Avenue", "move_to": 25},
    {"name": "Advance to St. Charles Place", "description": "Move to St. Charles Place", "move_to": 12},
    {"name": "Advance to nearest Utility", "description": "Move to nearest Utility", "nearest": "Utility"},
    {"name": "Advance to nearest Railroad", "description": "Move to nearest Railroad", "nearest": "Railroad"}, 
    {"name": "Bank pays you dividend of $50", "description": "Collect $50", "money": 50},
    {"name": "Get Out of Jail Free", "description": "Keep this card to get out of Jail", "get_out_of_jail": True},
    {"name": "Go back 3 spaces", "description": "Move back 3 spaces", "move_back": 3},
    {"name": "Take a trip to Reading Railroad", "description": "Move to Reading Railroad", "move_to": 6},
    {"name": "Take a walk on Boardwalk Street", "description": "Move to Boardwalk", "move_to": 40},
    {"name": "Your building loan matures – Collect $150", "description": "Collect $150", "money": 150},
    {"name": "Advance to nearest Railroad (second card)", "description": "Move to nearest Railroad", "nearest": "Railroad"},
    {"name": "Advance token to St. James Place", "description": "Move to St. James Place", "move_to": 17},
]

community_chest_cards = [
    {"name": "Advance to GO", "description": "Move to GO and collect $200", "move_to": 1, "money": 200},
    {"name": "Bank error in your favor – Collect $200", "description": "Collect $200", "money": 200},
    {"name": "Doctor's fees – Pay $50", "description": "Pay $50", "money": -50},
    {"name": "From sale of stock you get $50", "description": "Collect $50", "money": 50},
    {"name": "Get Out of Jail Free", "description": "Keep this card to get out of Jail", "get_out_of_jail": True},
    {"name": "Go to Jail", "description": "Go directly to Jail", "move_to": 11, "prison": 1},
    {"name": "Holiday Fund matures – Receive $100", "description": "Collect $100", "money": 100},
    {"name": "Income tax refund – Collect $20", "description": "Collect $20", "money": 20},
    {"name": "Life insurance matures – Collect $100", "description": "Collect $100", "money": 100},
    {"name": "Hospital fees – Pay $100", "description": "Pay $100", "money": -100},
    {"name": "School fees – Pay $50", "description": "Pay $50", "money": -50},
    {"name": "Receive $25 consultancy fee", "description": "Collect $25", "money": 25},
    {"name": "You have won second prize in a beauty contest – Collect $10", "description": "Collect $10", "money": 10},
]



def chance_card(player):
    card = random.choice(chance_cards)
    print(f"{player['name']} draws Chance card: {card['name']}")

    if "move_to" in card:
        player["position"] = card["move_to"]
    if "move_back" in card:
        player["position"] = (player["position"] - card["move_back"]) % 40

    if "money" in card:

        if(card['money'] > 0):
           player["money"] += card["money"]

        elif(card['money'] < 0 and player['money']+card['money'] >=0):
            player["money"] += card["money"]
        
        else:
            sell_properties_to_resolve_bankrupt(abs(card['money']))

            if(player['money']+card['money']>=0):
                player["money"] +=card['money']
                print("The task of chance Card has done successfully!!")

            else:
                assets=load_assets()
                print(f"\n☠ {player['username']} is BANKRUPT!")

                for asset in assets.values():
                    if asset.get("owner") == player["username"]:
                        asset["owner"] = ""

                    if(asset.get('house_num') or asset.get('hotel_num')):
                        asset['house_num']=0
                        asset['hotel_num']=0
                

                player["money"] = 0
                player["status"] = "Bankrupt"
                player["assets"] = []

                save_assets(assets)



    if "get_out_of_jail" in card:
        player["assets"].append("get_out_of_jail")

    if "prison" in card and card["prison"] == 1:
        player["position"] = 11
        player["prison"] = 1


    if "nearest" in card:
        if card["nearest"] == "Utility":
            options = [13, 29]
            
        else:
            options = [6, 16, 26, 36]

        old_pos = player["position"]
        distances = [(o - player["position"]) % 40 for o in options]
        player["position"] = options[distances.index(min(distances))]

        if player["position"] < old_pos:
           player["money"] += 200

    return card

def community_chest_card(player):
    card = random.choice(community_chest_cards)
    print(f"{player['name']} draws Community Chest card: {card['name']}")

    if "move_to" in card:
        player["position"] = card["move_to"]

    if "move_back" in card:
        player["position"] = (player["position"] - card["move_back"]) % 40

    if "money" in card:
        
        if(card['money'] > 0):
           player["money"] += card["money"]

        elif(card['money'] < 0 and player['money']+card['money'] >=0):
            player["money"] += card["money"]
        
        else:
            sell_properties_to_resolve_bankrupt(abs(card['money']))

            if(player['money']+card['money']>=0):
                player["money"] +=card['money']
                print("The task of chance Card has done successfully!!")

            else:
                assets=load_assets()
                print(f"\n☠ {player['username']} is BANKRUPT!")

                for asset in assets.values():
                    if asset.get("owner") == player["username"]:
                        asset["owner"] = ""

                    if(asset.get('house_num') or asset.get('hotel_num')):
                        asset['house_num']=0
                        asset['hotel_num']=0
                

                player["money"] = 0
                player["status"] = "Bankrupt"
                player["assets"] = []

                save_assets(assets)


    if "get_out_of_jail" in card:
        player["assets"].append("get_out_of_jail")

    if "prison" in card and card["prison"] == 1:
        player["position"] = 11
        player["prison"] = 1

    if "nearest" in card:
        if card["nearest"] == "Utility":
            options = [13, 29]
            
        else:
            options = [6, 16, 26, 36]

        old_pos = player["position"]
        distances = [(o - player["position"]) % 40 for o in options]
        player["position"] = options[distances.index(min(distances))]

        if player["position"] < old_pos:
           player["money"] += 200

    return card



def free_parking(player):
    print(f"{player['name']} landed on Free Parking. No action.")


def go_to_jail(player):
    print(f"{player['name']} landed on Go to Jail and goes directly to Jail!")
    player['prison'] = 1
    player['position']=11


def go(player, old_pos, new_pos):
    if new_pos < old_pos:
        print(f"{player['name']} passed GO and collected $200.")
        player["money"] += 200
