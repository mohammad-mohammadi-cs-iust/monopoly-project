import random
from functions.finance import *
from functions.transactions import *
from functions.special import *
from functions.graphicalmap import players_board
from functions.jail import *
def dice():
    dice_1 = random.randint(1, 6)
    dice_2 = random.randint(1, 6)
    return dice_1 + dice_2, dice_1, dice_2
repeat_dice = 0
while True:
    _, _, user = get_current_player()
    if user['prison'] == 0:
        total_dice, dice_1, dice_2 = dice()
        if dice_1 == dice_2:
            repeat_dice += 1
            if repeat_dice == 3:
                user['prison'] += 1
                print('you are going to jail because you had 3 double')
                user['position'] = 11
                next_turn()

                repeat_dice = 0
                continue
            else:
                user['position'] += total_dice
                block = get_current_block()
                if 'owner' in block:
                    if block['owner'] != '':
                        if block['owner'] == user['username']:
                            build_houses_and_hotels()
                            sell_properties()
                        else:
                            resolve_bankrupt(user['position'], total_dice)
                            sell_properties()
                    else:
                        ownership()
                        sell_properties()
                elif block['name'] == 'Chance':
                    chance_card()
                elif block['name'] == "Community Chest":
                    community_chest_card()
                elif block['name'] == 'Income Tax' or block['name'] == 'Luxury Tax':
                    if user['money'] >= block['amount']:
                        user['money'] -= block['amount']
                    else:
                        resolve_bankrupt()
                elif block['name'] == 'Go To Jail':
                    user['prison'] += 1
                    user['position'] = 11
                    print('you are going to jail because you are on go to jail block')
                

                
        else:
            user['position'] += total_dice
            repeat_dice = 0
            next_turn()
            if block['owner'] != '':
                if block['owner'] == user['username']:
                    build_houses_and_hotels()
                    sell_properties()
                else:
                    sell_properties()
            else:
                ownership()
                sell_properties()
    else:
        manage_prison()
    



