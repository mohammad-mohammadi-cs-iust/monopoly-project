import json
import os
import random
from functions.finance import save_players,sell_properties_to_resolve_bankrupt,load_assets,save_assets

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
    players, player, index =get_current_player()

    if(player['prison']!=0):
        return True
    
    else:
        return False
    

def get_free_from_jail_card(players, player, index ):
    player['prison']=0
    
    if "get_out_of_jail" in player['assets']:
        player['assets'].remove("get_out_of_jail")


    players[index]=player

    save_players(players)

    print("You successfully got Free from the prison")
    print("Now roll a dice to continue...")


def try_to_get_double(players, player, index):
    try_num=3
    dice1=0
    dice2=0

    while try_num!=0:
        try_num-=1
        print(f"\n-----Round {4-try_num}----")
        dice1=random.randint(1,6)
        dice2=random.randint(1,6)
        print("dice1: ",dice1)
        print("dice2: ",dice2)

        if(dice1==dice2):
            break
    
    if(dice1==dice2):
       player['prison']=0
       players[index]=player
       save_players(players)

       print("You successfully got Free from the prison")
       print("Now you will go forward by sum of the dice1 and dice2")

       return dice1,dice2
    
    else:
        print("Unfortunately , you didn't get Free from the Jail try again in next round !!")


    

def fifty_dollar_to_pay(players, player, index):
     if(player['money'] >= 50):

        player['money']-=50
        player['prison']=0

        players[index]=player

        save_players(players)

        print("You successfully got Free from the prison")
        print("Now roll a dice to continue...")


     else:
        sell_properties_to_resolve_bankrupt()

        if(player['money']>=50):
            
            player['money']-=50
            player['prison']=0

            players[index]=player

            save_players(players)

            print("You successfully got Free from the prison")
            print("Now roll a dice to continue...")

        else:
            if(player['prison'] < 3):
                print("You still don't have 50$ dollars to pay , but you can exit this choice and try another one.")
                
                while True:
                    answer=input("\nDo you want to try another option to get Free(yes/no):").strip()

                    if(answer=="yes" or answer=="no"):
                       break

                    else:
                        continue

                if(answer=="no"):
                    print(f"\n☠ {player['username']} is BANKRUPT!")
                    
                    assets=load_assets()

                    for asset in assets.values():
                        if asset.get("owner") == player["username"]:
                            asset["owner"] = ""

                        if(asset.get("house_num") or asset.get("hotel_num")):
                            asset['hotel_num']=0
                            asset['house_num']=0
                    
                    player["money"] = 0
                    player["status"] = "Bankrupt"
                    player["assets"] = []
                    players[index] = player

                    save_players(players)
                    save_assets(assets)

                else:
                    return 

            elif(player['prison']==3):

                print(f"\n☠ {player['username']} is BANKRUPT!")
                    
                assets=load_assets()

                for asset in assets.values():
                        if asset.get("owner") == player["username"]:
                            asset["owner"] = ""

                        if(asset.get("house_num") or asset.get("hotel_num")):
                            asset['hotel_num']=0
                            asset['house_num']=0
                    
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
        print("The only way to get out of prison is to pay 50$ and roll the dice.")
        fifty_dollar_to_pay(players, player, index)
        return

    choices = []
    if "get_out_of_jail" in player['assets']:
        choices.append("Use Get out of Jail card to get Free")
    choices.append("Try for double to get Free of Jail")
    choices.append("Pay 50$ and roll dice to continue")


    print("\nOptions to get free from Jail:")
    for i, option in enumerate(choices, 1):
        print(f"{i}. {option}")

    while True:
        prompt = input("Type a number to choose an option: ").strip()
        if not prompt.isdigit():
            print("Type a valid number only!")
            continue
        prompt = int(prompt)
        if 1 <= prompt <= len(choices):
            break
        else:
            print("The number is not in the list. Try again!")

    choice = choices[prompt - 1]

    if choice == "Use Get out of Jail card to get Free":
        get_free_from_jail_card(players, player, index)

    elif choice == "Try for double to get Free of Jail":
        dice_result = try_to_get_double(players, player, index)
        if dice_result: 
            dice1, dice2 = dice_result
            player['position'] = (player['position'] + dice1 + dice2) % 40
            players[index] = player
            save_players(players)
            print(f"Moved forward by {dice1 + dice2} steps!")

    elif choice == "Pay 50$ and roll dice to continue":
        fifty_dollar_to_pay(players, player, index)

    if player['prison'] == 0:
        print("You are now free from prison. Continue your turn!")

        
              

manage_prison()