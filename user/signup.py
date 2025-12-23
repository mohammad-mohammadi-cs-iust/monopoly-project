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
file_path = os.path.join(BASE_DIR, 'users.json')

#check if email already exists in users.json
def check_repeat_email(email):
     if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []
     else:
        users = []

     for user in users:
        if(email==user['email']):
            print("This Email already exists. Please try again.")
            return False
     return True

#check email validation

def check_email():
    regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    
    while True:
        email = input("\n-please type your email address: ").strip()
        if re.fullmatch(regex, email) and check_repeat_email(email):
               return email
        
        elif not(re.fullmatch(regex, email)):
            print("-Invalid email address, please type a valid email address !!.")

        else:
            pass


#check if username already exists in username.

def check_username(username):
     if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []
     else:
        users = []

     for user in users:
        if(username==user['username']):
            print("This Username already exists. Please try again.")
            return True
     return False



def create_user():
    #validation of username
    unvalidusername=True

    while unvalidusername:
     username=input("\n-please type your username:").strip()
     if(check_username(username)):
         continue

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

    #create a unique id for user using UUID4.

    user_id = str(uuid.uuid4())

    #create user dictionary to dump to users.json
    user_info={'id':user_id,'username':username,'email':email , 'password':password,"point":0}





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


def header_box(text, width=32):
    print("\n")
    print("*" * width)
    print("*" + text.center(width - 2) + "*")
    print("*" * width)

header_box("SIGN UP")


while True:
    create_user()

    while True:
        answer=input("\nDo you want to still continue? (yes/no):").strip()
        if(answer=="yes" or answer=="no"):
            break
        else:
            continue
        
    if(answer=="yes"):
        continue

    else:
        break