import os
import json

from backend.classes.index import User

def get_all_users():
    path = 'backend/db/users.json'
    if not os.path.exists(path):
        raise FileNotFoundError("The users.json file does not exist.")

    with open(path, 'r') as f:
        try:
            users: list[User] = json.load(f)
            return users
        except json.JSONDecodeError:
            users = []

def create_user(user: User):
    path = 'backend/db/users.json'

    if not os.path.exists(path):
        raise FileNotFoundError("The users.json file does not exist.")

    with open(path, 'r+') as f:

        try:
            users: list[User] = json.load(f)
        
        except Exception as e:
            users = []
            
        users.append(user.__dict__)

        f.seek(0)
        json.dump(users, f, indent=4)
