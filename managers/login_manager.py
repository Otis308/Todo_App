#---LOGIN---
import re, os, json
import tkinter.messagebox as mb
from gui.GUI_Tasks import TaskManagerApp

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
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # lên 2 cấp
    user_file = os.path.join(project_root, 'data', 'user.json')

    print(f"[DEBUG] Đang load file user từ: {user_file}")

    if not os.path.exists(user_file):
        mb.showerror("Lỗi", f"Không tìm thấy file dữ liệu {user_file}")
        return []

    with open(user_file, 'r', encoding='utf-8') as f:
        users = json.load(f)

    return users

def _authenticate_user(email, password):
    users = _load_users()
    print("[DEBUG] Users loaded:", users)  

    email = email.strip()
    password = password.strip()
    print(f"[DEBUG] Email nhập: {email}, Password nhập: {password}")

    for user in users:
        print(f"[DEBUG] So sánh với user: {user['email']} / {user['password']}")
        if user['email'].strip() == email and user['password'].strip() == password:
            return user
    return None



def login_action_manager(email, password, controller, email_entry, password_entry):
    if not email or not password:
        mb.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
        return

    user = _authenticate_user(email, password)
    if user:
        mb.showinfo("Thông báo", "Đăng nhập thành công!")
        controller.show_frame(TaskManagerApp)
    else:
        mb.showerror("Lỗi", "Sai email hoặc mật khẩu!")
        if email_entry:
            email_entry.delete(0, 'end')

def _open_register(controller):
    from gui.GUI_Register import RegisterFrame  
    controller.show_frame(RegisterFrame) 
