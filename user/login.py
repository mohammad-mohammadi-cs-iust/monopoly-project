import bcrypt
import json
import os

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "users.json")


def load_users(address=file_path):
    try:
        with open(address, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []



def insert_player(player_number, username):
    users = load_users(os.path.join(BASE_DIR, "players.json"))

    new_player = {
        "player_number": player_number,
        "username": username,
        "money": 1500,
        "assets": [],     
        "position":1,
        "prison":False
    }

    users.append(new_player)

    with open(os.path.join(BASE_DIR, "players.json"), "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


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
        return

    username = find_username()
    if check_password(username):
        insert_player(logged_in_player,username)
        print(f"User '{username}' with logged in successfully!")

logged_in_player=1


def header_box(text, width=32):
    print("\n")
    print("*" * width)
    print("*" + text.center(width - 2) + "*")
    print("*" * width)

while logged_in_player!=5:
    header_box("Player "+str(logged_in_player))
    login()
    logged_in_player+=1
