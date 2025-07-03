if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()
import pygame
import random
import math
from config import SCREEN_HEIGHT
class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.radius = 1
        self.max_radius = 30
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

    def update(self,dt):
        self.radius += 6
        if self.radius >= self.max_radius:
            self.kill()
            return
        self.image.fill((0, 0, 0, 0))
        alpha = int(255 * (1 - self.radius / self.max_radius))
        pygame.draw.circle(self.image, (255, 200, 0, alpha), (30, 30), self.radius)
        self.rect = self.image.get_rect(center=self.pos)

class Fragment(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed, scale=0.10):
        super().__init__()
        w, h = image.get_size()
        # ①生成位置は敵の中心のみ
        self.image = pygame.transform.scale(
            image, (int(w*scale), int(h*scale))
        )
        self.rect = self.image.get_rect(center=pos)
        
        # ②角度を全周からランダムに
        angle = random.uniform(0, 2 * math.pi)
        magnitude = speed * random.uniform(3.0,6.0)
        
        # ③速度の振れ幅を均等に
        self.vx = magnitude * math.cos(angle)*3.0
        self.vy = magnitude * math.sin(angle)*3.0
        
        # （オプション）上方向に強めたい場合
        if self.vy < 0:
            self.vy *= 1.2
        
        self.gravity = 500

    def update(self, dt_ms):
        dt = dt_ms / 1000.0
        self.vy += self.gravity * dt
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)
        
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()