#---LOGIN---
import re, hashlib, os, json
import tkinter.messagebox as mb

def check_email_login(username):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    result = re.match(pattern, username)
    if result:
        print("Email hợp lệ")
        return True
    else:
        print("Email không hợp lệ")
        return False

def check_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%.*#?&])[A-Za-z\d@$!#.%*?&]{6,20}$'
    result = re.match(pattern, password)
    if result:
        print("Mật khẩu đúng")
        return True
    else:
        print("Mật khẩu không đúng")
        return False

def _load_users():
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    user_file = os.path.join(current_dir, '..', 'data', 'user.json') 
    user_file = os.path.abspath(user_file)  
    if not os.path.exists(user_file):
        mb.showerror("Lỗi", f"Không tìm thấy file dữ liệu {user_file}")
        return []
    with open(user_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def _authenticate_user(email, password):
    users = _load_users()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    for user in users:
        if user['email'] == email and user['password'] == hashed_password:
            return user 
    return None 

def _login_action(email, password, controller, email_entry, password_entry):
    if not email or not password:
        mb.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
        return

    user = _authenticate_user(email, password)

    if user:
        mb.showinfo("Thông báo", "Đăng nhập thành công!")
    else:
        mb.showerror("Lỗi", "Sai email hoặc mật khẩu!")

def _open_register(controller):
    from gui.GUI_Register import RegisterFrame  
    controller.show_frame(RegisterFrame) 

def _toggle_password(password_entry, button_show):
    if password_entry.cget('show') == '':
        password_entry.config(show='*')
        button_show.config(text='👁')
    else:
        password_entry.config(show='')
        button_show.config(text='🙈')