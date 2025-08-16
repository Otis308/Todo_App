
# import tkinter as tk
# from tkinter import *
# from datetime import datetime
# import json, uuid, os

# DATA_FILE = "tasks.json"
# DATE_FMT = "%d%m%Y"

# def load_tasks():
#     if not os.path.exists(DATA_FILE):
#         return []
#     try:
#         with open(DATA_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             return data
#     except Exception as e:
#         print("Failed to load tasks:", e)
#         return []


# def save_tasks(tasks):
#     try:
#         with open(DATA_FILE, "w", encoding="utf-8") as f:
#             json.dump(tasks, f, ensure_ascii=False, indent=2)
#     except Exception as e:
#         print("Failed to save tasks:", e)

import tkinter as tk
import json, uuid, os, logging
from tkinter import ttk, messagebox, simpledialog, filedialog, font
from datetime import datetime
from tkcalendar import DateEntry
from src.models.task import User, Task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATE_FMT = "%d-%m-%Y"

class TaskManager:
    def __init__(self, user):
        self.user = user
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file"""
        try:
            if os.path.exists(self.user.get_task_file_path()):
                with open(self.user.get_task_file_path(), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
                logger.info(f"Loaded {len(self.tasks)} tasks for user {self.user.username}")
            else:
                self.tasks = []
                logger.info(f"No existing tasks file for user {self.user.username}")
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self, file_path=None):
        """Save tasks to file"""
        try:
            save_path = file_path or self.user.get_task_file_path()
            task_data = [task.to_dict() for task in self.tasks]
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(task_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(self.tasks)} tasks to {save_path}")
            return save_path
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")
            raise
    
    def add_task(self, task):
        """Add a new task"""
        self.tasks.append(task)
        self.save_tasks()
    
    def update_task(self, task_id, **kwargs):
        """Update a task"""
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    setattr(task, key, value)
                task.completed = (task.status == "Hoàn thành")
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id):
        """Delete a task"""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
    
    def find_task(self, task_id):
        """Find a task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def export_to_json(self, file_path):
        """Export tasks to JSON file"""
        return self.save_tasks(file_path)

