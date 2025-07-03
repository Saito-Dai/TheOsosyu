if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()
import pygame
from config import path

def safe_load_image(path_str, fallback_size=(100, 100)):
    try:
        image = pygame.image.load(path_str).convert_alpha()
        return image
    except Exception as e:
        print(f"[エラー]画像読み込み失敗: {path_str} - {e}")
        return pygame.Surface(fallback_size)

def safe_load_sound(path_str):
    try:
        return pygame.mixer.Sound(path_str)
    except Exception as e:
        print(f"[エラー]音声読み込み失敗: {path_str} - {e}")
        return None

def load_images():
    return {
        "player": safe_load_image(path("assets", "image", "runba_jiki.png")),
        "mizuaka": safe_load_image(path("assets", "image", "Enemy1-mizuaka.png")),
        "abura": safe_load_image(path("assets", "image", "Enemy2-abura.png")),
        "sabi": safe_load_image(path("assets", "image", "Enemy3-sabi.png")),
        "kabi": safe_load_image(path("assets", "image", "Enemy4-kabi.png")),
        "bg_top": safe_load_image(path("assets", "image", "kabe_r.png")),
        "bg_bot": safe_load_image(path("assets", "image", "yuka_t.png")),
        "Shield": safe_load_image(path("assets", "image", "shield.png")),
        "kabismoke": safe_load_image(path("assets", "image", "kabismoke.png")),
        "boss":safe_load_image(path("assets","image","Boss.png")),
        "fragment":safe_load_image(path("assets","image","fragment.png"))
    }

def load_sounds():
    return {
        "hit": safe_load_sound(path("assets", "sound", "SE", "Hit.wav")),
        "clear": safe_load_sound(path("assets", "sound", "SE", "clear.wav"))
    }

def load_bgm():
    return {
        "start": path("assets", "sound", "BGM", "start_edm.wav"),
        "play": path("assets", "sound", "BGM", "game_pop.wav"),
    }

def load_font(font_size=48):
    font_path = path("assets", "font", "なぎの", "nagino.ttf")
    if not pygame.freetype.get_init():
        pygame.freetype.init()
    try:
        return pygame.freetype.Font(font_path, font_size)
    except:
        return pygame.freetype.SysFont(None, font_size)
