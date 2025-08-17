# main.py
import tkinter as tk
from views.GUI_Login import LoginFrame
from views.GUI_Register import RegisterFrame
from views.GUI_Tasks import TaskManagerApp
from views.GUI_Menu import MenuFrame
from controllers.menu_manager import create_menu


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NOTION")
        self.state("zoomed")
        self.configure(bg='white')
        
        self.current_user_email = None  

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Tạo các frame
        self.frames = {}
        for F in (LoginFrame, RegisterFrame, TaskManagerApp, MenuFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        create_menu(self, self.frames, self.show_frame)

        self.show_frame(MenuFrame)
        self.show_frame(LoginFrame)

    def show_frame(self, cont):
        frame = self.frames.get(cont)
        if frame:
            frame.tkraise()

    def show_login(self):
        from src.views.GUI_Login import LoginFrame
        frame = self.frames[LoginFrame]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