class LoginDialog(simpledialog.Dialog):
    """Simple login dialog"""
    def __init__(self, parent):
        super().__init__(parent, "Đăng nhập")
    
    def body(self, master):
        self.after(0, lambda: self.geometry("300x150+500+300"))
        
        ttk.Label(master, text="Tên đăng nhập:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(master, textvariable=self.username_var, width=20)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        return self.username_entry
    
    def validate(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên đăng nhập")
            return False
        return True
    
    def apply(self):
        self.result = self.username_var.get().strip()

class TaskDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, task=None):
        self.task = task
        super().__init__(parent, title=title)

    def body(self, master):
        self.after(0, lambda: self.geometry("500x300+530+215"))        
        roboto_font = font.Font(family="Roboto", size=50)
        ttk.Label(master, text="Chủ đề:",  font=(roboto_font, 11)).grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar(value=(self.task.title if self.task else ""))
        self.title_entry = ttk.Entry(master, textvariable=self.title_var)
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=10)

        ttk.Label(master, text="Mô tả công việc:", font=(roboto_font, 11)).grid(row=1, column=0, sticky="nw")
        self.desc_text = tk.Text(master, height=6, width=45)
        if self.task:
            self.desc_text.insert("1.0", self.task.description)
        self.desc_text.grid(row=1, column=1, sticky="ew", padx=5, pady=8)

        ttk.Label(master, text="Ngày thiết lập: ", font=(roboto_font, 11)).grid(row=2, column=0, sticky="w")
        self.due_var = tk.StringVar(value=(self.task.due if self.task else ""))
        cal = DateEntry(master, textvariable=self.due_var, date_pattern="dd-mm-yyyy",
                        background='darkblue', foreground='white', borderwidth=2)
        cal.grid(row=2, column=1, sticky="w", padx=5,pady=10)

        ttk.Label(master, text="Mức độ ưu tiên: ", font=(roboto_font, 11)).grid(row=3, column=0, sticky="w")
        self.prio_var = tk.IntVar(value=(self.task.priority if self.task else 2))
        prio_spin = ttk.Spinbox(master, from_=1, to=3, textvariable=self.prio_var, width=5)
        prio_spin.grid(row=3, column=1, sticky="w", padx=5,pady=10)

        master.columnconfigure(1, weight=1)
        return self.title_entry

    def validate(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Title cannot be empty")
            return False
        due = self.due_var.get().strip()
        if due:
            try:
                datetime.strptime(due, DATE_FMT)
            except Exception:
                messagebox.showwarning("Validation", f"Due date must be in DD-MM-YYYY format")
                return False
        return True

    def apply(self):
        self.result = Task(
            title=self.title_var.get().strip(),
            description=self.desc_text.get("1.0", "end").strip(),
            due=self.due_var.get().strip(),
            priority=int(self.prio_var.get()),
            status=self.task.status if self.task else "Đang chờ",
            task_id=self.task.id if self.task else None
        )

class LoginFrame(tk.Frame):
    """Login frame for multi-frame application"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        # Center the login form
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        login_frame = tk.Frame(self, bg='white', relief='solid', bd=1)
        login_frame.grid(row=1, column=1, padx=50, pady=50, sticky='nsew')
        
        # Title
        title_label = tk.Label(login_frame, text="NOTION", font=('Arial', 24, 'bold'), bg='white')
        title_label.pack(pady=20)
        
        # Login form
        form_frame = tk.Frame(login_frame, bg='white')
        form_frame.pack(padx=40, pady=20)
        
        tk.Label(form_frame, text="Tên đăng nhập:", bg='white', font=('Arial', 12)).pack(anchor='w', pady=(0, 5))
        self.username_var = tk.StringVar()
        username_entry = tk.Entry(form_frame, textvariable=self.username_var, font=('Arial', 12), width=25)
        username_entry.pack(pady=(0, 15))
        username_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_btn = tk.Button(form_frame, text="Đăng nhập", command=self.login, 
                             bg='#007bff', fg='white', font=('Arial', 12), padx=20, pady=5)
        login_btn.pack(pady=10)
        
        username_entry.focus()
    
    def login(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên đăng nhập")
            return
        
        user = User(username)
        self.controller.set_user(user)
        self.controller.show_frame("TaskFrame")

class TaskFrame(tk.Frame):
    """Task management frame"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")  
        self.controller = controller
        self.user = None
        self.task_manager = None

        self.status_colors = {
            "Hoàn thành": "#28a745",  
            "Đang tiến hành": "#007bff",   
            "Đang chờ": "#dc3545"  
        }
        
        self.create_widgets()
        
    def set_user(self, user):
        """Set user and initialize task manager"""
        self.user = user
        self.task_manager = TaskManager(self.user)
        self.user_label.config(text=f"Người dùng: {self.user.username}")
        self.refresh_tree()

    def create_widgets(self):
        # Top frame for buttons and search
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=6)
        
        # Configure columns
        for c in range(8):
            top_frame.columnconfigure(c, weight=1)

        # Buttons
        add_btn = ttk.Button(top_frame, text="Thêm công việc", command=self.add_task)
        add_btn.grid(row=0, column=0, padx=4, pady=2, sticky="ew")

        edit_btn = ttk.Button(top_frame, text="Chỉnh sửa", command=self.edit_task)
        edit_btn.grid(row=0, column=1, padx=4, pady=2, sticky="ew")

        del_btn = ttk.Button(top_frame, text="Xóa công việc", command=self.delete_task)
        del_btn.grid(row=0, column=2, padx=4, pady=2, sticky="ew")

        # Status change menu button
        self.status_menu_btn = ttk.Menubutton(top_frame, text="Thay đổi trạng thái")
        self.status_menu_btn.grid(row=0, column=3, padx=4, pady=2, sticky="ew")
        
        self.status_menu = tk.Menu(self.status_menu_btn, tearoff=0)
        self.status_menu_btn['menu'] = self.status_menu
        
        for status, color in self.status_colors.items():
            self.status_menu.add_command(label=status, 
                                       command=lambda s=status: self.change_task_status(s),
                                       foreground=color)

        # Search
        ttk.Label(top_frame, text="Tìm kiếm:").grid(row=0, column=4, sticky="e", padx=(12, 2))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=5, sticky="ew", padx=(0, 8))
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_tree())

        # User info
        self.user_label = ttk.Label(top_frame, text="Người dùng: ")
        self.user_label.grid(row=0, column=6, sticky="e", padx=8)

        # Logout button
        logout_btn = ttk.Button(top_frame, text="Đăng xuất", command=self.logout)
        logout_btn.grid(row=0, column=7, padx=4, pady=2, sticky="ew")

        # Treeview with colored status
        cols = ("title", "due", "priority", "status")
        self.tree = ttk.Treeview(self, columns=cols, show='headings', selectmode='browse')
        self.tree.heading('title', text='Chủ đề')
        self.tree.heading('due', text='Ngày thiết lập')
        self.tree.heading('priority', text='Độ ưu tiên')
        self.tree.heading('status', text='Trạng thái')

        self.tree.column('title', width=380, anchor='w')
        self.tree.column('due', width=120, anchor='center')
        self.tree.column('priority', width=100, anchor='center')
        self.tree.column('status', width=120, anchor='center')

        self.tree.grid(row=1, column=0, sticky="nsew", padx=8, pady=6)
        self.tree.bind('<Double-1>', lambda e: self.view_details())
        self.tree.bind('<Button-1>', self.on_tree_click)

        # Bottom frame
        bottom = ttk.Frame(self)
        bottom.grid(row=2, column=0, sticky="ew", padx=8, pady=6)
        bottom.columnconfigure(3, weight=1)

        save_btn = ttk.Button(bottom, text='Lưu', command=self.save_tasks)
        save_btn.grid(row=0, column=0, sticky="w")

        export_btn = ttk.Button(bottom, text='Xuất JSON', command=self.export_json)
        export_btn.grid(row=0, column=1, sticky="w", padx=6)

        save_as_btn = ttk.Button(bottom, text='Lưu thành...', command=self.save_as)
        save_as_btn.grid(row=0, column=2, sticky="w", padx=6)

        self.count_label = ttk.Label(bottom, text='0 công việc')
        self.count_label.grid(row=0, column=3, sticky="e")

        # Configure grid weights
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Initialize filter variables
        self.filter_var = tk.StringVar(value="Tất cả")
        self.priority_filter_var = tk.StringVar(value="Tất cả")
        self.sort_var = tk.StringVar(value="Ngày thiết lập")

    def logout(self):
        """Logout current user"""
        if messagebox.askyesno("Đăng xuất", "Bạn có muốn đăng xuất không?"):
            self.controller.show_frame("LoginFrame")

    def on_tree_click(self, event):
        """Handle click on tree view"""
        item = self.tree.identify('item', event.x, event.y)
        column = self.tree.identify('column', event.x, event.y)
        
        if item and column == '#4':  # Status column
            values = self.tree.item(item, 'values')
            if len(values) >= 5:
                task_id = values[4]  # ID is now in 5th position
                self.cycle_task_status(task_id)

    def cycle_task_status(self, task_id):
        """Cycle through task statuses"""
        if not self.task_manager:
            return
            
        task = self.task_manager.find_task(task_id)
        if task:
            status_cycle = ["Đang chờ", "Đang tiến hành", "Hoàn thành"]
            current_index = status_cycle.index(task.status) if task.status in status_cycle else 0
            new_status = status_cycle[(current_index + 1) % len(status_cycle)]
            
            self.task_manager.update_task(task_id, status=new_status)
            self.refresh_tree()

    def change_task_status(self, new_status):
        """Change status of selected task"""
        item = self.tree.selection()
        if not item:
            messagebox.showinfo('Thông báo', 'Vui lòng chọn một công việc')
            return
        
        if not self.task_manager:
            return
            
        values = self.tree.item(item, 'values')
        if len(values) >= 5:
            task_id = values[4]
            self.task_manager.update_task(task_id, status=new_status)
            self.refresh_tree()

    def add_task(self):
        if not self.task_manager:
            messagebox.showwarning("Lỗi", "Vui lòng đăng nhập trước")
            return
            
        dlg = TaskDialog(self, title='Thêm công việc')
        if dlg.result:
            self.task_manager.add_task(dlg.result)
            self.refresh_tree()

    def edit_task(self):
        item = self.tree.selection()
        if not item:
            messagebox.showinfo('Chỉnh sửa', 'Vui lòng chọn một công việc để chỉnh sửa')
            return
        
        if not self.task_manager:
            return
            
        values = self.tree.item(item, 'values')
        if len(values) >= 5:
            task_id = values[4]
            task = self.task_manager.find_task(task_id)
            if task:
                dlg = TaskDialog(self, title='Chỉnh sửa công việc', task=task)
                if dlg.result:
                    self.task_manager.update_task(task_id, 
                                                title=dlg.result.title,
                                                description=dlg.result.description,
                                                due=dlg.result.due,
                                                priority=dlg.result.priority)
                    self.refresh_tree()

    def delete_task(self):
        item = self.tree.selection()
        if not item:
            messagebox.showinfo('Xóa', 'Vui lòng chọn một công việc để xóa')
            return
        
        if not messagebox.askyesno('Xác nhận', 'Xóa công việc đã chọn?'):
            return
        
        if not self.task_manager:
            return
            
        values = self.tree.item(item, 'values')
        if len(values) >= 5:
            task_id = values[4]
            self.task_manager.delete_task(task_id)
            self.refresh_tree()

    def view_details(self):
        item = self.tree.selection()
        if not item:
            return
        
        if not self.task_manager:
            return
            
        values = self.tree.item(item, 'values')
        if len(values) >= 5:
            task_id = values[4]
            task = self.task_manager.find_task(task_id)
            if task:
                details = f"Chủ đề: {task.title}\n\nMô tả:\n{task.description}\n\nNgày thiết lập: {task.due}\nĐộ ưu tiên: {task.priority}\nTrạng thái: {task.status}"
                messagebox.showinfo('Chi tiết công việc', details)

    def save_tasks(self):
        """Save tasks to default location"""
        if not self.task_manager:
            messagebox.showwarning("Lỗi", "Vui lòng đăng nhập trước")
            return
            
        try:
            self.task_manager.save_tasks()
            messagebox.showinfo('Lưu', 'Đã lưu công việc thành công!')
        except Exception as e:
            messagebox.showerror('Lỗi', f'Không thể lưu công việc: {e}')

    def save_as(self):
        """Save tasks to user-specified location"""
        if not self.task_manager:
            messagebox.showwarning("Lỗi", "Vui lòng đăng nhập trước")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Lưu công việc thành..."
        )
        
        if file_path:
            try:
                self.task_manager.save_tasks(file_path)
                messagebox.showinfo('Lưu', f'Đã lưu công việc thành công tại:\n{file_path}')
            except Exception as e:
                messagebox.showerror('Lỗi', f'Không thể lưu công việc: {e}')

    def export_json(self):
        """Export tasks to JSON file"""
        if not self.task_manager:
            messagebox.showwarning("Lỗi", "Vui lòng đăng nhập trước")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Xuất công việc ra JSON"
        )
        
        if file_path:
            try:
                self.task_manager.export_to_json(file_path)
                messagebox.showinfo('Xuất dữ liệu', f'Đã xuất công việc thành công tại:\n{file_path}')
            except Exception as e:
                messagebox.showerror('Lỗi', f'Không thể xuất công việc: {e}')

    def filter_tasks(self):
        """Filter tasks based on current filter settings"""
        if not self.task_manager:
            return []
            
        q = self.search_var.get().strip().lower()
        status_filter = self.filter_var.get()
        priority_filter = self.priority_filter_var.get()
        
        result = []
        for task in self.task_manager.tasks:
            # Text search filter
            if q:
                if q not in (task.title.lower() + ' ' + task.description.lower()):
                    continue
            
            # Status filter
            if status_filter != 'Tất cả' and task.status != status_filter:
                continue
            
            # Priority filter
            if priority_filter != 'Tất cả' and str(task.priority) != priority_filter:
                continue
            
            result.append(task)
        
        return result

    def sort_tasks(self, tasks):
        """Sort tasks based on current sort setting"""
        sort_key = self.sort_var.get()
        
        if sort_key == 'Ngày thiết lập':
            def sort_func(task):
                if not task.due:
                    return datetime.max
                try:
                    return datetime.strptime(task.due, DATE_FMT)
                except Exception:
                    return datetime.max
            tasks.sort(key=sort_func)
        elif sort_key == 'Độ ưu tiên':
            tasks.sort(key=lambda x: x.priority)
        elif sort_key == 'Chủ đề':
            tasks.sort(key=lambda x: x.title.lower())

    def refresh_tree(self):
        """Refresh the tree view with current tasks"""
        if not self.task_manager:
            return
            
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filtered and sorted tasks
        filtered_tasks = self.filter_tasks()
        self.sort_tasks(filtered_tasks)
        
        # Configure tags for colors - only status column should have colors
        for status, color in self.status_colors.items():
            self.tree.tag_configure(status, foreground='black')  # Default black for all
        
        # Insert tasks
        for task in filtered_tasks:
            values = (task.title, task.due, task.priority, task.status, task.id)
            item_id = self.tree.insert('', 'end', values=values)
            
            # Apply color only to status column
            self.tree.set(item_id, 'status', task.status)
            for col_id, col_name in enumerate(['title', 'due', 'priority', 'status'], 1):
                if col_name == 'status':
                    # Create unique tag for each status
                    tag_name = f"status_{task.status}"
                    self.tree.tag_configure(tag_name, foreground=self.status_colors.get(task.status, 'black'))
                    self.tree.item(item_id, tags=(tag_name,))
                    break
        
        # Update count
        self.count_label.config(text=f"{len(filtered_tasks)} công việc")