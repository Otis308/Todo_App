#---LOGIN---
import re, os, json
import tkinter.messagebox as mb
from views.GUI_Tasks import TaskManagerApp
from src.controllers.task_manager import TaskManager

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
    return bool(re.match(pattern, password))

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
    email = email.strip()
    password = password.strip()
    for user in users:
        if user['email'].strip() == email and user['password'].strip() == password:
            return user
    return None

def login_action(login_frame):
    controller = login_frame.controller
    email = login_frame.email_entry.get().strip()
    password = login_frame.password_entry.get().strip()

    user = _authenticate_user(email, password)
    if not user:
        mb.showerror("Lỗi", "Email hoặc mật khẩu không đúng")
        return

    controller.current_user_email = email

    task_frame = controller.frames[TaskManagerApp]
    task_frame.initialize_user(email)

    login_frame.email_entry.delete(0, "end")
    login_frame.password_entry.delete(0, "end")

    controller.show_frame(TaskManagerApp)

def _open_register(controller):
    from gui.GUI_Register import RegisterFrame  
    controller.show_frame(RegisterFrame) 

