#---REGISTER---
import re, datetime, json
import tkinter.messagebox as mb

USER_FILE = 'data/user.json'


def check_phone_number(phone_number):
    pattern = '^(032|033|034|035|036|037|038|039|096|097|098|086|083|084|085|081|082|088|091|094|070|079|077|076|078|090|093|089|056|058|092|059|099)[0-9]{7}$'
    result = re.match(pattern, phone_number)
    if result:
        print("Số điện thoại hợp lệ.")
    else:
        print("Số điện thoại không hợp lệ.")

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
    
def _toggle_password(password_entry, button_show):
    if password_entry.cget('show') == '':
        password_entry.config(show='*')
        button_show.config(text='👁')
    else:
        password_entry.config(show='')
        button_show.config(text='🙈' )