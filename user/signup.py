#import bcrypt library to use it for encoding user password.
import bcrypt
# import re library to check the regular expression(regex) of an email.
import re

#import json
import json


def check_email():
    regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"

    email=input("\n-please type your email address:").strip()
    
    #check email validation

    if(re.fullmatch(regex,email)):
        return email
    
    else:
        print("-Invalid email address, please type a valid email address !!.")
        check_email()


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
            password = bcrypt.hashpw(bytes, salt)


            unvalidpassword=False 

    #create user dictionary to dump to users.json
    user_info={'username':username,'email':email , 'password':password}

    with open("users.json", mode="a", encoding="utf-8") as write_file:
         json.dump(user_info, write_file)
create_user()