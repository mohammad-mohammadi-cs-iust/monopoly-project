import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PLAYERS_FILE = os.path.join(BASE_DIR, "user", "players.json")

def load_players():
    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

BOARD_SIZE = 11
CELL_W = 15

def empty_cell():
    return [" " * CELL_W] * 4

def cell(number=None, players=""):
    return [
        "┌" + "─" * (CELL_W - 2) + "┐",
        f"│{str(number).center(CELL_W - 2)}│",
        f"│{players.center(CELL_W - 2)}│",
        "└" + "─" * (CELL_W - 2) + "┘",
    ]

def generate_positions():
    pos = []
    for c in range(BOARD_SIZE - 1, -1, -1): pos.append((10, c)) 
    for r in range(9, -1, -1): pos.append((r, 0))
    for c in range(1, 11): pos.append((0, c))
    for r in range(1, 10): pos.append((r, 10))
    return pos[:40]


def draw_board(players=None):
    grid = []
    
    for i in range(BOARD_SIZE):          
       row = []
       
       for i in range(BOARD_SIZE):       
           row.append(empty_cell())
    
       grid.append(row)



    positions = generate_positions()

    for i, (r, c) in enumerate(positions, 1):
        ps = " ".join(players.get(i, [])) if players else ""
        grid[r][c] = cell(f"{i:02}", ps)

    for row in grid:
        for h in range(4):
            print("".join(col[h] for col in row))





def run_graphicalmap():
    print("\n====================================== Maps of The Game =============================================\n")
    players=load_players()
    players=players[2:]

    players_board= {

}

    for player in players:

        if(player['position'] in players_board):
            players_board[player['position']].append("p"+str(player['player_number']))

        else:
            players_board[player['position']]=[]
            players_board[player['position']].append("p"+str(player['player_number']))

    draw_board(players_board)
