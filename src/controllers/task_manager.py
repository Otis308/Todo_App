
# # import tkinter as tk
# # from tkinter import *
# # from datetime import datetime
# # import json, uuid, os

# # DATA_FILE = "tasks.json"
# # DATE_FMT = "%d%m%Y"

# # def load_tasks():
# #     if not os.path.exists(DATA_FILE):
# #         return []
# #     try:
# #         with open(DATA_FILE, "r", encoding="utf-8") as f:
# #             data = json.load(f)
# #             return data
# #     except Exception as e:
# #         print("Failed to load tasks:", e)
# #         return []


# # def save_tasks(tasks):
# #     try:
# #         with open(DATA_FILE, "w", encoding="utf-8") as f:
# #             json.dump(tasks, f, ensure_ascii=False, indent=2)
# #     except Exception as e:
# #         print("Failed to save tasks:", e)

# import tkinter as tk
# import json, uuid, os, logging
# from tkinter import ttk, messagebox, simpledialog, filedialog, font
# from datetime import datetime
# from tkcalendar import DateEntry
# from src.models.task import User, Task

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# DATE_FMT = "%d-%m-%Y"

# class TaskManager:
#     def __init__(self, user):
#         self.user = user
#         self.tasks = []
#         self.load_tasks()
    
#     def load_tasks(self):
#         """Load tasks from file"""
#         try:
#             if os.path.exists(self.user.get_task_file_path()):
#                 with open(self.user.get_task_file_path(), 'r', encoding='utf-8') as f:
#                     data = json.load(f)
#                     self.tasks = [Task.from_dict(task_data) for task_data in data]
#                 logger.info(f"Loaded {len(self.tasks)} tasks for user {self.user.username}")
#             else:
#                 self.tasks = []
#                 logger.info(f"No existing tasks file for user {self.user.username}")
#         except Exception as e:
#             logger.error(f"Error loading tasks: {e}")
#             self.tasks = []
    
#     def save_tasks(self, file_path=None):
#         """Save tasks to file"""
#         try:
#             save_path = file_path or self.user.get_task_file_path()
#             task_data = [task.to_dict() for task in self.tasks]
            
#             # Create directory if it doesn't exist
#             os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
#             with open(save_path, 'w', encoding='utf-8') as f:
#                 json.dump(task_data, f, ensure_ascii=False, indent=2)
#             logger.info(f"Saved {len(self.tasks)} tasks to {save_path}")
#             return save_path
#         except Exception as e:
#             logger.error(f"Error saving tasks: {e}")
#             raise
    
#     def add_task(self, task):
#         self.tasks.append(task)
#         self.save_tasks()
    
#     def update_tasks(self, task_id, **kwargs):
#         """Update a task"""
#         for task in self.tasks:
#             if task.id == task_id:
#                 for key, value in kwargs.items():
#                     setattr(task, key, value)
#                 task.completed = (task.status == "Hoàn thành")
#                 self.save_tasks()
#                 return True
#         return False
    
#     def delete_task(self, task_id):
#         """Delete a task"""
#         self.tasks = [task for task in self.tasks if task.id != task_id]
#         self.save_tasks()
    
#     def find_task(self, task_id):
#         """Find a task by ID"""
#         for task in self.tasks:
#             if task.id == task_id:
#                 return task
#         return None
    
#     def export_to_json(self, file_path):
#         """Export tasks to JSON file"""
#         return self.save_tasks(file_path)


#     def validate(self):
#         title = self.title_var.get().strip()
#         if not title:
#             messagebox.showwarning("Validation", "Title cannot be empty")
#             return False
#         due = self.due_var.get().strip()
#         if due:
#             try:
#                 datetime.strptime(due, DATE_FMT)
#             except Exception:
#                 messagebox.showwarning("Validation", f"Due date must be in DD-MM-YYYY format")
#                 return False
#         return True

#     def apply(self):
#         self.result = Task(
#             title=self.title_var.get().strip(),
#             description=self.desc_text.get("1.0", "end").strip(),
#             due=self.due_var.get().strip(),
#             priority=int(self.prio_var.get()),
#             status=self.task.status if self.task else "Đang chờ",
#             task_id=self.task.id if self.task else None
#         )
# class TaskFrame(tk.Frame):
#     """Task management frame"""
#     def __init__(self, parent, controller):
#         super().__init__(parent, bg="white")  
#         self.controller = controller
#         self.user = None
#         self.task_manager = None

