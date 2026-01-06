import os
import sys
import random

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from functions.finance import *
from functions.transactions import *
from functions.special import *
from functions.graphicalmap import run_graphicalmap
from functions.jail import manage_prison
from functions.game_end import *
from functions.menu import run_menu
from functions.scoreboard import run_scoreboard
from functions.game_end import show_leaderboard

repeat_dice = 0

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def dice():
    dice_1 = random.randint(1, 6)
    dice_2 = random.randint(1, 6)
    return dice_1 + dice_2, dice_1, dice_2

def _pos_key(pos):
    return str(40 if pos == 0 else pos)

def player_turn():
    global repeat_dice
    repeat_dice = 0

    players, player, index = get_current_player()
    turn_over = False

    while not turn_over:
        clear_screen()
        run_graphicalmap()
        run_scoreboard()
        print(f"\n\n\n--- Current Turn: Player {player['player_number']} Username: {player['username']} ---")

        if player['prison'] > 0:
            manage_prison()
            players, player, index = get_current_player()
            if player['status'] == "Bankrupt":
                turn_over = True
                continue
            if player['prison'] > 0:
                sell_properties()
                build_houses_and_hotels()
                turn_over = True
                continue
        
        print("\n\n")
        print("------- Before rolling dice selling properties--------\n")
        sell_properties()

        print("\n\n")


        input("Press Enter to roll dice...")
        total_dice, dice_1, dice_2 = dice()
        print(f"Dice rolled: {dice_1} and {dice_2}, total: {total_dice}")

        players, player, index = get_current_player()
        old_pos = player['position']
        new_pos = (player['position'] + total_dice) % 40
        player['position'] = new_pos
        players[index] = player
        save_players(players)
        dest_block = get_current_block(player)
        dest_name = dest_block.get("name") if dest_block else "Unknown"
        print(f"You will land on: Position {new_pos} - {dest_name}")

        if new_pos < old_pos:
            print(f"\nYou passed GO and collected $200.")
            player["money"] += 200
            players[index]=player
            save_players(players)


        if dest_block and dest_block.get('name') in ['Chance', 'Community Chest']:
            if dest_block['name'] == 'Chance':
                chance_card(player)
            else:
                community_chest_card(player)
            players, player, index = get_current_player()
            dest_block = get_current_block(player)

        if dest_block and 'buy_price' in dest_block and dest_block.get('owner','') == "":
            ownership()
        elif dest_block and 'owner' in dest_block and dest_block.get('owner','') not in ("", player['username']):
            resolve_bankrupt(player['position'], total_dice)
        elif dest_block and dest_block.get('name') in ['Income Tax', 'Luxury Tax']:
            amount = dest_block.get('amount', 0)
            players, player, index = get_current_player()
            if player['money'] >= amount:
                player['money'] -= amount

                print(f"\n${amount}$ money paid from your account for "+dest_block.get("name"))

                players[index] = player
                save_players(players)
            else:
                print(f"\n$You don't have enough money to pay {amount}$ for "+dest_block.get("name"))

                resolve_bankrupt(player['position'], total_dice)
        elif dest_block and dest_block.get('name') == 'Go To Jail':
            go_to_jail(player)

        build_houses_and_hotels()
        
        
        print("\n\n")
        print("------- After rolling dice selling properties--------\n")
        sell_properties()

        print("\n\n")

        players, player, index = get_current_player()
        players[index] = player
        save_players(players)

        if dice_1 == dice_2:
            repeat_dice += 1
            if repeat_dice < 3:
                print(f"\nDoubles rolled! This is double number {repeat_dice}, you get another turn...")
            else:
                print("\nRolled doubles three times! Going to jail.")
                players, player, index = get_current_player()
                player['prison'] = 1
                player['position'] = 11
                repeat_dice = 0
                players[index] = player
                save_players(players)
                turn_over = True
        else:
            repeat_dice = 0
            turn_over = True

    return repeat_dice == 0


def run_game():
    global repeat_dice

    while True:
        players, player, player_index = get_current_player()

        if player['status'] != 'In Progress':
            next_turn()
            continue

        if end_game_if_finished() == "Game ended successfully. Returning to the menu....":
            print("Game ended successfully. ")
            
            show_leaderboard()

            input("Press Any key to Return to the menu....")
            break

        should_advance = player_turn()

        if should_advance:
            next_turn()  

        if end_game_if_finished() == "Game ended successfully. Returning to the menu....":
            print("Game ended successfully. Returning to the menu....")
            break

        while True:
            answer = input("\nDo you want to continue the game? (yes/no): ").strip().lower()
            if answer in ("yes", "no"):
                break
        if answer == "no":
            break

while True:
    menu = run_menu()
    if menu:
        run_game()
    else:
        break
