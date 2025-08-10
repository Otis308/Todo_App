
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json, uuid, os
from tkcalendar import DateEntry
from managers.task_manager import load_tasks, save_tasks

DATA_FILE = "tasks.json"
DATE_FMT = "%d%m%Y"

class TaskDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, task=None):
        self.task = task
        super().__init__(parent, title=title)

    def body(self, master):
        self.geometry("1000x780+270+20")
        ttk.Label(master, text="Title:").grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar(value=(self.task.get('title') if self.task else ""))
        self.title_entry = ttk.Entry(master, textvariable=self.title_var)
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=6, pady=4)

        ttk.Label(master, text="Description:").grid(row=1, column=0, sticky="nw")
        self.desc_text = tk.Text(master, height=6, width=40)
        if self.task:
            self.desc_text.insert("1.0", self.task.get("description", ""))
        self.desc_text.grid(row=1, column=1, sticky="ew", padx=6, pady=4)

        ttk.Label(master, text="Due date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        self.due_var = tk.StringVar(value=(self.task.get('due') if self.task else ""))
        cal = DateEntry(master, textvariable=self.due_var, date_pattern="yyyy-mm-dd",
                        background='darkblue', foreground='white', borderwidth=2)
        cal.grid(row=2, column=1)

        ttk.Label(master, text="Priority (1=High, 3=Low):").grid(row=3, column=0, sticky="w")
        self.prio_var = tk.IntVar(value=(self.task.get('priority') if self.task else 2))
        prio_spin = ttk.Spinbox(master, from_=1, to=3, textvariable=self.prio_var, width=5)
        prio_spin.grid(row=3, column=1, sticky="w", padx=6, pady=4)

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
                messagebox.showwarning("Validation", "Due date must be in YYYY-MM-DD format")
                return False
        return True

    def apply(self):
        self.result = {
            "title": self.title_var.get().strip(),
            "description": self.desc_text.get("1.0", "end").strip(),
            "due": self.due_var.get().strip(),
            "priority": int(self.prio_var.get()),
            "completed": bool(self.task.get("completed") if self.task else False),
            "id": (self.task.get("id") if self.task else str(uuid.uuid4()))
        }

class TaskManagerApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  
        self.controller = controller
        self.tasks = load_tasks()
        self.create_widgets()
        self.refresh_tree()

    def create_widgets(self):
        # Top controls
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=8, pady=6)

        add_btn = ttk.Button(top_frame, text="Add Task", command=self.add_task)
        add_btn.pack(side="left")

        edit_btn = ttk.Button(top_frame, text="Edit Task", command=self.edit_task)
        edit_btn.pack(side="left", padx=6)

        del_btn = ttk.Button(top_frame, text="Delete Task", command=self.delete_task)
        del_btn.pack(side="left")

        complete_btn = ttk.Button(top_frame, text="Toggle Complete", command=self.toggle_complete)
        complete_btn.pack(side="left", padx=6)

        ttk.Label(top_frame, text="Search:").pack(side="left", padx=(12, 4))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var)
        search_entry.pack(side="left")
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_tree())

        ttk.Label(top_frame, text="Filter:").pack(side="left", padx=(12, 4))
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(top_frame, values=["All", "Active", "Completed"], width=10, state="readonly", textvariable=self.filter_var)
        filter_combo.pack(side="left")
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_tree())

        ttk.Label(top_frame, text="Sort by:").pack(side="left", padx=(12,4))
        self.sort_var = tk.StringVar(value="due")
        sort_combo = ttk.Combobox(top_frame, values=["due", "priority", "title"], width=10, state="readonly", textvariable=self.sort_var)
        sort_combo.pack(side="left")
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_tree())

        # Tree / List
        cols = ("title", "due", "priority", "status")
        self.tree = ttk.Treeview(self, columns=cols, show='headings', selectmode='browse')
        self.tree.heading('title', text='Title')
        self.tree.heading('due', text='Due')
        self.tree.heading('priority', text='Priority')
        self.tree.heading('status', text='Status')

        self.tree.column('title', width=380)
        self.tree.column('due', width=100, anchor='center')
        self.tree.column('priority', width=70, anchor='center')
        self.tree.column('status', width=90, anchor='center')

        self.tree.pack(fill='both', expand=True, padx=8, pady=6)
        self.tree.bind('<Double-1>', lambda e: self.view_details())

        # Bottom status
        bottom = ttk.Frame(self)
        bottom.pack(fill='x', padx=8, pady=6)
        save_btn = ttk.Button(bottom, text='Save', command=lambda: save_tasks(self.tasks))
        save_btn.pack(side='left')
        export_btn = ttk.Button(bottom, text='Export as JSON', command=self.export_json)
        export_btn.pack(side='left', padx=6)
        self.count_label = ttk.Label(bottom, text='0 tasks')
        self.count_label.pack(side='right')

    def add_task(self):
        dlg = TaskDialog(self, title='Add Task')
        if dlg.result:
            task = dlg.result
            self.tasks.append(task)
            self.refresh_tree()

    def edit_task(self):
        item = self.tree.selection()
        if not item:
            messagebox.showinfo('Edit', 'Please select a task to edit')
            return
        task_id = self.tree.item(item, 'values')[3]  # hidden id stored in values 4th
        task = self.find_task(task_id)
        if not task:
            messagebox.showerror('Error', 'Task not found')
            return
        dlg = TaskDialog(self, title='Edit Task', task=task)
        if dlg.result:
            # preserve completed and id but update other fields
            task.update(dlg.result)
            task['completed'] = dlg.result.get('completed', task.get('completed', False))
            self.refresh_tree()

    def delete_task(self):
        item = self.tree.selection()
        if not item:
            messagebox.showinfo('Delete', 'Please select a task to delete')
            return
        if not messagebox.askyesno('Confirm', 'Delete selected task?'):
            return
        task_id = self.tree.item(item, 'values')[3]
        self.tasks = [t for t in self.tasks if t.get('id') != task_id]
        self.refresh_tree()

    def toggle_complete(self):
        item = self.tree.selection()
        if not item:
            messagebox.showinfo('Toggle', 'Please select a task')
            return
        task_id = self.tree.item(item, 'values')[3]
        task = self.find_task(task_id)
        if task:
            task['completed'] = not task.get('completed', False)
            self.refresh_tree()

    def view_details(self):
        item = self.tree.selection()
        if not item:
            return
        task_id = self.tree.item(item, 'values')[3]
        task = self.find_task(task_id)
        if not task:
            return
        details = f"Title: {task.get('title')}\n\nDescription:\n{task.get('description')}\n\nDue: {task.get('due')}\nPriority: {task.get('priority')}\nCompleted: {task.get('completed')}"
        messagebox.showinfo('Task details', details)

    def export_json(self):
        save_tasks(self.tasks)
        messagebox.showinfo('Export', f'Saved to {DATA_FILE}')

    def find_task(self, tid):
        for t in self.tasks:
            if t.get('id') == tid:
                return t
        return None

    def filter_tasks(self):
        q = self.search_var.get().strip().lower()
        f = self.filter_var.get()
        result = []
        for t in self.tasks:
            if q:
                if q not in (t.get('title','').lower() + ' ' + t.get('description','').lower()):
                    continue
            if f == 'Active' and t.get('completed'):
                continue
            if f == 'Completed' and not t.get('completed'):
                continue
            result.append(t)
        return result

    def sort_tasks(self, tasks):
        key = self.sort_var.get()
        if key == 'due':
            def _k(t):
                d = t.get('due')
                if not d:
                    return datetime.max
                try:
                    return datetime.strptime(d, DATE_FMT)
                except Exception:
                    return datetime.max
            tasks.sort(key=_k)
        elif key == 'priority':
            tasks.sort(key=lambda x: x.get('priority', 2))
        else:
            tasks.sort(key=lambda x: x.get('title','').lower())

    def refresh_tree(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        filtered = self.filter_tasks()
        self.sort_tasks(filtered)
        for t in filtered:
            status = 'Completed' if t.get('completed') else 'Active'
            due = t.get('due') or ''
            prio = t.get('priority', 2)
            # store id as hidden 4th column value
            self.tree.insert('', 'end', values=(t.get('title',''), due, prio, t.get('id'), status))
        # update count
        self.count_label.config(text=f"{len(filtered)} tasks (showing)")


if __name__ == '__main__':
    app = TaskManagerApp()
    app.mainloop()
