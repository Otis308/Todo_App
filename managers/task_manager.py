from models.task import task
from datetime import datetime
import sys 

class task_manager:
    def __init__(self):
        self.tasks = [] 
        self.id = 0
#1. func add_task
    def add_task(self): 
        self.id += 1
        new_task = task(
            id=self.id,
            title="",
            description="",
            created_at = datetime.now(),
            due_date="",
            status="",
            owner=""
        )
        new_task.input_info()
        self.tasks.append(new_task)
        print("✅Task added!")
#2. func delete_task
#3. func update_task
#4. func search_task
#5. func show_all_tasks
    def show_all_tasks(self):
        print("\n📝 TASK LIST:")
        for task in self.tasks:
            task.show_info()
#func menu_task
    def menu_task(self):
        while True: 
            print("\n===== TASK MENU =====")
            print("1. Add task")
            print("2. Delete task")
            print("3. Update task")
            print("4. Show all tasks")
            print("0. Exit")
            print("\n===== ********* =====")
            choice = input("👉 Choice a number: ")
            
            if choice == 0:
                sys.exit(0)
                break
            elif choice == '1': 
                self.add_task()
                break
            elif choice == '2': 
                break
            elif choice == '3': 
                break
            elif choice == '4': 
                self.show_all_tasks()
                break
            else:
                print("⚠️ Invalid choice! Try again.")
        return self.menu_task()
    



