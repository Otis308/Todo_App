import tkinter as tk
import tkinter.messagebox as mb
from PIL import Image, ImageTk
# Đảm bảo các hàm này có sẵn trong file user_manager.py
# Nếu chưa, bạn cần tạo/cập nhật file đó.
from managers.user_manager.register_manager import load_users, save_users, cal_age, check_email_register, email_exits, hash_password

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
            logo_label.image = self.img_tk  # Giữ tham chiếu ảnh tránh mất hình
            logo_label.grid(row=0, column=0, pady=10, columnspan=2)
        except Exception as e:
            logo_label = tk.Label(main_frame, text="LOGO", font=("Arial", 20), 
                                bg='lightgray', width=15, height=8)
            logo_label.grid(row=0, column=0, pady=10, columnspan=2)

        title_label = tk.Label(main_frame, text="NOTION", font=("Verdana", 50), 
                              fg="#990011", bg='white')
        title_label.grid(row=1, column=0, pady=5, columnspan=2)
        
        subtitle_label = tk.Label(main_frame, text="ĐĂNG KÝ", font=("Times New Roman", 18, "bold"), 
                                 bg='white')
        subtitle_label.grid(row=2, column=0, pady=5, columnspan=2)

        current_row = 3
        
        self.name_entry = self._add_labeled_entry(main_frame, "Họ và tên:", current_row)
        current_row += 1
        
        self.date_of_birth_entry = self._add_labeled_entry(main_frame, "Ngày sinh (dd/mm/yyyy):", current_row)
        current_row += 1
        
        self.email_entry = self._add_labeled_entry(main_frame, "Email:", current_row)
        current_row += 1
        
        self.password_entry = self._add_labeled_entry(main_frame, "Mật khẩu:", current_row, show="*")
        current_row += 1
        
        self.retry_password_entry = self._add_labeled_entry(main_frame, "Nhập lại mật khẩu:", current_row, show="*")
        current_row += 1

        register_btn = tk.Button(main_frame, text="Đăng ký", command=self.register, 
                                width=15, height=1, font=("Times New Roman", 15, "bold"),
                                bg="#4CAF50", fg="white", cursor="hand2")
        register_btn.grid(row=current_row, column=0, pady=20, columnspan=2)
        current_row += 1

        login_link = tk.Label(main_frame, text="Đã có tài khoản? Quay lại đăng nhập", 
                             fg="blue", bg='white', cursor="hand2", 
                             font=('Arial', 10, 'underline'))
        login_link.grid(row=current_row, column=0, columnspan=2)
        login_link.bind("<Button-1>", lambda e: self._go_login())

    def _add_labeled_entry(self, parent_frame, text, row, show=None):
        """Tạo label và entry được căn chỉnh đẹp"""

        label = tk.Label(parent_frame, text=text, font=("Times New Roman", 12), 
                        bg='white', anchor='e')  # anchor='e' để text căn phải
        label.grid(row=row, column=0, padx=(0, 10), pady=8, sticky='e')
        
        entry = tk.Entry(parent_frame, width=25, font=("Times New Roman", 11), show=show)
        entry.grid(row=row, column=1, padx=(10, 0), pady=8, sticky='w')
        
        return entry

    def _go_login(self):
        from gui.GUI_Login import LoginFrame  
        self.controller.show_frame(LoginFrame)

    def register(self):
        name = self.name_entry.get().strip()
        date_of_birth = self.date_of_birth_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        retry_password = self.retry_password_entry.get().strip()

        if not email or not password or not name or not date_of_birth:
            mb.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin.")
            return
        
        age = cal_age(date_of_birth)
        if age == -1:
            mb.showerror("Ngày sinh không hợp lệ", "Ngày sinh phải đúng định dạng dd/mm/yyyy.")
            return
        if age < 18:
            mb.showerror("Tuổi không hợp lệ", "Bạn phải đủ 18 tuổi để đăng ký.")
            return

        if not check_email_register(email):
            mb.showerror("Email không hợp lệ", "Vui lòng nhập đúng định dạng email.")
            return

        if email_exits(email):
            mb.showerror("Email đã tồn tại", "Email này đã có người sử dụng.")
            return

        if password != retry_password:
            mb.showerror("Mật khẩu không đúng", "Mật khẩu nhập lại không khớp.")
            return

        hashed_password = hash_password(password)
        users = load_users()
        users.append({
            "name": name,
            "day_of_birth": date_of_birth,
            "email": email,
            "password": hashed_password
        })
        save_users(users)
        
        mb.showinfo("Thành công", "Đăng ký tài khoản thành công!")
        self._go_login()