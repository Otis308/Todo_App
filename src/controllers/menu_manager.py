from tkinter import Menu
from src.views.GUI_Menu import MenuFrame


def create_menu(self, frames_dict, show_frame_callback):
    """Tạo menu chung cho toàn bộ app"""
    menubar = Menu(self)
    self.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)

    menubar.add_command(label="Open", command=lambda: frames_dict[MenuFrame].open_file())
    menubar.add_command(label="Save", command=lambda: frames_dict[MenuFrame].save_data())
    menubar.add_command(label="Save As", command=lambda: frames_dict[MenuFrame].save_as())
    menubar.add_command(label="Export Json", command=lambda: frames_dict[MenuFrame].export_json())
    menubar.add_command(label="Exit", command=self.quit)
    return menubar
