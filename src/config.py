# src/config.py
import os

# Thư mục gốc dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Đường dẫn file dữ liệu
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")

# Cấu hình giao diện
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 780
WINDOW_POSITION = "+270+20"

# Bảo mật
PASSWORD_HASH_ALGORITHM = "sha256"
