import tkinter as tk
import tkinter.messagebox as mb
from PIL import Image, ImageTk
from datetime import datetime
from managers.user_manager import load_users, save_users
from managers.user_manager import cal_age, check_email, email_exits, hash_password, add_user

def start_register_gui():
    def register():
        name = name_entry.get().strip()
        date_of_birth = date_of_birth_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        retry_password = retry_password_entry.get().strip()
        
        if not email or not password or not name or not date_of_birth:
            mb.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin")
            return
        
        age = cal_age(date_of_birth)
        if age < 18:
            mb.showerror("Tuổi không hợp lệ", "Bạn phải đủ 18 tuổi để đăng ký.")
            return
        if age == -1:
            mb.showerror("Ngày sinh không hợp lệ", "Ngày sinh phải đúng định dạng dd/mm/yyyy.")
            return

        if not check_email(email):
            mb.showerror("Email không hợp lệ", "Vui lòng nhập đúng định dạng email.")
            return
        
        if email_exits(email):
            mb.showerror("Email đã tồn tại", "Email này đã có người sử dụng.")
            return
        
        if password != retry_password:
            mb.showerror("Mật khẩu không đúng", "Mật khẩu nhập lại không đúng.")
            return

        hashed_password = hash_password(password)
        new_users = {
                "name": name,
                "day_of_birth": date_of_birth,
                "email": email,
                "password": hashed_password
            }
        users = load_users()
        users.append(new_users)
        save_users(users)
        
        mb.showinfo("Thành công", "Đăng ký thành công")

    def open_login():
        from gui.Login_gui import start_login_gui
        root.destroy()
        start_login_gui()
        

    root = tk.Tk()
    root.title("NOTION REGISTER")
    root.geometry("480x730+520+40")
    root.resizable(False, False)
    root.configure(bg='white')
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    img = Image.open("assets/Logo.jpg")
    resize_img = img.resize((180, 180))
    img = ImageTk.PhotoImage(resize_img)
    label_img = tk.Label(root, image=img, bg='white')
    label_img.grid(row=0, column=0, columnspan=3, pady=10)

    label_title = tk.Label(root, text="NOTION", font=("Verdana", 50), fg="blue", bg='white')
    label_title.grid(row=1, column=0, columnspan=3, pady=5, sticky='n')

    label_subtitle = tk.Label(root, text="ĐĂNG KÝ", font=("Times New Roman", 18,"bold"), bg='white')
    label_subtitle.grid(row=2, column=0, columnspan=3, pady=5, sticky='n')

    name_label = tk.Label(root, text="Họ và tên:", font=("Times New Roman", 20), bg='white')
    name_entry = tk.Entry(root, width=30)

    date_of_birth_label = tk.Label(root, text="Ngày sinh:", font=("Times New Roman", 20), bg='white')
    date_of_birth_entry = tk.Entry(root, width=30)

    email_label = tk.Label(root, text="Email:", font=("Times New Roman", 20), bg='white')
    email_entry = tk.Entry(root, width=30)

    password_label = tk.Label(root, text="Mật khẩu:", font=("Times New Roman", 20), bg='white')
    password_entry = tk.Entry(root, width=30, show="*")

    retry_password_label = tk.Label(root, text="Nhập lại mật khẩu:", font=("Times New Roman", 20), bg='white')
    retry_password_entry = tk.Entry(root, width=30, show="*")

    name_label.grid(row = 3, column = 0, sticky='e', padx=10, pady=10)
    name_entry.grid(row = 3, column = 1, sticky='w', padx=10, pady=10)

    date_of_birth_label.grid(row = 4, column = 0, sticky='e',  padx=10, pady=10)
    date_of_birth_entry.grid(row = 4, column = 1, sticky='w', padx=10, pady=10)

    email_label.grid(row = 5, column = 0, sticky='e',  padx=10, pady=10)
    email_entry.grid(row = 5, column = 1, sticky='w', padx=10, pady=10)

    password_label.grid(row = 6, column = 0, sticky='e',  padx=10, pady=10)
    password_entry.grid(row = 6, column = 1, sticky='w', padx=10, pady=10)

    retry_password_label.grid(row = 7, column = 0, sticky='e',  padx=10, pady=10)
    retry_password_entry.grid(row = 7, column = 1, sticky='w', padx=10, pady=10)

    register_button = tk.Button(root,text="Đăng ký", command=register,  width=15, height=1, font=("Times New Roman", 12))
    register_button.grid(row = 8, columnspan=3, pady=20)

    login_link = tk.Label(root, text="Đã có tài khoản? Quay lại đăng nhập", fg="blue", bg='white', cursor="hand2", font=('Arial', 10, 'underline'))
    login_link.grid(row=9, columnspan=3)
    login_link.bind("<Button-1>", lambda e: open_login())

    root.mainloop()






