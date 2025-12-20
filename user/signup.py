#import bcrypt library to use it for encoding user password.
import bcrypt
# import re library to check the regular expression(regex) of an email.
import re

#import json
import json

#import os
import os


def check_email():
    regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    
    while True:
        email = input("\n-please type your email address: ").strip()
        if re.fullmatch(regex, email):
            return email
        print("-Invalid email address, please type a valid email address !!.")


def create_user():
    #validation of username
    unvalidusername=True

    while unvalidusername:
     username=input("\n-please type your username:").strip()

     if(len(username) < 4):
        print("-length Error:your username must have at least 4 characters.")
        continue
     
     else:
        unvalidusername=False
    
    #import and validate email using check_email function.

    email=check_email()
    unvalidpassword=True

    while unvalidpassword:
         password=input("\n-please type your password:").strip()

         if(len(password)<9):
            print("-length Error:your password must have at least 9 characters.")
            continue  

         else:
            bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(bytes, salt).decode('utf-8')


            unvalidpassword=False 

    #create user dictionary to dump to users.json
    user_info={'username':username,'email':email , 'password':password}


    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'users.json')


    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []
    else:
        users = []

    users.append(user_info)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

create_user()