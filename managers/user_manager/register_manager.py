#---REGISTER---
import re, hashlib, datetime, json
import tkinter.messagebox as mb

USER_FILE = 'data/user.json'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def cal_age(date_of_birth):
    try:
        bd = datetime.strptime(date_of_birth, "%d/%m/%Y")
        today = datetime.today()
        age = today.year - bd.year
        return age
    except ValueError:
        return -1

def load_users():
    try:
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def check_email_register(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)
     
def email_exits(email):
    users = load_users()
    return any(user['email'] == email for user in users)

def add_user(user_data):
    users = load_users()
    users.append(user_data)
    save_users(users) 