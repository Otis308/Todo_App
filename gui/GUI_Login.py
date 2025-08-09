import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import tkinter.messagebox as mb
from managers.user_manager.login_manager import check_email_login, check_password, login_action_manager, _open_register

class LoginFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)  
        self.grid_rowconfigure(1, weight=0)  
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=0)  
        self.grid_columnconfigure(2, weight=1)  

        main_frame = tk.Frame(self, bg='white')
        main_frame.grid(row=1, column=1) 

        try:
            img = Image.open("assets/Logo.jpg").resize((180, 180))
            self.img_tk = ImageTk.PhotoImage(img)
            logo_label = tk.Label(main_frame, image=self.img_tk, bg='white')
            logo_label.image = self.img_tk  
            logo_label.grid(row=0, column=0, pady=10, columnspan=2)
        except Exception as e:
            logo_label = tk.Label(main_frame, text="LOGO", font=("Arial", 20), 
                                bg='lightgray', width=15, height=8)
            logo_label.grid(row=0, column=0, pady=10, columnspan=2)

        roboto_font = font.Font(family="Roboto", size=50)
        quantico_font = font.Font(family="Quantico", size=50)
        
        title_label = tk.Label(main_frame, text="NOTION", font=quantico_font, fg="#990011", bg='white')
        title_label.grid(row=1, column=0, pady=5, columnspan=2)

        subtitle_label = tk.Label(main_frame, text="ĐĂNG NHẬP", font=(roboto_font, 18, "bold"), bg='white')
        subtitle_label.grid(row=2, column=0, pady=5, columnspan=2)

        email_label = tk.Label(main_frame, text="Email:", font=(roboto_font, 16), bg='white', anchor='e')
        email_label.grid(row=3, column=0, padx=(0, 10), pady=15, sticky='e')
        
        self.email_entry = tk.Entry(main_frame, width=25, font=(roboto_font, 12))
        self.email_entry.grid(row=3, column=1, padx=(10, 0), pady=15, sticky='w')

        password_label = tk.Label(main_frame, text="Mật khẩu:", font=(roboto_font, 16), bg='white', anchor='e')
        password_label.grid(row=4, column=0, padx=(0, 10), pady=15, sticky='e')
        
        password_frame = tk.Frame(main_frame, bg='white')
        password_frame.grid(row=4, column=1, padx=(10, 0), pady=15, sticky='w')
        
        self.password_entry = tk.Entry(password_frame, width=25, font=(roboto_font, 12), show="*")
        self.password_entry.pack(side=tk.LEFT)

        login_btn = tk.Button(main_frame, text="Đăng nhập", command=self._login_action, 
                                width=15, height=1, font=(roboto_font, 15, "bold"),
                                bg="#2196F3", fg="white", cursor="hand2")
        login_btn.grid(row=5, column=0, pady=25, columnspan=2)

        register_link = tk.Label(main_frame, text="Chưa có tài khoản? Đăng ký tại đây", 
                                        fg="blue", bg='white', cursor="hand2", 
                                        font=('Arial', 10, 'underline'))
        register_link.grid(row=6, column=0, columnspan=2)
        register_link.bind("<Button-1>", lambda e: self._open_register())


    def _login_action(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not check_email_login(email):
            mb.showerror("Error", "Email không hợp lệ!")
            return
        if not check_password(password):
            mb.showerror("Error", "Mật khẩu không hợp lệ!")
            return
        
        login_action_manager(email, password, self.controller, self.email_entry, self.password_entry)

    def _open_register(self):
        _open_register(self.controller)
