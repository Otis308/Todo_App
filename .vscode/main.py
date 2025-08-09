import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gui.GUI_Login import LoginFrame
from gui.GUI_Register import RegisterFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NOTION")
        self.geometry("1000x780+270+20")
        self.resizable(False, False)
        self.configure(bg='white')

        self.container = tk.Frame(self, bg='white')
        self.container.pack(fill='both', expand=True)



        self.frames = {}
        for F in (LoginFrame, RegisterFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)

    def show_frame(self, cont):
        self.frames[cont].tkraise()
    
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
