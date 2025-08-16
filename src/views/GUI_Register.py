import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import tkinter.messagebox as mb
from src.controllers.auth_controller import AuthController

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller        
        self.auth_controller = AuthController()

        # Grid
        self.grid_rowconfigure(0, weight=1)  
        self.grid_rowconfigure(1, weight=0) 
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=0) 
        self.grid_columnconfigure(2, weight=1)  

        main_frame = tk.Frame(self, bg='white')
        main_frame.grid(row=1, column=1)

        try:
            img = Image.open("assets/images/Logo.jpg").resize((180, 180))
            self.img_tk = ImageTk.PhotoImage(img)
            logo_label = tk.Label(main_frame, image=self.img_tk, bg='white')
            logo_label.grid(row=0, column=0, pady=10, columnspan=2)
        except Exception:
            logo_label = tk.Label(main_frame, text="LOGO", font=("Arial", 20), 
                                  bg='lightgray', width=15, height=8)
            logo_label.grid(row=0, column=0, pady=10, columnspan=2)

        roboto_font = font.Font(family="Roboto", size=50)
        quantico_font = font.Font(family="Quantico", size=50)

        tk.Label(main_frame, text="NOTION", font=quantico_font, fg="#990011", bg='white')\
            .grid(row=1, column=0, pady=5, columnspan=2)
        tk.Label(main_frame, text="ĐĂNG KÝ", font=(roboto_font, 18, "bold"), bg='white')\
            .grid(row=2, column=0, pady=5, columnspan=2)

        current_row = 3
        self.name_entry = self._add_labeled_entry(main_frame, "Họ và tên:", current_row); current_row+=1
        self.phone_entry = self._add_labeled_entry(main_frame, "Số điện thoại:", current_row); current_row+=1
        self.email_entry = self._add_labeled_entry(main_frame, "Email:", current_row); current_row+=1
        self.password_entry = self._add_labeled_entry(main_frame, "Mật khẩu:", current_row, show="*"); current_row+=1
        self.retry_password_entry = self._add_labeled_entry(main_frame, "Nhập lại mật khẩu:", current_row, show="*"); current_row+=1

        tk.Button(main_frame, text="Đăng ký", width=15, height=1, font=(roboto_font,15,"bold"),
                  bg="#4CAF50", fg="white", cursor="hand2", command=self._register_action)\
            .grid(row=current_row, column=0, pady=20, columnspan=2); current_row+=1

        login_link = tk.Label(main_frame, text="Đã có tài khoản? Quay lại đăng nhập", 
                              fg="blue", bg='white', cursor="hand2", font=('Arial',10,'underline'))
        login_link.grid(row=current_row, column=0, columnspan=2)
        login_link.bind("<Button-1>", lambda e: self._go_login())

    def _add_labeled_entry(self, parent, text, row, show=None):
        roboto_font = font.Font(family="Roboto", size=50)
        tk.Label(parent, text=text, font=(roboto_font,14), bg='white', anchor='e')\
            .grid(row=row, column=0, padx=(0,10), pady=8, sticky='e')
        entry = tk.Entry(parent, width=25, font=("Times New Roman", 11), show=show, relief='solid')
        entry.grid(row=row, column=1, padx=(10,0), pady=8, sticky='w')
        return entry

    def _register_action(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        retry_password = self.retry_password_entry.get().strip()

        success, message = self.auth_controller.handle_register(name, email, phone, password, retry_password)
        if success:
            mb.showinfo("Thành công", message)
            self._go_login()
        else:
            mb.showerror("Lỗi", message)

    def _go_login(self):
        from src.views.GUI_Login import LoginFrame
        self.controller.show_frame(LoginFrame)
