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


players_board= {
    1: ["p1","p2"],
    33:["p3"],
    26:["p4"]
}

print("\n====================================== Maps of The Game =============================================\n")
draw_board(players_board)

