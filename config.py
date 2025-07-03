if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FPS = 60
WHITE, BLACK, RED, GREEN = (255,255,255), (0,0,0), (255,0,0), (0,255,0)

BASE_DIR =os.path.dirname(__file__)
SAVE_PATH = os.path.join(BASE_DIR,"save","save.json")

def path(*p):
    return os.path.join(BASE_DIR,*p)