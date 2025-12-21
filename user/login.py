#import bcrypt library to use it for encoding user password.
import bcrypt
# import re library to check the regular expression(regex) of an email.
import re

#import json
import json

#import os
import os

#import uuid
import uuid

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "users.json")


def login():
    
    if not os.path.exists(file_path):
        print("No users registered.")
        return None

    username = input("Username: ").strip()
    password = input("Password: ").strip().encode("utf-8")

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            print("User database error.")
            return None

    for user in users:
        if user["username"] == username:
            stored_password = user["password"].encode("utf-8")

            if bcrypt.checkpw(password, stored_password):
                print("Login successful.")
                return user
            else:
                print("Incorrect password.")
                return None

    print("Username not found.")
    return None