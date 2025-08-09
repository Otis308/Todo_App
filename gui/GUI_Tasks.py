import tkinter as tk
from PIL import Image, ImageTk
from managers.menu_manager import hello, close, quit_app

class TaskFrame(tk.Frame):
    def __init__(self, parent, controller, user):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.user = user

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        main_frame = tk.Frame(self, bg='white')
        main_frame.grid(row=1, column=1)

        menubar = tk.Menu(self)
        self.controller.config(menu=menubar)

        label_title = tk.Label(main_frame, text="QUẢN LÝ DANH SÁCH CÔNG VIỆC CÁ NHÂN", 
                               bg='white', font=("Verdana", 20))
        label_title.grid(row=1, column=0, pady=10, columnspan=2)

        label_info = tk.Label(self, text='I. THÔNG TIN CÁ NHÂN', bg='white', font=('Verdana', 14))
        label_info.grid(row=1, column=0, sticky='w', padx=30, pady=10)

        name_info = tk.Label(self, text=(f'Họ và tên: {self.user["name"]}'), bg='white', font=('Times New Roman', 13))
        name_info.grid(row=2, column=0, sticky='w', padx=50, pady=5)

        email_info = tk.Label(self, text=(f'Email: {self.user["email"]}'), bg='white', font=('Times New Roman', 13))
        email_info.grid(row=3, column=0, sticky='w', padx=50, pady=5)

        label_info = tk.Label(self, text='II. QUẢN LÍ CÔNG VIỆC', bg='white', font=('Verdana', 14))
        label_info.grid(row=4, column=0, sticky='w', padx=30, pady=10)
