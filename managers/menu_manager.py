import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

def hello():
    print("Hello!")

def close():
    from gui.GUI_Login import start_login_gui
    root.destroy()
    start_login_gui()
    
def quit_app():
    root.quit()
