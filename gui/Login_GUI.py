import tkinter as tk
from PIL import Image, ImageTk
import tkinter.messagebox as mb
from managers.user_manager import check_email, check_password
from gui.Register_gui import start_register_gui

def start_login_gui():
    def check_login():
        username = username_entry.get()
        password = password_entry.get()

        if check_email(username) == True & check_password(password) == True:
            mb.showinfo("Thông báo", "Đăng nhập thành công")
        else:
            mb.showwarning("Thông báo", "Tên đăng nhập hoặc mật khẩu sai. Vui lòng nhập lại")

    def open_register():
        root.destroy()
        start_register_gui()
    
    root = tk.Tk()
    root.title("ĐĂNG NHẬP")
    root.geometry("480x600+520+70")
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

    label_subtitle = tk.Label(root, text="ĐĂNG NHẬP", font=("Times New Roman", 18, "bold"), bg='white')
    label_subtitle.grid(row=2, column=0, columnspan=3, pady=5, sticky='n')

    username_label = tk.Label(root, text="Email:", font=("Times New Roman", 20), bg='white')
    username_label.grid(row=3, column=0, sticky='e', padx=10, pady=10)

    username_entry = tk.Entry(root, width=40)
    username_entry.grid(row=3, column=1, columnspan=2, sticky='w', padx=10, pady=10)

    password_label = tk.Label(root, text="Mật khẩu:", font=("Times New Roman", 20), bg='white')
    password_label.grid(row=4, column=0, sticky='e', padx=10, pady=10)

    password_frame = tk.Frame(root, bg='white')
    password_frame.grid(row=4, column=1, columnspan=2, sticky='w', padx=10, pady=10)

    password_entry = tk.Entry(password_frame, width=40, show="*")
    password_entry.grid(row=0, column=0)

    login_button = tk.Button(root, text="Đăng nhập", command=check_login, width=15, height=2, font=("Times New Roman", 12,"bold"))
    login_button.grid(row=5, column=0, columnspan=3, pady=20)

    def toggle_password():
        if password_entry.cget('show') == '':
            password_entry.config(show='*')
            button_show.config(text='👁')
        else:
            password_entry.config(show='')
            button_show.config(text='🙈')

    button_show = tk.Button(password_frame, text="👁", width=3, command=toggle_password)
    button_show.grid(row=0, column=1, padx=5)

    register_link = tk.Label(root, text="Chưa có tài khoản? Đăng ký tại đây", fg="blue", bg='white', cursor="hand2", font=('Arial', 10, 'underline'))
    register_link.grid(row=6, columnspan=3)
    register_link.bind("<Button-1>", lambda e: open_register())
 
    root.mainloop()