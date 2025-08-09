#Role: Read/Write JSON
#save_task_to_file
#load_task_from_file
#save_user_to_file
#load_user_from_file

import tkinter as tk
from tkinter import font

root = tk.Tk()
root.title("Font Demo")

quantico_font = font.Font(family="Quantico", size=16)
label = tk.Label(root, text="Xin chào, đây là font Quantico!", font=quantico_font)
label.pack(pady=20)

roboto_font = font.Font(family="Roboto", size=13)
label = tk.Label(root, text="Xin chào, đây là font Quantico!", font=quantico_font)
label.pack(pady=20)

root.mainloop()