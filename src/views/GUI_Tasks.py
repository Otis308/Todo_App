import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from src.controllers.task_controller import TaskController

class TaskDialog(tk.Toplevel):
    def __init__(self, parent, task=None, categories=None):
        super().__init__(parent)
        self.parent = parent
        self.task = task
        self.categories = categories or ["All Tasks"]
        self.result = None

        self.title("Thêm Task Mới" if not task else "Chỉnh Sửa Task")
        self.geometry("500x450")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        self.center_window()

        if task:
            self.load_task_data()

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (450 // 2)
        self.geometry(f"500x450+{x}+{y}")

    def create_widgets(self):
        main_frame = tk.Frame(self, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="📝 THÔNG TIN TASK", font=("Arial", 16, "bold"), fg="#4A90E2", bg='white').pack(pady=(0, 20))
        tk.Label(main_frame, text="Tiêu đề:", font=("Arial", 11, "bold"), bg='white').pack(anchor='w')
        self.title_entry = tk.Entry(main_frame, font=("Arial", 11), width=50)
        self.title_entry.pack(fill=tk.X, pady=(5, 15))

        tk.Label(main_frame, text="Mô tả:", font=("Arial", 11, "bold"), bg='white').pack(anchor='w')
        self.desc_text = tk.Text(main_frame, height=4, font=("Arial", 11))
        self.desc_text.pack(fill=tk.X, pady=(5, 15))

        row_frame = tk.Frame(main_frame, bg='white')
        row_frame.pack(fill=tk.X, pady=(0, 15))

        priority_frame = tk.Frame(row_frame, bg='white')
        priority_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(priority_frame, text="Độ ưu tiên:", font=("Arial", 11, "bold"), bg='white').pack(anchor='w')
        self.priority_var = tk.StringVar(value="Thấp")
        ttk.Combobox(priority_frame, textvariable=self.priority_var, values=["Thấp", "Trung bình", "Cao"], state="readonly").pack(fill=tk.X, pady=(5, 0))

        status_frame = tk.Frame(row_frame, bg='white')
        status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        tk.Label(status_frame, text="Trạng thái:", font=("Arial", 11, "bold"), bg='white').pack(anchor='w')
        self.status_var = tk.StringVar(value="Đang chờ")
        ttk.Combobox(status_frame, textvariable=self.status_var, values=["Đang chờ", "Đang tiến hành", "Hoàn thành"], state="readonly").pack(fill=tk.X, pady=(5, 0))

        tk.Label(main_frame, text="Thư mục:", font=("Arial", 11, "bold"), bg='white').pack(anchor='w')
        self.category_var = tk.StringVar(value="All Tasks")
        ttk.Combobox(main_frame, textvariable=self.category_var, values=list(self.categories), state="readonly").pack(fill=tk.X, pady=(5, 20))

        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        tk.Button(btn_frame, text="✅ Tạo", command=self.create_task, bg='#5CB85C', fg='white', font=("Arial", 11, "bold"), padx=20, pady=8).pack(side=tk.RIGHT, padx=(10, 0))
        tk.Button(btn_frame, text="💾 Lưu", command=self.save_task, bg='#5BC0DE', fg='white', font=("Arial", 11, "bold"), padx=20, pady=8).pack(side=tk.RIGHT, padx=(10, 0))
        tk.Button(btn_frame, text="❌ Hủy", command=self.destroy, bg='#D9534F', fg='white', font=("Arial", 11, "bold"), padx=20, pady=8).pack(side=tk.RIGHT)

    def load_task_data(self):
        if self.task:
            self.title_entry.insert(0, self.task.title)
            self.desc_text.insert('1.0', getattr(self.task, 'description', ''))
            self.priority_var.set(self.task.priority)
            self.status_var.set(self.task.status)
            self.category_var.set(getattr(self.task, 'category', 'All Tasks'))

    def create_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Lỗi", "Vui lòng nhập tiêu đề!")
            return
        self.result = {
            'title': title,
            'description': self.desc_text.get('1.0', tk.END).strip(),
            'priority': self.priority_var.get(),
            'status': self.status_var.get(),
            'category': self.category_var.get(),
            'action': 'create'
        }
        self.destroy()

    def save_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Lỗi", "Vui lòng nhập tiêu đề!")
            return
        self.result = {
            'title': title,
            'description': self.desc_text.get('1.0', tk.END).strip(),
            'priority': self.priority_var.get(),
            'status': self.status_var.get(),
            'category': self.category_var.get(),
            'action': 'save'
        }
        self.destroy()

class TaskManagerApp(tk.Frame):
    def __init__(self, parent, controller, user_id=None):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.task_controller = None
        self.current_user_email = None
        self.filtered_manual_tasks = []
        self.search_text = ""
        self.current_category = "All Tasks"
        self.categories = {
            "All Tasks": {"icon": "📋", "tasks": []},
            "Work": {"icon": "💼", "tasks": []},
            "Personal": {"icon": "🏠", "tasks": []},
            "Projects": {"icon": "📁", "tasks": []},
            "Ideas": {"icon": "💡", "tasks": []},
            "Shopping": {"icon": "🛒", "tasks": []},
            "Health": {"icon": "🏥", "tasks": []},
            "Learning": {"icon": "📚", "tasks": []}
        }
        self.create_widgets()

    def initialize_user(self, email):
        self.current_user_email = email
        if hasattr(self, "user_label"):
            self.user_label.config(text=f"👤 {email}")
        self.task_controller = TaskController(email)
        self.refresh_view()

    # =================== GUI Layout ===================
    def create_widgets(self):
        # Main title
        title_frame = tk.Frame(self, bg='white')
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = tk.Label(title_frame, text="🎯TASK MANAGER", 
                              font=("Quantico", 40, "bold"), fg="#D52C12", bg='white')
        title_label.pack()
        
        main_frame = tk.Frame(self, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.create_toolbar(main_frame)

        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        content_frame.grid_columnconfigure(0, weight=1)  # Sidebar
        content_frame.grid_columnconfigure(1, weight=2)  # Task area gets more space
        content_frame.grid_rowconfigure(0, weight=1)

        self.create_sidebar(content_frame)  # Left side (column 0)
        self.create_manual_tasks_section(content_frame)  # Right side (column 1)
        self.create_control_frame(main_frame)

    # =================== Toolbar ===================
    def create_toolbar(self, parent):
        toolbar_frame = tk.Frame(parent, bg='#F8F9FA', relief='solid', bd=1)
        toolbar_frame.pack(fill=tk.X, pady=10)
        
        # Inner frame for padding
        inner_frame = tk.Frame(toolbar_frame, bg='#F8F9FA')
        inner_frame.pack(fill=tk.X, padx=10, pady=10)

        # Smaller button style
        btn_style = {
            "relief": "solid",
            "borderwidth": 1,
            "font": ("Arial", 11, "bold"), 
            "padx": 4,
            "pady": 3,
            "fg": "black" 
        }
        # Create grid layout for even spacing
        inner_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        inner_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        inner_frame.grid_columnconfigure(2, weight=1, uniform="group1")
        inner_frame.grid_columnconfigure(3, weight=1, uniform="group1")
        inner_frame.grid_columnconfigure(4, weight=1, uniform="group1")
        inner_frame.grid_columnconfigure(5, weight=1, uniform="group1")
        inner_frame.grid_columnconfigure(6, weight=2, uniform="group2")  # Search gets more space

        # CRUD Buttons - lighter colors, bold text
        btn_add = tk.Button(inner_frame, text="➕ Thêm", bg='#D4EDDA',
                           command=self.add_task, **btn_style)
        btn_add.grid(row=0, column=0, padx=3, sticky="ew")

        btn_update = tk.Button(inner_frame, text="✏️ Sửa", bg='#FFF3CD', 
                              command=self.edit_manual_task, **btn_style)
        btn_update.grid(row=0, column=1, padx=3, sticky="ew")

        btn_delete = tk.Button(inner_frame, text="🗑️ Xóa", bg='#F8D7DA',
                              command=self.delete_selected_tasks, **btn_style)
        btn_delete.grid(row=0, column=2, padx=3, sticky="ew")

        # Sort (changed from "Độ ưu tiên")
        self.sort_var = tk.StringVar(value="Sắp xếp")
        sort_menu = ttk.Combobox(inner_frame, textvariable=self.sort_var,
                                values=["Độ ưu tiên", "Ngày tạo", "Trạng thái"],
                                state="readonly", font=("Arial", 9))
        sort_menu.grid(row=0, column=3, padx=3, sticky="ew")
        sort_menu.bind("<<ComboboxSelected>>", lambda e: self.sort_tasks())

        # Filter (changed from "Tất cả")
        self.filter_var = tk.StringVar(value="Lọc")
        filter_menu = ttk.Combobox(inner_frame, textvariable=self.filter_var,
                                  values=["Hoàn thành", "Đang tiến hành", "Đang chờ"],
                                  state="readonly", font=("Arial", 9))
        filter_menu.grid(row=0, column=4, padx=3, sticky="ew")
        filter_menu.bind("<<ComboboxSelected>>", lambda e: self.filter_tasks())

        # Refresh button - smaller, lighter color, bold text
        btn_refresh = tk.Button(inner_frame, text="🔄 Làm mới",
                               command=self.refresh_view, bg='#E2F3F5',
                               relief="solid", borderwidth=1, font=("Arial", 10, "bold"), 
                               padx=8, pady=6)
        btn_refresh.grid(row=0, column=5, padx=3, sticky="ew")

        # Search - no gap between input and button
        search_frame = tk.Frame(inner_frame, bg='#F8F9FA')
        search_frame.grid(row=0, column=6, padx=3, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        search_inner = tk.Frame(search_frame, relief='solid', bd=1, bg='white')
        search_inner.pack(fill=tk.X)
        
        tk.Label(search_inner, text="🔍", bg='white', font=("Arial", 11)).pack(side=tk.LEFT, padx=(6, 3))
        
        self.search_entry = tk.Entry(search_inner, font=("Arial", 10), bg='white', relief='flat')
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=3)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        search_btn = tk.Button(search_inner, text="Tìm", bg='#007BFF', fg='white',
                              font=("Arial", 9, "bold"), relief='flat', padx=8,
                              command=self.search_tasks)
        search_btn.pack(side=tk.RIGHT)  # Removed padding to eliminate gap

    # =================== Sidebar Creation (Left Side) ===================
    def create_sidebar(self, parent):
        sidebar_frame = tk.LabelFrame(parent, text="📂 THƯ MỤC", 
                                    font=("Arial", 14, "bold"), 
                                    fg="#4A90E2", bg='#F8F9FA', 
                                    relief="solid", bd=1)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        sidebar_frame.grid_columnconfigure(0, weight=1)
        sidebar_frame.grid_rowconfigure(1, weight=1)

        # Category management buttons - lighter colors like main toolbar
        btn_frame = tk.Frame(sidebar_frame, bg='#F8F9FA')
        btn_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=8)
        
        btn_style = {"font": ("Arial", 9, "bold"), "relief": "solid", "borderwidth": 1, "padx": 6, "pady": 3}
        
        add_cat_btn = tk.Button(btn_frame, text="➕ Thêm", 
                               command=self.add_category,
                               bg='#D4EDDA', **btn_style)
        add_cat_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        edit_cat_btn = tk.Button(btn_frame, text="✏️ Sửa", 
                                command=self.edit_category,
                                bg='#FFF3CD',**btn_style)
        edit_cat_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        del_cat_btn = tk.Button(btn_frame, text="🗑️ Xóa", 
                               command=self.delete_category,
                               bg='#F8D7DA', **btn_style)
        del_cat_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        # Categories list with scrollbar - increased spacing
        list_frame = tk.Frame(sidebar_frame, bg='#F8F9FA')
        list_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        self.category_listbox = tk.Listbox(list_frame, 
                                         font=("Arial", 11),
                                         selectmode=tk.SINGLE,
                                         bg='white',
                                         selectbackground='#4A90E2',
                                         selectforeground='white',
                                         activestyle='none',
                                         relief='solid', bd=1)
        self.category_listbox.grid(row=0, column=0, sticky="nsew")
        self.category_listbox.bind('<<ListboxSelect>>', self.on_category_select)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
                                command=self.category_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.category_listbox.configure(yscrollcommand=scrollbar.set)

        # Task count info
        self.category_info_label = tk.Label(sidebar_frame, 
                                          text="📊 Chọn thư mục để xem task",
                                          font=("Arial", 10, "italic"),
                                          bg='#F8F9FA', fg='#666')
        self.category_info_label.grid(row=2, column=0, sticky="ew", padx=8, pady=8)

        self.populate_categories()

    # =================== Task Sections (Right Side) ===================
    def create_manual_tasks_section(self, parent):
        self.tree_manual = self._create_tree_frame(parent, 1, "📝 DANH SÁCH TASK", "#4A90E2")

    def _create_tree_frame(self, parent, col, title, color):
        frame = tk.LabelFrame(parent, text=title, font=("Arial", 14, "bold"), 
                             fg=color, bg='white', relief="solid", bd=1)
        frame.grid(row=0, column=col, sticky="nsew", padx=(10, 0))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        # Removed description column, added checkbox column
        tree = ttk.Treeview(frame, columns=("checkbox", "title", "created_date", "priority", "status"), 
                           show="headings", height=20)
        tree.grid(row=0, column=0, sticky="nsew")
        
        # Configure columns
        columns_config = [
            ("checkbox", "☑", 40),  # Checkbox column
            ("title", "Tiêu đề", 250),
            ("created_date", "Ngày tạo", 100),
            ("priority", "Độ ưu tiên", 100),
            ("status", "Trạng thái", 120)
        ]
        
        for col_id, text, width in columns_config:
            tree.heading(col_id, text=text)
            tree.column(col_id, width=width, anchor="w")
        
        # Bind double-click to show task details
        tree.bind("<Double-1>", self.on_task_double_click)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)
        
        return tree

    def on_task_double_click(self, event):
        """Show task details on double click"""
        selected = self.tree_manual.selection()
        if not selected:
            return
        
        task_item = selected[0]
        task_tags = self.tree_manual.item(task_item, "tags")
        if not task_tags:
            return
            
        task_id = task_tags[0]
        
        # Find the task
        task = None
        for t in self.task_controller.list_tasks():
            if t.task_id == task_id:
                task = t
                break
        
        if task:
            # Show task details dialog
            details = f"""Tiêu đề: {task.title}
            
Mô tả: {getattr(task, 'description', 'Không có mô tả')}

Độ ưu tiên: {task.priority}
Trạng thái: {task.status}
Thư mục: {getattr(task, 'category', 'All Tasks')}
Ngày tạo: {task.created_date}"""
            
            messagebox.showinfo("Chi tiết Task", details)

    # =================== Sidebar Functions ===================
    def populate_categories(self):
        self.category_listbox.delete(0, tk.END)
        for category, data in self.categories.items():
            task_count = len(data.get("tasks", []))
            display_text = f"{data['icon']} {category} ({task_count})"
            self.category_listbox.insert(tk.END, display_text)
        
        if self.category_listbox.size() > 0:
            self.category_listbox.selection_set(0)
            self.on_category_select(None)

    def on_category_select(self, event):
        selection = self.category_listbox.curselection()
        if selection:
            index = selection[0]
            category_name = list(self.categories.keys())[index]
            self.current_category = category_name
            self.filter_tasks_by_category()
            
            task_count = len(self.categories[category_name].get("tasks", []))
            self.category_info_label.config(
                text=f"📊 {category_name}: {task_count} tasks"
            )

    def filter_tasks_by_category(self):
        if not self.task_controller:
            return
            
        all_tasks = self.task_controller.list_tasks() or []
        
        if self.current_category == "All Tasks":
            self.filtered_manual_tasks = [t for t in all_tasks if getattr(t, 'source', 'manual') == 'manual']
        else:
            assigned_task_ids = self.categories[self.current_category].get("tasks", [])
            self.filtered_manual_tasks = [
                t for t in all_tasks 
                if getattr(t, 'source', 'manual') == 'manual' and 
                getattr(t, 'task_id', None) in assigned_task_ids
            ]
        
        self.apply_filters_and_search()

    def add_category(self):
        name = simpledialog.askstring("Thêm thư mục mới", "Tên thư mục:")
        if name and name.strip():
            name = name.strip()
            if name not in self.categories:
                icons = ["📋", "💼", "🏠", "📁", "💡", "🛒", "🏥", "📚", "⭐", "🎯", "🔥", "📝"]
                icon = simpledialog.askstring("Chọn icon", 
                                            f"Chọn icon:\n{' '.join(icons)}\n(Mặc định: 📋)")
                if not icon or icon not in icons:
                    icon = "📋"
                    
                self.categories[name] = {"icon": icon, "tasks": []}
                self.populate_categories()
                messagebox.showinfo("Thành công", f"Đã thêm thư mục '{name}'")
            else:
                messagebox.showwarning("Lỗi", "Tên thư mục đã tồn tại!")

    def edit_category(self):
        selection = self.category_listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thư mục để sửa!")
            return
            
        index = selection[0]
        old_name = list(self.categories.keys())[index]
        
        if old_name == "All Tasks":
            messagebox.showwarning("Cảnh báo", "Không thể sửa thư mục 'All Tasks'!")
            return
            
        new_name = simpledialog.askstring("Sửa tên thư mục", "Tên mới:", initialvalue=old_name)
        if new_name and new_name.strip() and new_name != old_name:
            new_name = new_name.strip()
            if new_name not in self.categories:
                self.categories[new_name] = self.categories[old_name]
                del self.categories[old_name]
                self.populate_categories()
                messagebox.showinfo("Thành công", f"Đã đổi tên từ '{old_name}' thành '{new_name}'")
            else:
                messagebox.showwarning("Lỗi", "Tên thư mục đã tồn tại!")

    def delete_category(self):
        selection = self.category_listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thư mục để xóa!")
            return
            
        index = selection[0]
        category_name = list(self.categories.keys())[index]
        
        if category_name == "All Tasks":
            messagebox.showwarning("Cảnh báo", "Không thể xóa thư mục 'All Tasks'!")
            return
            
        task_count = len(self.categories[category_name].get("tasks", []))
        if messagebox.askyesno("Xác nhận xóa", 
                              f"Bạn có chắc muốn xóa thư mục '{category_name}'?\n"
                              f"Thư mục này có {task_count} tasks (tasks sẽ chuyển về 'All Tasks')."):
            # Move tasks back to All Tasks
            for task_id in self.categories[category_name].get("tasks", []):
                for task in self.task_controller.list_tasks():
                    if task.task_id == task_id:
                        task.category = "All Tasks"
            
            del self.categories[category_name]
            self.populate_categories()
            messagebox.showinfo("Thành công", f"Đã xóa thư mục '{category_name}'")

    # =================== Control / Status ===================
    def create_control_frame(self, parent):
        control_frame = tk.Frame(parent, bg='white', height=50)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        control_frame.pack_propagate(False)

        left_frame = tk.Frame(control_frame, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.user_label = tk.Label(left_frame, text=f"👤 {self.current_user_email or ''}",
                                   bg='white', fg='#4A90E2', font=('Arial', 12, 'bold'))
        self.user_label.pack(side=tk.LEFT, anchor='w')

        tk.Button(left_frame, text="↩ Đăng xuất", command=self.logout,
                  bg='#FFE6E6', fg='#D9534F', font=('Arial', 10, 'bold'), 
                  relief="solid", borderwidth=1, padx=15, pady=5).pack(side=tk.LEFT, padx=(20,0))

        right_frame = tk.Frame(control_frame, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.count_label = tk.Label(right_frame, text="📝 Tasks: 0",
                                    font=('Arial', 12, 'bold'), bg='white', fg='#666666')
        self.count_label.pack(side=tk.RIGHT, anchor='e')

    # =================== Refresh / Populate ===================
    def refresh_view(self):
        if not self.task_controller:
            return
        all_tasks = self.task_controller.list_tasks() or []
        # Lọc task thủ công
        self.filtered_manual_tasks = [t for t in all_tasks if getattr(t, 'source', 'manual') == 'manual']
        self.filter_tasks_by_category()
        self.populate_categories()

    def populate_trees(self):
        self.tree_manual.delete(*self.tree_manual.get_children())
        for t in self.filtered_manual_tasks:
            # Add checkbox symbol based on completion status
            checkbox = "☑" if getattr(t, 'completed', False) else "☐"
            self.tree_manual.insert("", "end", tags=(t.task_id,), 
                                   values=(checkbox, t.title, t.created_date, t.priority, t.status))

    def update_status_display(self):
        total_tasks = len(self.task_controller.list_tasks()) if self.task_controller else 0
        filtered_tasks = len(self.filtered_manual_tasks)
        self.count_label.config(text=f"📝 Tasks: {filtered_tasks}/{total_tasks}")

    # =================== Task Actions ===================
    def add_task(self):
        dialog = TaskDialog(self, categories=list(self.categories.keys()))
        self.wait_window(dialog)
        
        if dialog.result and dialog.result.get('action') == 'create':
            task = self.task_controller.create_task(
                title=dialog.result['title'],
                description=dialog.result['description'],
                priority=dialog.result['priority'],
                status=dialog.result['status'],
                category=dialog.result['category']
            )
            category = dialog.result['category']
            if category != "All Tasks" and category in self.categories:
                if "tasks" not in self.categories[category]:
                    self.categories[category]["tasks"] = []
                self.categories[category]["tasks"].append(task.task_id)
            self.refresh_view()
            messagebox.showinfo("Thành công", "Đã tạo task mới!")

    def edit_manual_task(self):
        selected = self.tree_manual.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn task để sửa!")
            return
        
        # Get task ID from tree tags
        task_item = selected[0]
        task_tags = self.tree_manual.item(task_item, "tags")
        if not task_tags:
            return
            
        task_id = task_tags[0]
        
        # Find the task
        task = None
        for t in self.task_controller.list_tasks():
            if t.task_id == task_id:
                task = t
                break
        
        if not task:
            messagebox.showerror("Lỗi", "Không tìm thấy task!")
            return
        
        dialog = TaskDialog(self, task=task, categories=list(self.categories.keys()))
        self.wait_window(dialog)
        
        if dialog.result:
            old_category = getattr(task, 'category', 'All Tasks')
            new_category = dialog.result['category']
            self.task_controller.update_task(
                task_id,
                title=dialog.result['title'],
                description=dialog.result['description'],
                priority=dialog.result['priority'],
                status=dialog.result['status'],
                category=new_category
            )
            if old_category != new_category:
                if old_category in self.categories and task_id in self.categories[old_category].get("tasks", []):
                    self.categories[old_category]["tasks"].remove(task_id)
                if new_category != "All Tasks" and new_category in self.categories:
                    if "tasks" not in self.categories[new_category]:
                        self.categories[new_category]["tasks"] = []
                    if task_id not in self.categories[new_category]["tasks"]:
                        self.categories[new_category]["tasks"].append(task_id)
            self.refresh_view()
            messagebox.showinfo("Thành công", "Đã cập nhật task!")

    def delete_selected_tasks(self):
        selected = self.tree_manual.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn task để xóa!")
            return
        
        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa {len(selected)} task(s)?"):
            for task_item in selected:
                task_tags = self.tree_manual.item(task_item, "tags")
                if task_tags:
                    task_id = task_tags[0]
                    
                    # Remove from categories
                    for category_data in self.categories.values():
                        if task_id in category_data.get("tasks", []):
                            category_data["tasks"].remove(task_id)
                    
                    # Remove from task manager
                    self.task_controller.delete_task(task_id)
            
            self.refresh_view()
            messagebox.showinfo("Thành công", f"Đã xóa {len(selected)} task(s)!")

    def sort_tasks(self):
        if not self.filtered_manual_tasks:
            return
        
        sort_by = self.sort_var.get()
        
        if sort_by == "Độ ưu tiên":
            priority_order = {"Cao": 0, "Trung bình": 1, "Thấp": 2}
            self.filtered_manual_tasks.sort(key=lambda t: priority_order.get(t.priority, 3))
        elif sort_by == "Ngày tạo":
            self.filtered_manual_tasks.sort(key=lambda t: datetime.strptime(t.created_date, "%d/%m/%Y"), reverse=True)
        elif sort_by == "Tên":
            self.filtered_manual_tasks.sort(key=lambda t: t.title.lower())
        elif sort_by == "Trạng thái":
            status_order = {"Đang tiến hành": 0, "Đang chờ": 1, "Hoàn thành": 2}
            self.filtered_manual_tasks.sort(key=lambda t: status_order.get(t.status, 3))
        
        self.populate_trees()

    def filter_tasks(self):
        self.apply_filters_and_search()

    def apply_filters_and_search(self):
        if not self.task_controller:
            return
        
        # Start with category filtered tasks
        if self.current_category == "All Tasks":
            tasks = [t for t in self.task_controller.list_tasks() if getattr(t, 'source', 'manual') == 'manual']
        else:
            assigned_task_ids = self.categories[self.current_category].get("tasks", [])
            tasks = [
                t for t in self.task_controller.list_tasks() 
                if getattr(t, 'source', 'manual') == 'manual' and 
                getattr(t, 'task_id', None) in assigned_task_ids
            ]
        
        # Apply status filter
        status_filter = self.filter_var.get()
        if status_filter != "Lọc" and status_filter != "Tất cả":
            tasks = [t for t in tasks if t.status == status_filter]
        
        # Apply search filter
        if self.search_text:
            search_lower = self.search_text.lower()
            tasks = [t for t in tasks if 
                    search_lower in t.title.lower() or 
                    search_lower in getattr(t, 'description', '').lower()]
        
        self.filtered_manual_tasks = tasks
        self.populate_trees()
        self.update_status_display()

    def on_search_change(self, event):
        self.search_text = self.search_entry.get().strip()
        if len(self.search_text) >= 2 or self.search_text == "":
            self.apply_filters_and_search()

    def search_tasks(self):
        self.search_text = self.search_entry.get().strip()
        self.apply_filters_and_search()

    # =================== Logout ===================
    def logout(self):
        if messagebox.askyesno("Đăng xuất", f"Bạn có chắc chắn muốn đăng xuất {self.current_user_email}?"):
            self.controller.current_user_email = None
            if self.task_controller:
                self.task_controller.tasks.clear()
            self.filtered_manual_tasks.clear()
            self.tree_manual.delete(*self.tree_manual.get_children())
            self.user_label.config(text="")
            self.search_entry.delete(0, tk.END)
            if hasattr(self.controller, 'show_login'):
                self.controller.show_login()