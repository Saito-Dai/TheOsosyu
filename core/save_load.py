
import json
import os
from config import path

SAVE_PATH = path("save","save.json")

def save_game(data: dict):
    save_dir = os.path.dirname(SAVE_PATH)
    os.makedirs(save_dir,exist_ok=True)
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("[保存] セーブデータを書き込みました。")
    except Exception as e:
        print(f"[エラー] セーブに失敗しました: {e}")

def load_game() -> dict | None:
    if not os.path.exists(SAVE_PATH):
        return None
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("[読込] セーブデータを読み込みました。")
        return data
    except Exception as e:
        print(f"[エラー] セーブデータ読み込み失敗: {e}")
        return None

def delete_save():
    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)
        print("[削除] セーブデータを削除しました。")
