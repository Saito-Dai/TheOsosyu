if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()  
import pygame
from config import SCREEN_WIDTH,SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, image_surface):
        super().__init__()
        self.image = pygame.transform.scale(image_surface,(70,70))
        self.rect = self.image.get_rect(center=(100,SCREEN_HEIGHT // 2))
        self.hitbox = self.rect.inflate(-40,-40)
        # 移動に関する属性
        self.speed = 8
        self.slow_timer = 0
        self.vx = 0
        self.vy = 0

    def update(self, gm):
        speed = self.speed
        if self.slow_timer > 0:
            self.slow_timer -= 1
            speed = self.speed // 2
        else:
            speed = self.speed

        if gm.player_bound:
            self.vx = 0
            self.vy = 0
        else:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] and self.rect.top > 0:
                self.vy = -speed
            elif keys[pygame.K_s] and self.rect.bottom < 700:
                self.vy = speed
            else:
                self.vy = 0

            if keys[pygame.K_a] and self.rect.left > 0:
                self.vx = -speed
            elif keys[pygame.K_d] and self.rect.right < 1200:
                self.vx = speed
            else:
                self.vx = 0

        self.rect.x += self.vx
        self.rect.y += self.vy

        self.hitbox.center = self.rect.center

        
        