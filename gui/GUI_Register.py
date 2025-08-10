import tkinter as tk
import tkinter.messagebox as mb
from tkinter import font
from PIL import Image, ImageTk
from managers.register_manager import load_users, save_users, check_phone_number, check_email_register, email_exits, _toggle_password

class RegisterFrame(tk.Frame):
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

        title_label.grid(row=1, column=0, pady=5, columnspan=2)
        
        subtitle_label = tk.Label(main_frame, text="ĐĂNG KÝ", font=(roboto_font, 18, "bold"), bg='white')
        subtitle_label.grid(row=2, column=0, pady=5, columnspan=2)

        current_row = 3
        
        self.name_entry = self._add_labeled_entry(main_frame, "Họ và tên:", current_row)
        current_row += 1
        
        self.phone_entry = self._add_labeled_entry(main_frame, "Số điện thoại", current_row)
        current_row += 1
        
        self.email_entry = self._add_labeled_entry(main_frame, "Email:", current_row)
        current_row += 1

        pw_frame = tk.Frame(main_frame, bg='white')
        pw_frame.grid(row=current_row, column=1, padx=(10, 0), pady=8, sticky='w')
        self.password_entry = tk.Entry(pw_frame, width=22, font=(roboto_font, 11), show="*", relief='solid')
        self.password_entry.pack(side=tk.LEFT)
        self.show_password_btn = tk.Button(
            pw_frame, text="👁", width=3, command=self._toggle_password,
            font=("Arial", 8), cursor="hand2"
        )
        self.show_password_btn.pack(side=tk.LEFT, padx=5)
        tk.Label(main_frame, text="Mật khẩu:", font=(roboto_font, 14), bg='white').grid(
            row=current_row, column=0, padx=(0, 10), pady=8, sticky='e'
        )
        current_row += 1

        retry_pw_frame = tk.Frame(main_frame, bg='white')
        retry_pw_frame.grid(row=current_row, column=1, padx=(10, 0), pady=8, sticky='w')
        self.retry_password_entry = tk.Entry(retry_pw_frame, width=22, font=(roboto_font, 11), show="*", relief='solid')
        self.retry_password_entry.pack(side=tk.LEFT)
        self.show_retry_password_btn = tk.Button(
            retry_pw_frame, text="👁", width=3, command=self._toggle_retry_password,
            font=("Arial", 8), cursor="hand2"
        )
        self.show_retry_password_btn.pack(side=tk.LEFT, padx=5)
        tk.Label(main_frame, text="Nhập lại mật khẩu:", font=(roboto_font, 14), bg='white').grid(
            row=current_row, column=0, padx=(0, 10), pady=8, sticky='e'
        )
        current_row += 1

        register_btn = tk.Button(main_frame, text="Đăng ký", command=self.register, 
                                width=15, height=1, font=(roboto_font, 15, "bold"),
                                bg="#4CAF50", fg="white", cursor="hand2")
        register_btn.grid(row=current_row, column=0, pady=20, columnspan=2)
        current_row += 1

        login_link = tk.Label(main_frame, text="Đã có tài khoản? Quay lại đăng nhập", 
                             fg="blue", bg='white', cursor="hand2", 
                             font=('Arial', 10, 'underline'))
        login_link.grid(row=current_row, column=0, columnspan=2)
        login_link.bind("<Button-1>", lambda e: self._go_login())

    def _add_labeled_entry(self, parent_frame, text, row, show=None):
        roboto_font = font.Font(family="Roboto", size=50)
        label = tk.Label(parent_frame, text=text, font=(roboto_font, 14), bg='white', anchor='e')
        label.grid(row=row, column=0, padx=(0, 10), pady=8, sticky='e')
        
        entry = tk.Entry(parent_frame, width=25, font=("Times New Roman", 11), show=show, relief='solid')
        entry.grid(row=row, column=1, padx=(10, 0), pady=8, sticky='w')
        
        return entry

    def _go_login(self):
        from gui.GUI_Login import LoginFrame  
        self.controller.show_frame(LoginFrame)

    def register(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        retry_password = self.retry_password_entry.get().strip()

        if not email or not password or not name or not phone or not retry_password:
            mb.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin.")
            return
            
        if not check_email_register(email):
            mb.showerror("Lỗi Email", "Không hợp lệ! Vui lòng nhập đúng định dạng.")
            return
        
        if email_exits(email):
            mb.showerror("Lỗi Email", "Email này đã tồn tại.")
            return

        if password != retry_password:
            mb.showerror("Lỗi mật khẩu", "Mật khẩu nhập lại không khớp.")
            return

        users = load_users()
        users.append({
            "name": name,
            "phonenumber": phone,
            "email": email,
            "password": password
        })
        save_users(users)
        
        mb.showinfo("Thành công", "Đăng ký tài khoản thành công!")
        self._go_login()

    def _toggle_password(self):
        if self.password_entry.cget("show") == "":
            self.password_entry.config(show="*")
        else:
            self.password_entry.config(show="")

    def _toggle_retry_password(self):
        if self.retry_password_entry.cget("show") == "":
            self.retry_password_entry.config(show="*")
        else:
            self.retry_password_entry.config(show="")

            