# src/config.py
import os

# Thư mục gốc dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Đường dẫn file dữ liệu
DATA_DIR = os.path.join(BASE_DIR, "data")
TASKS_DIR = os.path.join(BASE_DIR, "data", "tasks")
USERS_FILE = os.path.join(DATA_DIR, "users.json")