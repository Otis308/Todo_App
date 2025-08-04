from managers.task_manager import TaskManager

# Khởi tạo TaskManager
manager = TaskManager()

# Thêm task
manager.add_task("Học Python")
manager.add_task("Làm bài tập")

# Tìm kiếm
results = manager.find_task_by_title("python")
print(results)

# Lọc task đã hoàn thành
done = manager.get_completed_tasks()
print(done)
