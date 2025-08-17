import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import tkinter.messagebox as mb
from controllers.auth_controller import AuthController

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        
        self.auth_controller = AuthController()
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)  
        self.grid_rowconfigure(1, weight=0)  
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=0)  
        self.grid_columnconfigure(2, weight=1)  

        # Main frame
        main_frame = tk.Frame(self, bg='white')
        main_frame.grid(row=1, column=1)

        # Logo
        try:
            img = Image.open("assets/images/Logo.jpg").resize((180, 180))
            self.img_tk = ImageTk.PhotoImage(img)
            logo_label = tk.Label(main_frame, image=self.img_tk, bg='white')
            logo_label.grid(row=0, column=0, pady=10, columnspan=2)
        except Exception:
            logo_label = tk.Label(main_frame, text="LOGO", font=("Arial", 20), 
                                  bg='lightgray', width=15, height=8)
            logo_label.grid(row=0, column=0, pady=10, columnspan=2)

        # Fonts
        roboto_font = font.Font(family="Roboto", size=50)
        quantico_font = font.Font(family="Quantico", size=50)

        # Titles
        tk.Label(main_frame, text="NOTION", font=quantico_font, fg="#990011", bg='white')\
            .grid(row=1, column=0, pady=5, columnspan=2)
        tk.Label(main_frame, text="ĐĂNG NHẬP", font=(roboto_font, 18, "bold"), bg='white')\
            .grid(row=2, column=0, pady=5, columnspan=2)

        # Email
        tk.Label(main_frame, text="Email:", font=(roboto_font, 16), bg='white', anchor='e')\
            .grid(row=3, column=0, padx=(0,10), pady=15, sticky='e')
        self.email_entry = tk.Entry(main_frame, width=25, font=(roboto_font,12), relief='solid')
        self.email_entry.grid(row=3, column=1, padx=(10,0), pady=15, sticky='w')

        # Password
        tk.Label(main_frame, text="Mật khẩu:", font=(roboto_font, 16), bg='white', anchor='e')\
            .grid(row=4, column=0, padx=(0,10), pady=15, sticky='e')
        self.password_entry = tk.Entry(main_frame, width=25, font=(roboto_font,12), show="*", relief='solid')
        self.password_entry.grid(row=4, column=1, padx=(10,0), pady=15, sticky='w')

        # Login button
        tk.Button(main_frame, text="Đăng nhập", width=15, height=1, font=(roboto_font, 15, "bold"),
                  bg="#2196F3", fg="white", cursor="hand2", command=self._login_action)\
            .grid(row=5, column=0, pady=25, columnspan=2)

        # Link to register
        register_link = tk.Label(main_frame, text="Chưa có tài khoản? Đăng ký tại đây", 
                                 fg="blue", bg='white', cursor="hand2",
                                 font=('Arial',10,'underline'))
        register_link.grid(row=6, column=0, columnspan=2)
        register_link.bind("<Button-1>", lambda e: self._go_register())

    def _login_action(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        success, message = self.auth_controller.handle_login(email, password)
        if success:
            mb.showinfo("Thành công", message)
            from views.GUI_Tasks import TaskManagerApp
            task_frame = self.controller.frames[TaskManagerApp]
            task_frame.initialize_user(email)
            self.controller.show_frame(TaskManagerApp)
        else:
            mb.showerror("Lỗi", message)

    def _go_register(self):
        from views.GUI_Register import RegisterFrame
        self.controller.show_frame(RegisterFrame)

    def clear_entries(self):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        