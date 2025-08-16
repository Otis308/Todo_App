import tkinter as tk
import tkinter.messagebox as mb
from tkinter import filedialog, END
import json

class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.text = tk.Text(self, width=50, height=20)
        self.text.pack(pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.text.delete(1.0, END)
                self.text.insert(END, f.read())
    
    def save_data(self):
        """Lưu dữ liệu"""
        try:
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
            mb.showinfo("Thành công", "Đã lưu dữ liệu thành công!")
        except Exception as e:
            mb.showerror("Lỗi", f"Không thể lưu dữ liệu: {str(e)}")
    
    def export_json(self):
        """Xuất ra file JSON"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(self.tasks, f, ensure_ascii=False, indent=2)
                mb.showinfo("Thành công", f"Đã xuất dữ liệu ra {filename}")
            except Exception as e:
                mb.showerror("Lỗi", f"Không thể xuất dữ liệu: {str(e)}")
    
    def save_as(self):
        """Lưu dữ liệu với tên file mới"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(self.tasks, f, ensure_ascii=False, indent=2)
                mb.showinfo("Thành công", f"Đã lưu dữ liệu ra {filename}")
            except Exception as e:
                mb.showerror("Lỗi", f"Không thể lưu dữ liệu: {str(e)}")

                