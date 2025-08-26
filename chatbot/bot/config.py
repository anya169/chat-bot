TOKEN='7741930969:AAFFBhqYEqetYvSKCHtKSQ5yhP1mUNNHwo8'
ADMINS={1027655992}
# bot/config.py
import json
from pathlib import Path

BLOCKED_FILE = Path(__file__).parent.parent / 'blocked_users.json'

def load_blocked():
   if BLOCKED_FILE.exists():
      with open(BLOCKED_FILE, 'r', encoding='utf-8') as f:
         data = json.load(f)
         return data
   else:
      # Создаем пустой файл если не существует
      with open(BLOCKED_FILE, 'w', encoding='utf-8') as f:
         json.dump([], f)
      return []
  
def save_blocked(blocked_list):
   with open(BLOCKED_FILE, 'w', encoding='utf-8') as f:
      json.dump(blocked_list, f, ensure_ascii=False)


def add_to_blocked(user_id):
   blocked = load_blocked()
   if user_id not in blocked:
      blocked.append(user_id)
      save_blocked(blocked)
     


def get_blocked_users():
   return load_blocked()

