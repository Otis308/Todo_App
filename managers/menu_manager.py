from tkinter import Menu
from gui.GUI_Editor import EditorFrame
from gui.GUI_Home import HomeFrame

def create_menu(self, frames_dict, show_frame_callback):
    """Tạo menu chung cho toàn bộ app"""
    menubar = Menu(self)
    self.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)

    file_menu.add_command(label="Open", command=lambda: frames_dict[EditorFrame].open_file())
    file_menu.add_command(label="Save", command=lambda: frames_dict[EditorFrame].save_data())
    file_menu.add_command(label="Save As", command=lambda: frames_dict[EditorFrame].save_as())
    file_menu.add_separator()
    file_menu.add_command(label="Export Json", command=lambda: frames_dict[EditorFrame].export_json())
    file_menu.add_command(label="Exit", command=self.quit)

    view_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=view_menu)
    view_menu.add_command(label="Home", command=lambda: show_frame_callback(HomeFrame))
    view_menu.add_command(label="Editor", command=lambda: show_frame_callback(EditorFrame))

    return menubar
