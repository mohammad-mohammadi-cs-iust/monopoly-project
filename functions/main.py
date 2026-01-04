import random
from functions.finance import *
from functions.transactions import *

def dice():
    dice_1 = random.randint(1, 6)
    dice_2 = random.randint(1, 6)
    return dice_1 + dice_2, dice_1, dice_2

        



