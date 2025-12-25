import json
import os

BASE_DIR = os.path.dirname(__file__)
file_path_players = os.path.join(BASE_DIR,"user", "players.json")
file_path_assets = os.path.join(BASE_DIR,"asset", "assets.json")

def load_players(address = file_path_players):
    try:
        with open(address, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_assets(address=file_path_assets):
    try:
        with open(address, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def check_position() :
    playerslists = load_players()
    game_status = playerslist[0]
    players = playerslist[1:]
    for player in players:
        return player["position"]

def check_money() :
    playerslists = load_players()
    game_status = playerslist[0]
    players = playerslist[1:]
    for player in players:
        return player["money"]



def load_position() :
    position = check_position()
    with open(file_path_assets, "r", encoding="utf-8") as f:
        assets = json.load(f)
    return assets.get(position)

def ownership() :
    block = load_position()
    block_cost = block.get("buy_price")
    available_money = check_money()
    while True :
        if not block.get("owner") :
            buy_req = input("do you wanna buy the block(yes/no)? ")
            if buy_req == "yes" :
                available_money -= block_cost
                player["money"] = available_money
                return True
            elif buy_req == "no" :
                return None
            else :
                print("invalid answer damn!")
        else :
            pass







def rent_paying(): 
    pass



