
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json, uuid, os

DATA_FILE = "tasks.json"
DATE_FMT = "%d%m%Y"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print("Failed to load tasks:", e)
        return []


def save_tasks(tasks):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Failed to save tasks:", e)
