import json
import os

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(CURRENT_DIR, "data", "scores.json")

def load_data():
    try:
        with open(FILE, "r", encoding="utf8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(FILE, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)

def add_score(user_id, amount):
    data = load_data()

    if str(user_id) not in data:
        data[str(user_id)] = 0

    data[str(user_id)] += amount

    save_data(data)

def get_top():
    data = load_data()
    return sorted(data.items(), key=lambda x: x[1], reverse=True)