#         self.status_colors = {
#             "Hoàn thành": "#28a745",  
#             "Đang tiến hành": "#007bff",   
#             "Đang chờ": "#dc3545"  
#         }
        
#         self.create_widgets()
        
#     def set_user(self, user):
#         """Set user and initialize task manager"""
#         self.user = user
#         self.task_manager = TaskManager(self.user)
#         self.user_label.config(text=f"Người dùng: {self.user.username}")
#         self.refresh_tree()

#     def logout(self):
#         """Logout current user"""
#         if messagebox.askyesno("Đăng xuất", "Bạn có muốn đăng xuất không?"):
#             self.controller.show_frame("LoginFrame")

#     def on_tree_click(self, event):
#         """Handle click on tree view"""
#         item = self.tree.identify('item', event.x, event.y)
#         column = self.tree.identify('column', event.x, event.y)
        
#         if item and column == '#4':  # Status column
#             values = self.tree.item(item, 'values')
#             if len(values) >= 5:
#                 task_id = values[4]  # ID is now in 5th position
#                 self.cycle_task_status(task_id)

#     def cycle_task_status(self, task_id):
#         """Cycle through task statuses"""
#         if not self.task_manager:
#             return
            
#         task = self.task_manager.find_task(task_id)
#         if task:
#             status_cycle = ["Đang chờ", "Đang tiến hành", "Hoàn thành"]
#             current_index = status_cycle.index(task.status) if task.status in status_cycle else 0
#             new_status = status_cycle[(current_index + 1) % len(status_cycle)]
            
#             self.task_manager.update_task(task_id, status=new_status)
#             self.refresh_tree()

#     def change_task_status(self, new_status):
#         """Change status of selected task"""
#         item = self.tree.selection()
#         if not item:
#             messagebox.showinfo('Thông báo', 'Vui lòng chọn một công việc')
#             return
        
#         if not self.task_manager:
#             return
            
#         values = self.tree.item(item, 'values')
#         if len(values) >= 5:
#             task_id = values[4]
#             self.task_manager.update_task(task_id, status=new_status)
#             self.refresh_tree()

#     def add_task(self):
#         if not self.task_manager:
#             messagebox.showwarning("Lỗi", "Vui lòng đăng nhập trước")
#             return
            
#         dlg = TaskDialog(self, title='Thêm công việc')
#         if dlg.result:
#             self.task_manager.add_task(dlg.result)
#             self.refresh_tree()

#     def edit_task(self):
#         item = self.tree.selection()
#         if not item:
#             messagebox.showinfo('Chỉnh sửa', 'Vui lòng chọn một công việc để chỉnh sửa')
#             return
        
#         if not self.task_manager:
#             return
            
#         values = self.tree.item(item, 'values')
#         if len(values) >= 5:
#             task_id = values[4]
#             task = self.task_manager.find_task(task_id)
#             if task:
#                 dlg = TaskDialog(self, title='Chỉnh sửa công việc', task=task)
#                 if dlg.result:
#                     self.task_manager.update_task(task_id, 
#                                                 title=dlg.result.title,
#                                                 description=dlg.result.description,
#                                                 due=dlg.result.due,
#                                                 priority=dlg.result.priority)
#                     self.refresh_tree()

#     def delete_task(self):
#         item = self.tree.selection()
#         if not item:
#             messagebox.showinfo('Xóa', 'Vui lòng chọn một công việc để xóa')
#             return
        
#         if not messagebox.askyesno('Xác nhận', 'Xóa công việc đã chọn?'):
#             return
        
#         if not self.task_manager:
#             return
            
#         values = self.tree.item(item, 'values')
#         if len(values) >= 5:
#             task_id = values[4]
#             self.task_manager.delete_task(task_id)
#             self.refresh_tree()

#     def view_details(self):
#         item = self.tree.selection()
#         if not item:
#             return
        
#         if not self.task_manager:
#             return
            
#         values = self.tree.item(item, 'values')
#         if len(values) >= 5:
#             task_id = values[4]
#             task = self.task_manager.find_task(task_id)
#             if task:
#                 details = f"Chủ đề: {task.title}\n\nMô tả:\n{task.description}\n\nNgày thiết lập: {task.due}\nĐộ ưu tiên: {task.priority}\nTrạng thái: {task.status}"
#                 messagebox.showinfo('Chi tiết công việc', details)

