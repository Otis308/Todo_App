import tkinter as tk
from gui.GUI_Login import LoginFrame
from gui.GUI_Register import RegisterFrame
from gui.GUI_Tasks import TaskManagerApp

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NOTION")
        self.geometry("1000x780+270+20")
        self.configure(bg='white')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = tk.Frame(self, bg='white')
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginFrame, RegisterFrame, TaskManagerApp):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)
        
    def show_frame(self, cont):
        self.frames[cont].tkraise()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
