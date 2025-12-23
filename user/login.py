import bcrypt
import json
import os

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "users.json")

players_buffer = []


def load_users(address=file_path):
    try:
        with open(address, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []



def insert_player(player_number, username):

    for user in players_buffer:
        if user['username'] == username:
            print("This player has already logged in. Please add a new player.")
            return False  

    new_player = {
        "player_number": player_number,
        "username": username,
        "money": 1500,
        "assets": [],     
        "position":1,
        "prison":False,
        "status":"In Progress",
    }
    
    players_buffer.append(new_player)

    return True 


def find_username():
    users = load_users()

    while True:
        input_username = input("\n-Please type the username: ").strip()

        if not input_username:
            print("Invalid username. Try again.")
            continue

        for user in users:
            if user["username"] == input_username:
                return input_username

        print("Username not found. Please sign up first.")


def check_password(username):
    users = load_users()

    while True:
        input_password = input("\n-Please type the password: ").strip()
        input_password_bytes = input_password.encode("utf-8")

        for user in users:
            if user["username"] == username:
                stored_hash = user["password"].encode("utf-8")

                if bcrypt.checkpw(input_password_bytes, stored_hash):
                    return True
                else:
                    print("Incorrect password. Try again.")


def login():
    if not os.path.exists(file_path):
        print("No users registered.")
        return False

    username = find_username()

    if check_password(username):

        success = insert_player(logged_in_player, username)

        if success:
            print(f"User '{username}' logged in successfully!")
            return True
        else:
            return False

logged_in_player=1


def header_box(text, width=32):
    print("\n")
    print("*" * width)
    print("*" + text.center(width - 2) + "*")
    print("*" * width)


#check if there is at least for 4 players in users.json
load_user=load_users()

if not (len(load_user)>=4):
    print("\nSorry, There should be at least 4 users to start the game. Please go to sign up and add 4 players to start the game.")

else:
    players_path = os.path.join(BASE_DIR, "players.json")
    #load previous users
    player_initial=load_users(players_path)

    # reset players.json at game start
    with open(players_path, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)

        #run the programm
    while logged_in_player != 5:
            header_box("Player " + str(logged_in_player))

            if login():              
                logged_in_player += 1
                
                while True:
                    answer=input("\nDo you want to continue? (yes/no):").strip()
                    if(answer=="yes" or answer=="no"):
                        break
                    else:
                        pass

                if(answer=="no"):
                    with open(players_path, "w", encoding="utf-8") as f:
                        json.dump(player_initial, f, indent=4, ensure_ascii=False)

                    exit()

                else:
                    if logged_in_player == 5:

                        players_path = os.path.join(BASE_DIR, "players.json")

                        with open(players_path, "w", encoding="utf-8") as f:
                            players_buffer.insert(0,"In Progress")
                            json.dump(players_buffer, f, indent=4, ensure_ascii=False)

                        print("\nAll players logged in successfully!")
                        print("\nStarting new game...")