#     def save_tasks(self):
#         """Save tasks to default location"""
#         if not self.task_manager:
#             messagebox.showwarning("Lỗi", "Vui lòng đăng nhập trước")
#             return
            
#         try:
#             self.task_manager.save_tasks()
#             messagebox.showinfo('Lưu', 'Đã lưu công việc thành công!')
#         except Exception as e:
#             messagebox.showerror('Lỗi', f'Không thể lưu công việc: {e}')

#     def save_as(self):
#         """Save tasks to user-specified location"""
#         if not self.task_manager:
#             messagebox.showwarning("Lỗi", "Vui lòng đăng nhập trước")
#             return
            
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".json",
#             filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
#             title="Lưu công việc thành..."
#         )
        
#         if file_path:
#             try:
#                 self.task_manager.save_tasks(file_path)
#                 messagebox.showinfo('Lưu', f'Đã lưu công việc thành công tại:\n{file_path}')
#             except Exception as e:
#                 messagebox.showerror('Lỗi', f'Không thể lưu công việc: {e}')

#     def export_json(self):
#         """Export tasks to JSON file"""
#         if not self.task_manager:
#             messagebox.showwarning("Lỗi", "Vui lòng đăng nhập trước")
#             return
            
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".json",
#             filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
#             title="Xuất công việc ra JSON"
#         )
        
#         if file_path:
#             try:
#                 self.task_manager.export_to_json(file_path)
#                 messagebox.showinfo('Xuất dữ liệu', f'Đã xuất công việc thành công tại:\n{file_path}')
#             except Exception as e:
#                 messagebox.showerror('Lỗi', f'Không thể xuất công việc: {e}')

#     def filter_tasks(self):
#         """Filter tasks based on current filter settings"""
#         if not self.task_manager:
#             return []
            
#         q = self.search_var.get().strip().lower()
#         status_filter = self.filter_var.get()
#         priority_filter = self.priority_filter_var.get()
        
#         result = []
#         for task in self.task_manager.tasks:
#             # Text search filter
#             if q:
#                 if q not in (task.title.lower() + ' ' + task.description.lower()):
#                     continue
            
#             # Status filter
#             if status_filter != 'Tất cả' and task.status != status_filter:
#                 continue
            
#             # Priority filter
#             if priority_filter != 'Tất cả' and str(task.priority) != priority_filter:
#                 continue
            
#             result.append(task)
        
#         return result

#     def sort_tasks(self, tasks):
#         """Sort tasks based on current sort setting"""
#         sort_key = self.sort_var.get()
        
#         if sort_key == 'Ngày thiết lập':
#             def sort_func(task):
#                 if not task.due:
#                     return datetime.max
#                 try:
#                     return datetime.strptime(task.due, DATE_FMT)
#                 except Exception:
#                     return datetime.max
#             tasks.sort(key=sort_func)
#         elif sort_key == 'Độ ưu tiên':
#             tasks.sort(key=lambda x: x.priority)
#         elif sort_key == 'Chủ đề':
#             tasks.sort(key=lambda x: x.title.lower())

#     def refresh_tree(self):
#         """Refresh the tree view with current tasks"""
#         if not self.task_manager:
#             return
            
#         # Clear existing items
#         for item in self.tree.get_children():
#             self.tree.delete(item)
        
#         # Get filtered and sorted tasks
#         filtered_tasks = self.filter_tasks()
#         self.sort_tasks(filtered_tasks)
        
#         # Configure tags for colors - only status column should have colors
#         for status, color in self.status_colors.items():
#             self.tree.tag_configure(status, foreground='black')  # Default black for all
        
#         # Insert tasks
#         for task in filtered_tasks:
#             values = (task.title, task.due, task.priority, task.status, task.id)
#             item_id = self.tree.insert('', 'end', values=values)
            
#             # Apply color only to status column
#             self.tree.set(item_id, 'status', task.status)
#             for col_id, col_name in enumerate(['title', 'due', 'priority', 'status'], 1):
#                 if col_name == 'status':
#                     # Create unique tag for each status
#                     tag_name = f"status_{task.status}"
#                     self.tree.tag_configure(tag_name, foreground=self.status_colors.get(task.status, 'black'))
#                     self.tree.item(item_id, tags=(tag_name,))
#                     break
        
#         # Update count
#         self.count_label.config(text=f"{len(filtered_tasks)} công việc")