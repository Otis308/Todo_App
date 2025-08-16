import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime
import os

class TaskManagerApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        self.filtered_tasks = self.tasks.copy()
        self.sort_column = None
        self.sort_reverse = False
        
        self.create_widgets()
        self.populate_tree()
        
    def create_widgets(self):
        """Tạo giao diện chính"""
        # Frame chính
        main_frame = tk.Frame(self, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame cho toolbar
        toolbar_frame = tk.Frame(main_frame, bg='white', height=40)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        toolbar_frame.pack_propagate(False)
        
        # Các nút toolbar
        btn_add = tk.Button(toolbar_frame, text="Thêm công việc", command=self.add_task, 
                           bg='#4CAF50', fg='white', relief='solid', borderwidth=1)
        btn_add.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_edit = tk.Button(toolbar_frame, text="Chỉnh sửa", command=self.edit_task,
                            bg='#2196F3', fg='white', relief='solid', borderwidth=1)
        btn_edit.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_delete = tk.Button(toolbar_frame, text="Xóa", command=self.delete_task,
                              bg='#f44336', fg='white', relief='solid', borderwidth=1)
        btn_delete.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bộ lọc
        tk.Label(toolbar_frame, text="Lọc:", bg='white').pack(side=tk.LEFT, padx=(10, 5))
        self.filter_var = tk.StringVar(value="Tất cả")
        filter_combo = ttk.Combobox(toolbar_frame, textvariable=self.filter_var, width=15, state="readonly")
        filter_combo['values'] = ('Tất cả', 'Hoàn thành', 'Đang chờ', 'Đang tiến hành')
        filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        filter_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Sắp xếp
        tk.Label(toolbar_frame, text="Sắp xếp:", bg='white').pack(side=tk.LEFT, padx=(10, 5))
        self.sort_var = tk.StringVar(value="Chọn cột")
        sort_combo = ttk.Combobox(toolbar_frame, textvariable=self.sort_var, width=15, state="readonly")
        sort_combo['values'] = ('Chọn cột', 'Chủ đề', 'Ngày thiết lập', 'Độ ưu tiên', 'Trạng thái')
        sort_combo.pack(side=tk.LEFT, padx=(0, 10))
        sort_combo.bind('<<ComboboxSelected>>', self.on_sort_change)
        
        # Làm mới
        btn_refresh = tk.Button(toolbar_frame, text="Làm mới", command=self.refresh_view,
                               bg='#e6e6e6', relief='solid', borderwidth=1)
        btn_refresh.pack(side=tk.LEFT)
        
        # Frame cho treeview
        tree_frame = tk.Frame(main_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview với scrollbar
        columns = ("title", "created_date", "priority", "status")
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=35)
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Định nghĩa headers với khả năng sắp xếp
        self.tree.heading("title", text="Chủ đề", command=lambda: self.sort_by_column("title"))
        self.tree.heading("created_date", text="Ngày thiết lập", command=lambda: self.sort_by_column("created_date"))
        self.tree.heading("priority", text="Độ ưu tiên", command=lambda: self.sort_by_column("priority"))
        self.tree.heading("status", text="Trạng thái", command=lambda: self.sort_by_column("status"))
        
        # Định nghĩa độ rộng cột
        self.tree.column("title", width=300, anchor="w")
        self.tree.column("created_date", width=150, anchor="center")
        self.tree.column("priority", width=100, anchor="center")
        self.tree.column("status", width=150, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview và scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame cho các nút điều khiển
        control_frame = tk.Frame(main_frame, bg='white', height=50)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        control_frame.pack_propagate(False)
        
        # Label hiển thị số lượng công việc
        self.count_label = tk.Label(control_frame, text="", bg='white', fg='gray')
        self.count_label.pack(side=tk.RIGHT)
        
        # Bind double click để chỉnh sửa
        self.tree.bind("<Double-1>", self.on_double_click)
        
    def populate_tree(self):
        """Điền dữ liệu vào treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm dữ liệu mới
        for i, task in enumerate(self.filtered_tasks):
            item = self.tree.insert("", "end", values=(
                task["title"], 
                task["created_date"], 
                task["priority"], 
                task["status"]
            ))
        
        # Cập nhật số lượng
        self.count_label.config(text=f"{len(self.filtered_tasks)} công việc")
    
    def on_sort_change(self, event=None):
        """Xử lý thay đổi sắp xếp"""
        sort_option = self.sort_var.get()
        if sort_option == "Chủ đề":
            self.sort_by_column("title")
        elif sort_option == "Ngày thiết lập":
            self.sort_by_column("created_date")
        elif sort_option == "Độ ưu tiên":
            self.sort_by_column("priority")
        elif sort_option == "Trạng thái":
            self.sort_by_column("status")
    
    def on_filter_change(self, event=None):
        """Xử lý thay đổi bộ lọc"""
        status = self.filter_var.get()
        self.filter_by_status(status)
    
    def filter_by_status(self, status):
        """Lọc công việc theo trạng thái"""
        if status == "Tất cả":
            self.filtered_tasks = self.tasks.copy()
        else:
            self.filtered_tasks = [task for task in self.tasks if task["status"] == status]
        self.populate_tree()
    
    def sort_by_column(self, column):
        """Sắp xếp theo cột"""
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        
        self.sort_column = column
        
        if column == "priority":
            self.filtered_tasks.sort(key=lambda x: int(x[column]), reverse=self.sort_reverse)
        elif column == "created_date":
            self.filtered_tasks.sort(key=lambda x: datetime.strptime(x[column], "%d-%m-%Y"), reverse=self.sort_reverse)
        else:
            self.filtered_tasks.sort(key=lambda x: x[column], reverse=self.sort_reverse)
        
        self.populate_tree()
    
    def add_task(self):
        """Thêm công việc mới"""
        self.open_task_dialog()
    
    def edit_task(self):
        """Chỉnh sửa công việc được chọn"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một công việc để chỉnh sửa!")
            return
        
        item = selected[0]
        index = self.tree.index(item)
        task = self.filtered_tasks[index]
        self.open_task_dialog(task, index)
    
    def delete_task(self):
        """Xóa công việc được chọn"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một công việc để xóa!")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa công việc này?"):
            item = selected[0]
            index = self.tree.index(item)
            task_to_remove = self.filtered_tasks[index]
            
            # Xóa từ cả filtered_tasks và tasks
            self.filtered_tasks.pop(index)
            self.tasks.remove(task_to_remove)
            
            self.populate_tree()
    
    def on_double_click(self, event):
        """Xử lý double click để chỉnh sửa"""
        self.edit_task()
    
    def open_task_dialog(self, task=None, index=None):
        """Mở dialog để thêm/sửa công việc"""
        dialog = tk.Toplevel(self.controller)
        dialog.title("Thêm công việc" if task is None else "Chỉnh sửa công việc")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.grab_set()
    
    # Center dialog
        dialog.transient(self.controller)
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"400x350+{x}+{y}")
    
        main_frame = tk.Frame(dialog, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="Thông tin công việc",
                font=('Arial', 12, 'bold'), bg='white').pack(pady=(0, 20))
        
        form_frame = tk.Frame(main_frame, bg='white')
        form_frame.pack(fill=tk.X)
        
        # Chủ đề
        tk.Label(form_frame, text="Chủ đề:", font=('Arial', 10), bg='white').pack(anchor='w', pady=(0, 5))
        title_entry = tk.Entry(form_frame, width=40, font=('Arial', 10))
        title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Ngày thiết lập
        tk.Label(form_frame, text="Ngày thiết lập (dd-mm-yyyy):", font=('Arial', 10), bg='white').pack(anchor='w', pady=(0, 5))
        date_entry = tk.Entry(form_frame, width=40, font=('Arial', 10))
        date_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Độ ưu tiên
        tk.Label(form_frame, text="Độ ưu tiên (số):", font=('Arial', 10), bg='white').pack(anchor='w', pady=(0, 5))
        priority_entry = tk.Entry(form_frame, width=40, font=('Arial', 10))
        priority_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Trạng thái
        tk.Label(form_frame, text="Trạng thái:", font=('Arial', 10), bg='white').pack(anchor='w', pady=(0, 5))
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, width=37, state="readonly", font=('Arial', 10))
        status_combo['values'] = ('Hoàn thành', 'Đang chờ', 'Đang tiến hành')
        status_combo.pack(fill=tk.X, pady=(0, 20))
        
        # Điền dữ liệu nếu sửa
        if task:
            title_entry.insert(0, task["title"])
            date_entry.insert(0, task["created_date"])
            priority_entry.insert(0, task["priority"])
            status_var.set(task["status"])
        else:
            date_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))
            status_var.set("Đang chờ")

        def save_task():
            title = title_entry.get().strip()
            date = date_entry.get().strip()
            priority = priority_entry.get().strip()
            status = status_var.get()

            if not all([title, date, priority, status]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
                return

            try:
                datetime.strptime(date, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ! (dd-mm-yyyy)")
                return

            try:
                int(priority)
            except ValueError:
                messagebox.showerror("Lỗi", "Độ ưu tiên phải là số!")
                return

            new_task = {
                "title": title,
                "created_date": date,
                "priority": priority,
                "status": status
            }

            if task is None:  # Thêm mới
                self.tasks.append(new_task)
            else:  # Chỉnh sửa
                self.tasks[index] = new_task

            # Cập nhật danh sách hiển thị
            self.apply_filters()
            dialog.destroy()

        # Buttons
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(pady=(10, 0))

        tk.Button(button_frame, text="Lưu", command=save_task,
                bg='#4CAF50', fg='white', width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Hủy", command=dialog.destroy,
                bg='#f44336', fg='white', width=10).pack(side=tk.LEFT, padx=5)

    
    
    def refresh_view(self):
        """Làm mới giao diện"""
        self.filter_var.set("Tất cả")
        self.sort_var.set("Chọn cột")
        self.filtered_tasks = self.tasks.copy()
        self.populate_tree()
    
    def load_data(self):
        """Tải dữ liệu từ file (có thể được gọi từ menu chính)"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
                self.refresh_view()
                messagebox.showinfo("Thành công", f"Đã tải dữ liệu từ {filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")