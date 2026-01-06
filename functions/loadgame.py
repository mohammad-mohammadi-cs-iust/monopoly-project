import bcrypt
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
players_path= os.path.join(BASE_DIR, "user", "players.json")
users_path= os.path.join(BASE_DIR, "user", "users.json")


def load_players():
    try:
        with open(players_path, "r", encoding="utf-8") as f:
            data=json.load(f)
            return data if data else []
        
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_users(address=users_path):
    try:
        with open(address, "r", encoding="utf-8") as f:
            data=json.load(f)
            return data if data else []

    except (FileNotFoundError, json.JSONDecodeError):
        return []



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


def header_box(text, width=32):
    print("\n")
    print("*" * width)
    print("*" + text.center(width - 2) + "*")
    print("*" * width)




def show_username(logged_in_player):
    players=load_players()
    return players[logged_in_player+1]["username"]

def run_loadgame():
    logged_in_player = 1
    TOTAL_PLAYERS = 4

    header_box("Load Game")

    if not load_users() or not load_players():
        print(
            "Sorry but there is no in progress game in database "
            "please go to login section and start a new game."
        )
        input("Press any key to return to menu...")



    else:
        while logged_in_player <= TOTAL_PLAYERS:
            header_box(f"Player {logged_in_player}")

            username = show_username(logged_in_player)
            print("Username:", username)

            if not check_password(username):
                break

            logged_in_player += 1

            while True:
                answer = input("\nDo you want to continue? (yes/no): ").strip().lower()
                if answer in ("yes", "no"):
                    break


            
            if answer == "no":
                print("Loading Game Cancelled....")
                break


            if logged_in_player > TOTAL_PLAYERS:
                print("\nAll players logged in successfully!")
                input("\nPress any key to continue the previous game...")
                os.system("cls" if os.name == "nt" else "clear")
                return True