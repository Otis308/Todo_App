import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from PIL import Image, ImageTk
from tkinter import font
from datetime import datetime
from src.controllers.task_manager import Task,TaskManager
from tkcalendar import DateEntry

class TaskManagerApp(tk.Frame):
    def __init__(self, parent, controller, user_id=None):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.task_manager = None
        self.current_user_email = None
        
        # Tách riêng filtered tasks cho 2 bên
        self.filtered_manual_tasks = []  # Task thủ công
        self.filtered_api_tasks = []     # Task từ API
        
        self.sort_column = None
        self.sort_reverse = False
        self.create_widgets() 

    def initialize_user(self, email):
        self.current_user_email = email
        print(f"🚀 Initializing user: {email}")

        if hasattr(self, "user_label"):
            self.user_label.config(text=f"👤 {email}")

        from managers.task_manager import TaskManager
        self.task_manager = TaskManager(email)

        # Reset trạng thái view
        self.filtered_manual_tasks = []
        self.filtered_api_tasks = []
        self.sort_column = None
        self.sort_reverse = False

        # Load data from JSON if exists
        self.load_tasks_from_json()

        # Load và render
        self.refresh_view()

        print(f"✅ Initialized user {email} with {len(self.task_manager.tasks)} tasks")

    def load_tasks_from_json(self):
        """Load tasks from JSON file - only called after task_manager is initialized"""
        if not self.task_manager:
            return
            
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                # Chỉ thêm task thủ công (không có source API)
                task = self.task_manager.add_task(
                    title=item["title"], 
                    content=item.get("content", ""),
                    status=item.get("status", "Đang chờ"),
                    priority=item.get("priority", "Khẩn cấp")
                )
                # Đánh dấu task thủ công
                if task:
                    task.source = "manual"
        except FileNotFoundError:
            print("📄 No tasks.json file found - starting with empty task list")
        except Exception as e:
            print(f"⚠️ Error loading tasks from JSON: {e}")

    def create_widgets(self):
        main_frame = tk.Frame(self, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toolbar
        self.create_toolbar(main_frame)
        
        # Tạo frame chứa 2 bên
        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Tạo 2 cột với tỉ lệ 50-50
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Bên trái - Task thủ công
        self.create_manual_tasks_section(content_frame)
        
        # Bên phải - Task API
        self.create_api_tasks_section(content_frame)
        
        # Control frame
        self.create_control_frame(main_frame)

    def create_toolbar(self, parent):
        toolbar_frame = tk.Frame(parent, bg='white', height=40)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        toolbar_frame.pack_propagate(False)

        # Tiêu đề
        title_label = tk.Label(toolbar_frame, text="TASK MANAGER", font=("Quantico", 35),
                            fg="#990011", bg='white')
        title_label.grid(row=0, column=0, columnspan=8, pady=(5, 15), sticky="nsew")

        btn_style = {"relief": "solid", "borderwidth": 0.5, "font": ("Arial", 9)}

        # Các nút chức năng
        btn_add = tk.Button(toolbar_frame, text="+ Thêm việc mới", command=self.add_task,
                            bg='#ccffcc', fg='black', **btn_style, padx=8, pady=2)
        btn_add.grid(row=1, column=0, sticky="ew", padx=3, pady=5)

        btn_edit_manual = tk.Button(toolbar_frame, text="✏ Sửa thủ công", command=self.edit_manual_task,
                            bg='#cce5ff', fg='black', **btn_style, padx=8, pady=2)
        btn_edit_manual.grid(row=1, column=1, sticky="ew", padx=3, pady=5)

        btn_edit_api = tk.Button(toolbar_frame, text="✏ Sửa API", command=self.edit_api_task,
                            bg='#e6ccff', fg='black', **btn_style, padx=8, pady=2)
        btn_edit_api.grid(row=1, column=2, sticky="ew", padx=3, pady=5)

        btn_delete_manual = tk.Button(toolbar_frame, text="🗑 Xóa thủ công", command=self.delete_manual_tasks,
                            bg='#ffcccc', fg='black', **btn_style, padx=8, pady=2)
        btn_delete_manual.grid(row=1, column=3, sticky="ew", padx=3, pady=5)

        btn_delete_api = tk.Button(toolbar_frame, text="🗑 Xóa API", command=self.delete_api_tasks,
                            bg='#ffb3cc', fg='black', **btn_style, padx=8, pady=2)
        btn_delete_api.grid(row=1, column=4, sticky="ew", padx=3, pady=5)

        # Làm mới
        btn_refresh = tk.Button(toolbar_frame, text="↻ Làm mới", command=self.refresh_view,
                                bg='white', fg='black', **btn_style, padx=8, pady=2)
        btn_refresh.grid(row=1, column=5, sticky="ew", padx=3, pady=5)

        btn_get_api = tk.Button(toolbar_frame, text="Get API", command=self.load_from_api,
                                bg='#ffffcc', fg='black', **btn_style, padx=8, pady=2)
        btn_get_api.grid(row=1, column=6, sticky="ew", padx=3, pady=5)

        # Thanh tìm kiếm (hàng thứ 2)
        tk.Label(toolbar_frame, text="🔎", font=("Arial", 17), bg='white').grid(
            row=2, column=0, padx=5, pady=2, sticky="e"
        )

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(toolbar_frame, textvariable=self.search_var, font=("Arial", 11))
        search_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5)
        search_entry.bind("<Return>", lambda e: self.search_tasks())

        tk.Button(toolbar_frame, text="Tìm", command=self.search_tasks,
                **btn_style, bg='white').grid(row=2, column=3, padx=2, pady=2, sticky="ew")

        tk.Button(toolbar_frame, text="Xóa lọc", command=self.refresh_view,
                **btn_style, bg='white').grid(row=2, column=4, padx=2, pady=2, sticky="ew")

        # Sắp xếp và lọc
        tk.Label(toolbar_frame, text="Sắp xếp:", bg='white', font=("Arial", 10, "bold")).grid(row=2, column=5, padx=(10, 3))
        self.sort_var = tk.StringVar(value="Chọn cột")
        sort_combo = ttk.Combobox(toolbar_frame, textvariable=self.sort_var, width=12, state="readonly", font=("Arial", 9))
        sort_combo['values'] = ('Chọn cột', 'Chủ đề', 'Ngày thiết lập', 'Độ ưu tiên', 'Trạng thái')
        sort_combo.grid(row=2, column=6, padx=3, sticky="ew")
        sort_combo.bind('<<ComboboxSelected>>', self.on_sort_change)

        # Cấu hình grid weights
        for i in range(7):
            toolbar_frame.grid_columnconfigure(i, weight=1)

    def create_manual_tasks_section(self, parent):
        """Tạo section cho task thủ công (bên trái)"""
        manual_frame = tk.LabelFrame(parent, text="📝 TASK THỦ CÔNG", font=("Arial", 12, "bold"),
                                   fg="#0066cc", bg='white', relief="solid", bd=1)
        manual_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        manual_frame.grid_columnconfigure(0, weight=1)
        manual_frame.grid_rowconfigure(1, weight=1)

        # Checkbox "Chọn tất cả" cho manual tasks
        self.select_all_manual_var = tk.BooleanVar()
        select_all_manual_cb = tk.Checkbutton(manual_frame, text="Chọn tất cả", 
                                            variable=self.select_all_manual_var,
                                            command=self.toggle_select_all_manual, 
                                            bg='white', font=("Arial", 10, "bold"))
        select_all_manual_cb.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Tree view cho manual tasks
        tree_manual_frame = tk.Frame(manual_frame, bg='white')
        tree_manual_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        tree_manual_frame.grid_columnconfigure(0, weight=1)
        tree_manual_frame.grid_rowconfigure(0, weight=1)

        columns = ("title", "created_date", "priority", "status")
        self.tree_manual = ttk.Treeview(tree_manual_frame, columns=columns, show="headings", height=20)
        self.tree_manual.grid(row=0, column=0, sticky="nsew")

        # Headers cho manual tree
        self.tree_manual.heading("title", text="Chủ đề", command=lambda: self.sort_manual_by_column("title"))
        self.tree_manual.heading("created_date", text="Ngày thiết lập", command=lambda: self.sort_manual_by_column("created_date"))
        self.tree_manual.heading("priority", text="Độ ưu tiên", command=lambda: self.sort_manual_by_column("priority"))
        self.tree_manual.heading("status", text="Trạng thái", command=lambda: self.sort_manual_by_column("status"))

        # Columns cho manual tree
        self.tree_manual.column("title", width=200, anchor="w")
        self.tree_manual.column("created_date", width=100, anchor="center")
        self.tree_manual.column("priority", width=80, anchor="center")
        self.tree_manual.column("status", width=100, anchor="center")

        # Scrollbar cho manual tree
        manual_scrollbar = ttk.Scrollbar(tree_manual_frame, orient="vertical", command=self.tree_manual.yview)
        self.tree_manual.configure(yscrollcommand=manual_scrollbar.set)
        manual_scrollbar.grid(row=0, column=1, sticky="ns")

        # Checkbox frame cho manual tasks
        self.create_checkbox_frame(manual_frame, "manual")

        # Bind events cho manual tree
        self.tree_manual.bind("<Double-1>", self.on_manual_double_click)

    def create_api_tasks_section(self, parent):
        """Tạo section cho task API (bên phải)"""
        api_frame = tk.LabelFrame(parent, text="🌐 TASK TỪ API", font=("Arial", 12, "bold"),
                                fg="#cc6600", bg='white', relief="solid", bd=1)
        api_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        api_frame.grid_columnconfigure(0, weight=1)
        api_frame.grid_rowconfigure(1, weight=1)

        # Checkbox "Chọn tất cả" cho API tasks
        self.select_all_api_var = tk.BooleanVar()
        select_all_api_cb = tk.Checkbutton(api_frame, text="Chọn tất cả", 
                                         variable=self.select_all_api_var,
                                         command=self.toggle_select_all_api, 
                                         bg='white', font=("Arial", 10, "bold"))
        select_all_api_cb.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Tree view cho API tasks
        tree_api_frame = tk.Frame(api_frame, bg='white')
        tree_api_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        tree_api_frame.grid_columnconfigure(0, weight=1)
        tree_api_frame.grid_rowconfigure(0, weight=1)

        columns = ("title", "created_date", "priority", "status")
        self.tree_api = ttk.Treeview(tree_api_frame, columns=columns, show="headings", height=20)
        self.tree_api.grid(row=0, column=0, sticky="nsew")

        # Headers cho API tree
        self.tree_api.heading("title", text="Chủ đề", command=lambda: self.sort_api_by_column("title"))
        self.tree_api.heading("created_date", text="Ngày thiết lập", command=lambda: self.sort_api_by_column("created_date"))
        self.tree_api.heading("priority", text="Độ ưu tiên", command=lambda: self.sort_api_by_column("priority"))
        self.tree_api.heading("status", text="Trạng thái", command=lambda: self.sort_api_by_column("status"))

        # Columns cho API tree
        self.tree_api.column("title", width=200, anchor="w")
        self.tree_api.column("created_date", width=100, anchor="center")
        self.tree_api.column("priority", width=80, anchor="center")
        self.tree_api.column("status", width=100, anchor="center")

        # Scrollbar cho API tree
        api_scrollbar = ttk.Scrollbar(tree_api_frame, orient="vertical", command=self.tree_api.yview)
        self.tree_api.configure(yscrollcommand=api_scrollbar.set)
        api_scrollbar.grid(row=0, column=1, sticky="ns")

        # Checkbox frame cho API tasks
        self.create_checkbox_frame(api_frame, "api")

        # Bind events cho API tree
        self.tree_api.bind("<Double-1>", self.on_api_double_click)

    def create_checkbox_frame(self, parent, task_type):
        """Tạo frame chứa checkbox cho từng loại task"""
        checkbox_frame = tk.Frame(parent, bg='white', width=50)
        if task_type == "manual":
            checkbox_frame.grid(row=1, column=1, sticky="ns", padx=(5, 0))
            self.checkbox_manual_vars = {}
        else:  # api
            checkbox_frame.grid(row=1, column=1, sticky="ns", padx=(5, 0))
            self.checkbox_api_vars = {}

        checkbox_frame.grid_propagate(False)

        # Canvas và scrollbar cho checkboxes
        canvas = tk.Canvas(checkbox_frame, bg='white', width=45, highlightthickness=0)
        scrollbar = ttk.Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
        inner_frame = tk.Frame(canvas, bg='white')

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew", padx=2)
        scrollbar.grid(row=0, column=1, sticky="ns")

        checkbox_frame.grid_rowconfigure(0, weight=1)
        checkbox_frame.grid_columnconfigure(0, weight=1)

        # Lưu reference
        if task_type == "manual":
            self.checkbox_manual_canvas = canvas
            self.checkbox_manual_inner_frame = inner_frame
        else:
            self.checkbox_api_canvas = canvas
            self.checkbox_api_inner_frame = inner_frame

        canvas_frame = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_frame, width=event.width)

        canvas.bind("<Configure>", configure_canvas)

    def update_checkbox_positions(self, task_type):
        """Cập nhật vị trí các checkbox để khớp với tree rows"""
        if task_type == "manual":
            canvas = self.checkbox_manual_canvas
            inner_frame = self.checkbox_manual_inner_frame
            checkbox_vars = self.checkbox_manual_vars
            tree = self.tree_manual
        else:
            canvas = self.checkbox_api_canvas
            inner_frame = self.checkbox_api_inner_frame
            checkbox_vars = self.checkbox_api_vars
            tree = self.tree_api

        # Xóa tất cả checkbox cũ
        for widget in inner_frame.winfo_children():
            widget.destroy()
        checkbox_vars.clear()

        # Tạo checkbox cho mỗi task
        row = 0
        for item in tree.get_children():
            task_id = tree.item(item)['tags'][0] if tree.item(item)['tags'] else str(row)
            
            var = tk.BooleanVar()
            checkbox_vars[task_id] = var
            
            cb = tk.Checkbutton(
                inner_frame,
                variable=var,
                bg='white',
                font=("Arial", 12),
                pady=2
            )
            cb.grid(row=row, column=0, pady=1, sticky="n")
            row += 1

        # Cập nhật scrollregion
        inner_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def toggle_select_all_manual(self):
        """Toggle tất cả checkbox manual"""
        select_all = self.select_all_manual_var.get()
        for var in self.checkbox_manual_vars.values():
            var.set(select_all)

    def toggle_select_all_api(self):
        """Toggle tất cả checkbox API"""
        select_all = self.select_all_api_var.get()
        for var in self.checkbox_api_vars.values():
            var.set(select_all)

    def get_selected_task_ids(self, task_type):
        """Lấy danh sách task_id của các task được chọn"""
        selected_ids = []
        if task_type == "manual":
            checkbox_vars = self.checkbox_manual_vars
        else:
            checkbox_vars = self.checkbox_api_vars

        for task_id, var in checkbox_vars.items():
            if var.get():  # Checkbox được chọn
                selected_ids.append(task_id)
        return selected_ids

    def populate_trees(self):
        """Điền dữ liệu vào cả 2 tree"""
        # Xóa tất cả items cũ
        for item in self.tree_manual.get_children():
            self.tree_manual.delete(item)
        for item in self.tree_api.get_children():
            self.tree_api.delete(item)

        # Thêm manual tasks
        for task in self.filtered_manual_tasks:
            self.tree_manual.insert("", "end", tags=(task.task_id,), values=(
                task.title,
                task.created_date,
                task.priority,
                task.status
            ))

        # Thêm API tasks
        for task in self.filtered_api_tasks:
            self.tree_api.insert("", "end", tags=(task.task_id,), values=(
                task.title,
                task.created_date,
                task.priority,
                task.status
            ))

        # Cập nhật checkbox positions
        self.update_checkbox_positions("manual")
        self.update_checkbox_positions("api")

        # Reset checkbox "Chọn tất cả"
        self.select_all_manual_var.set(False)
        self.select_all_api_var.set(False)

        # Cập nhật số lượng task
        self.update_status_display()

    def create_control_frame(self, parent):
        """Tạo control frame với thông tin user và số lượng task"""
        control_frame = tk.Frame(parent, bg='white', height=50)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        control_frame.pack_propagate(False)
        
        # Frame bên trái cho thông tin user
        left_frame = tk.Frame(control_frame, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Hiển thị tên user với icon
        self.user_label = tk.Label(left_frame,
            text=f"👤 {self.controller.current_user_email or ''}",
            bg='white', fg='#0066cc', font=('Arial', 13, 'bold'))
        self.user_label.pack(side=tk.LEFT, anchor='w')
        
        # Nút đăng xuất
        if hasattr(self.controller, 'show_login'):
            btn_logout = tk.Button(left_frame, text="↩ Đăng xuất", 
                                 command=self.logout, bg='#ffe6e6', fg='red',
                                 font=('Arial', 10), relief="solid", borderwidth=1)
            btn_logout.pack(side=tk.LEFT, padx=(20, 0))
        
        # Frame bên phải cho số lượng task
        right_frame = tk.Frame(control_frame, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.count_label = tk.Label(right_frame, text="📝 Manual: 0 | 🌐 API: 0", 
                                   font=('Arial', 12, 'bold'), 
                                   bg='white', fg='#666666')
        self.count_label.pack(side=tk.RIGHT, anchor='e')

    def update_status_display(self):
        """Cập nhật hiển thị số lượng task"""
        if not self.task_manager:
            self.count_label.config(text="📝 Manual: 0 | 🌐 API: 0")
            self.user_label.config(text="👤 Không có user")
            return

        manual_count = len(self.filtered_manual_tasks)
        api_count = len(self.filtered_api_tasks)
        total_manual = len([t for t in self.task_manager.get_all_tasks() or [] if getattr(t, 'source', 'manual') == 'manual'])
        total_api = len([t for t in self.task_manager.get_all_tasks() or [] if getattr(t, 'source', None) == 'api'])
        
        self.user_label.config(text=f"👤 {self.current_user_email or ''}")

        if manual_count == total_manual and api_count == total_api:
            count_text = f"📝 Manual: {manual_count} | 🌐 API: {api_count}"
        else:
            count_text = f"📝 Manual: {manual_count}/{total_manual} | 🌐 API: {api_count}/{total_api}"

        self.count_label.config(text=count_text)

    def refresh_view(self):
        """Làm mới view và phân loại tasks"""
        if not self.task_manager:
            print("⚠️ TaskManager chưa khởi tạo!")
            self.filtered_manual_tasks = []
            self.filtered_api_tasks = []
            self.clear_treeviews()
            self.update_status_display()
            return

        # Lấy tất cả tasks và phân loại
        all_tasks = self.task_manager.get_all_tasks() or []
        self.filtered_manual_tasks = [t for t in all_tasks if getattr(t, 'source', 'manual') == 'manual']
        self.filtered_api_tasks = [t for t in all_tasks if getattr(t, 'source', None) == 'api']
        
        self.populate_trees()
        print(f"✅ Refreshed: Manual={len(self.filtered_manual_tasks)}, API={len(self.filtered_api_tasks)}")

    def clear_treeviews(self):
        """Xóa tất cả items trong cả 2 tree"""
        if hasattr(self, 'tree_manual'):
            for item in self.tree_manual.get_children():
                self.tree_manual.delete(item)
        if hasattr(self, 'tree_api'):
            for item in self.tree_api.get_children():
                self.tree_api.delete(item)

    def search_tasks(self):
        """Tìm kiếm tasks trong cả 2 bên"""
        if not self.task_manager:
            return
        keyword = self.search_var.get()
        all_results = self.task_manager.search_tasks(keyword)
        
        # Phân loại kết quả tìm kiếm
        self.filtered_manual_tasks = [t for t in all_results if getattr(t, 'source', 'manual') == 'manual']
        self.filtered_api_tasks = [t for t in all_results if getattr(t, 'source', None) == 'api']
        
        self.populate_trees()

    def on_sort_change(self, event=None):
        """Xử lý thay đổi sắp xếp cho cả 2 bên"""
        sort_option = self.sort_var.get()
        column_mapping = {
            "Chủ đề": "title",
            "Ngày thiết lập": "created_date", 
            "Độ ưu tiên": "priority",
            "Trạng thái": "status"
        }
        
        if sort_option in column_mapping:
            column = column_mapping[sort_option]
            self.sort_manual_by_column(column)
            self.sort_api_by_column(column)

    def sort_manual_by_column(self, column):
        """Sắp xếp manual tasks"""
        if not self.task_manager:
            return
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        
        self.sort_column = column
        all_sorted = self.task_manager.sort_tasks(column, self.sort_reverse)
        self.filtered_manual_tasks = [t for t in all_sorted if getattr(t, 'source', 'manual') == 'manual']
        self.populate_trees()

    def sort_api_by_column(self, column):
        """Sắp xếp API tasks"""
        if not self.task_manager:
            return
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        
        self.sort_column = column
        all_sorted = self.task_manager.sort_tasks(column, self.sort_reverse)
        self.filtered_api_tasks = [t for t in all_sorted if getattr(t, 'source', None) == 'api']
        self.populate_trees()

    def add_task(self):
        """Thêm task mới (luôn là manual)"""
        self.show_task_dialog()

    def edit_manual_task(self):
        """Chỉnh sửa manual task"""
        self.edit_task_by_type("manual")

    def edit_api_task(self):
        """Chỉnh sửa API task"""
        self.edit_task_by_type("api")

    def edit_task_by_type(self, task_type):
        """Chỉnh sửa task theo loại"""
        tree = self.tree_manual if task_type == "manual" else self.tree_api
        selected = tree.selection()
        
        if not selected:
            messagebox.showwarning("Cảnh báo", f"Vui lòng chọn một công việc {task_type} để chỉnh sửa!")
            return
        
        try:
            item = selected[0]
            tags = tree.item(item)['tags']
            
            if not tags:
                messagebox.showerror("Lỗi", "Không tìm thấy ID công việc!")
                return
                
            task_id = tags[0]
            task = self.task_manager.get_task_by_id(task_id)
            
            if not task:
                messagebox.showerror("Lỗi", "Không tìm thấy công việc!")
                return
            
            self.show_task_dialog(task)
            
        except Exception as e:
            print(f"Lỗi khi edit task: {e}")
            messagebox.showerror("Lỗi", f"Không thể chỉnh sửa: {str(e)}")

    def delete_manual_tasks(self):
        """Xóa các manual tasks được chọn"""
        self.delete_selected_tasks("manual")

    def delete_api_tasks(self):
        """Xóa các API tasks được chọn"""
        self.delete_selected_tasks("api")

    def delete_selected_tasks(self, task_type):
        """Xóa nhiều task được chọn theo loại"""
        selected_ids = self.get_selected_task_ids(task_type)
        
        if not selected_ids:
            messagebox.showwarning("Cảnh báo", f"Vui lòng chọn ít nhất một công việc {task_type} để xóa!")
            return
        
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa {len(selected_ids)} công việc {task_type} đã chọn?"):
            return
        
        try:
            deleted_count = 0
            for task_id in selected_ids:
                if self.task_manager.delete_task(task_id):
                    deleted_count += 1
            
            if deleted_count > 0:
                messagebox.showinfo("Thành công", f"Đã xóa {deleted_count} công việc {task_type}!")
                self.refresh_view()
                if task_type == "manual":
                    self.select_all_manual_var.set(False)
                else:
                    self.select_all_api_var.set(False)
            else:
                messagebox.showerror("Lỗi", "Không thể xóa công việc nào!")
                
        except Exception as e:
            print(f"Lỗi khi xóa nhiều task {task_type}: {e}")
            messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}")

    def show_task_dialog(self, task=None):
        """Hiển thị dialog thêm/sửa task"""
        if not self.task_manager:
            messagebox.showerror("Lỗi", "TaskManager chưa khởi tạo!")
            return
            
        dialog = tk.Toplevel(self)
        dialog.title("Thêm công việc mới" if not task else "Chỉnh sửa công việc")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        w = 600
        h = 450
        ws = dialog.winfo_screenwidth()
        hs = dialog.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(dialog, text="Tiêu đề:", font=("Arial", 10, "bold")).pack(anchor='w', padx=10, pady=(10,5))
        title_var = tk.StringVar(value=task.title if task else "")
        title_entry = tk.Entry(dialog, textvariable=title_var, font=("Arial", 11))
        title_entry.pack(fill='x', padx=10, pady=(0,10))
        
        tk.Label(dialog, text="Nội dung:", font=("Arial", 10, "bold")).pack(anchor='w', padx=10, pady=5)
        content_text = tk.Text(dialog, height=6, font=("Arial", 10))
        content_text.pack(fill='both', expand=True, padx=10, pady=(0,10))   
        if task:
            content_text.insert('1.0', task.content)
        
        frame = tk.Frame(dialog)
        frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(frame, text="Độ ưu tiên:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
        priority_var = tk.StringVar(value=task.priority if task else "Khẩn cấp")
        priority_combo = ttk.Combobox(frame, textvariable=priority_var, state="readonly", width=15)
        priority_combo['values'] = ('Khẩn cấp', 'Rất cao', 'Cao', 'Trung bình', 'Thấp')
        priority_combo.grid(row=0, column=1, padx=(10,0), sticky='w')
        
        tk.Label(frame, text="Trạng thái:", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=(20,0), sticky='w')
        status_var = tk.StringVar(value=task.status if task else "Đang chờ")
        status_combo = ttk.Combobox(frame, textvariable=status_var, state="readonly", width=15)
        status_combo['values'] = ('Đang chờ', 'Đang tiến hành', 'Hoàn thành')
        status_combo.grid(row=0, column=3, padx=(10,0), sticky='w')
        
        tk.Label(frame, text="Ngày thiết lập:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky='w', pady=(10,0))
        date_var = tk.StringVar(value=task.created_date if task else datetime.now().strftime("%d-%m-%Y"))

        date_entry = DateEntry(
            frame,
            width=15,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd-mm-yyyy', 
            textvariable=date_var
        )
        date_entry.grid(row=1, column=1, padx=(10, 0), sticky='w', pady=(10, 0))
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(fill='x', padx=10, pady=20)
        
        def save_task():
            title = title_var.get().strip()
            if not title:
                messagebox.showerror("Lỗi", "Tiêu đề không được để trống!")
                return
                
            content = content_text.get('1.0', 'end-1c').strip()
            priority = priority_var.get()
            status = status_var.get()
            date = date_var.get()
            
            try:
                if task:  # Sửa task
                    updated_task = self.task_manager.update_task(
                        task_id=task.task_id,
                        title=title,
                        content=content,
                        created_date=date,
                        priority=priority,
                        status=status
                    )
                    if updated_task:
                        messagebox.showinfo("Thành công", "Đã cập nhật công việc!")
                    else:
                        messagebox.showerror("Lỗi", "Không thể cập nhật công việc!")
                else:  # Thêm task mới (luôn là manual)
                    new_task = self.task_manager.add_task(
                        title=title,
                        content=content,
                        created_date=date,
                        priority=priority,
                        status=status
                    )
                    if new_task:
                        # Đánh dấu là manual task
                        new_task.source = "manual"
                        messagebox.showinfo("Thành công", "Đã thêm công việc mới!")
                    else:
                        messagebox.showerror("Lỗi", "Không thể thêm công việc!")
                
                self.refresh_view()
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

        btn_save = tk.Button(
            btn_frame,
            text="💾 Lưu",
            command=save_task,
            bg='#ccffcc',
            font=("Arial", 11),
            compound="left",
            width=10  
        )
        btn_save.grid(row=0, column=0, padx=2)

        btn_cancel = tk.Button(
            btn_frame,
            text="❌ Hủy",
            command=dialog.destroy,
            bg='#ffcccc',
            font=("Arial", 11),
            compound="left",
            width=10
        )
        btn_cancel.grid(row=0, column=1, padx=5)
                        
        title_entry.focus()

    def on_manual_double_click(self, event):
        """Xử lý double click trên manual tree để xem chi tiết"""
        self.on_double_click_by_type(event, "manual")

    def on_api_double_click(self, event):
        """Xử lý double click trên API tree để xem chi tiết"""
        self.on_double_click_by_type(event, "api")

    def on_double_click_by_type(self, event, task_type):
        """Xử lý double click để xem chi tiết theo loại"""
        tree = self.tree_manual if task_type == "manual" else self.tree_api
        selected = tree.selection()
        if not selected:
            return
        
        try:
            item = selected[0]
            task_id = tree.item(item)['tags'][0]
            task = self.task_manager.get_task_by_id(task_id)
            
            if task:
                self.show_task_detail(task)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị chi tiết: {str(e)}")

    def show_task_detail(self, task):
        """Hiển thị chi tiết task"""
        detail_window = tk.Toplevel(self)
        detail_window.title(f"Chi tiết: {task.title}")
        detail_window.geometry("600x450")

        # Căn giữa màn hình
        detail_window.update_idletasks()
        w = 600
        h = 450
        ws = detail_window.winfo_screenwidth()
        hs = detail_window.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        detail_window.geometry(f"{w}x{h}+{x}+{y}")

        detail_window.transient(self)
        detail_window.grab_set()

        main_frame = tk.Frame(detail_window, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        title_frame = tk.Frame(main_frame, bg='white')
        title_frame.pack(fill='x', pady=(0, 20))

        # Hiển thị icon khác nhau cho manual vs API task
        icon = "📝" if getattr(task, 'source', 'manual') == 'manual' else "🌐"
        tk.Label(title_frame, text=icon, font=("Arial", 20), bg='white').pack(side='left', pady=2)
        tk.Label(title_frame, text=task.title, font=("Arial", 18, "bold"),
                bg='white', fg='#333').pack(side='left', padx=10)

        info_frame = tk.Frame(main_frame, bg='white')
        info_frame.pack(fill='x', pady=(0, 20))

        info_data = [
            ("📅 Ngày tạo:", task.created_date),
            ("🔥 Độ ưu tiên:", task.priority),
            ("📊 Trạng thái:", task.status),
            ("🆔 ID:", task.task_id),
            ("📋 Nguồn:", "Thủ công" if getattr(task, 'source', 'manual') == 'manual' else "API")
        ]

        for i, (label, value) in enumerate(info_data):
            row = i // 2
            col = (i % 2) * 2

            tk.Label(info_frame, text=label, font=("Arial", 14, "bold"),
                    bg='white').grid(row=row, column=col, sticky='w', padx=(0, 10), pady=5)
            tk.Label(info_frame, text=value, font=("Arial", 14),
                    bg='white', fg='#555').grid(row=row, column=col+1, sticky='w', padx=(0, 30), pady=5)

        tk.Label(main_frame, text="📝 Nội dung:", font=("Arial", 14, "bold"),
                bg='white').pack(anchor='w', pady=(10, 5))

        content_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        content_frame.pack(fill='both', expand=True, pady=(0, 20))

        content_text = tk.Text(content_frame, font=("Arial", 12), wrap='word',
                            state='disabled', bg='#f9f9f9', relief='flat', height=6)
        content_text.pack(fill='both', expand=True, padx=10, pady=10)

        content_text.config(state='normal')
        content_text.insert('1.0', task.content if task.content else "Không có nội dung")
        content_text.config(state='disabled')

        tk.Button(main_frame, text="❌ Đóng", command=detail_window.destroy,
                bg='#e6e6e6', font=("Arial", 11), width=10).pack(pady=(10, 0))

    def logout(self):
        if messagebox.askyesno("Đăng xuất", f"Bạn có chắc chắn muốn đăng xuất {self.controller.current_user_email}?"):

            # Xóa thông tin user hiện tại
            self.controller.current_user_email = None

            # Xóa dữ liệu task trong bộ nhớ
            if self.task_manager:
                self.task_manager.tasks.clear()
            self.task_manager = None
            if hasattr(self, 'filtered_manual_tasks'):
                self.filtered_manual_tasks.clear()
            if hasattr(self, 'filtered_api_tasks'):
                self.filtered_api_tasks.clear()

            # Xóa giao diện hiển thị task
            self.clear_task_view()

            # Xóa label tên/email
            if hasattr(self, 'user_label'):
                self.user_label.config(text="")

            # Quay về màn hình login
            login_frame = self.controller.show_login()

            # Xóa email & password trong form login
            if hasattr(login_frame, "email_entry") and hasattr(login_frame, "password_entry"):
                login_frame.email_entry.delete(0, "end")
                login_frame.password_entry.delete(0, "end")

    def clear_task_view(self):
        self.clear_treeviews()

    def load_from_api(self):
        """Tải tasks từ API và thêm vào TaskManager như task API"""
        if not self.task_manager:
            messagebox.showerror("Lỗi", "TaskManager chưa khởi tạo!")
            return
            
        api_url = "https://jsonplaceholder.typicode.com/todos"
        limit = 10
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            todos = response.json()[:limit]

            added_count = 0
            current_date = datetime.now().strftime("%d-%m-%Y")
            
            for item in todos:
                title = item.get("title", "").strip()
                if not title:
                    continue
                    
                # Tạo task với đầy đủ thông tin
                content = f"Task từ API - ID: {item.get('id', 'N/A')}\nUser ID: {item.get('userId', 'N/A')}"
                priority = "Trung bình"  # Mặc định cho API tasks
                status = "Hoàn thành" if item.get("completed", False) else "Đang chờ"
                
                # Thêm task vào TaskManager (sẽ tự động tạo task_id)
                new_task = self.task_manager.add_task(
                    title=title,
                    content=content,
                    created_date=current_date,
                    priority=priority,
                    status=status
                )
                
                if new_task:
                    # Đánh dấu là API task
                    new_task.source = "api"
                    added_count += 1

            # Refresh view để hiển thị các task mới
            self.refresh_view()
            
            messagebox.showinfo("Thành công", 
                              f"Đã tải và thêm {added_count} task từ API!\n"
                              f"Các task này xuất hiện ở cột bên phải và có thể xem chi tiết, chỉnh sửa như task bình thường.")

        except requests.RequestException as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối API:\n{e}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi xử lý dữ liệu API:\n{e}")