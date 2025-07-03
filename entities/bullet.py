if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()
import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target, bullet_type=1):
        super().__init__()
        self.type = bullet_type
        self.image = pygame.Surface((20, 8))
        color_map = {
            1: (120,160,190),
            2: (255,220,80),
            3: (170,100,50),
            4: (50,50,50),
        }
        self.image.fill(color_map.get(self.type, (255, 255, 255)))
        self.rect = self.image.get_rect(center=pos)

        dx = target[0] - pos[0]
        dy = target[1] - pos[1]
        length = math.hypot(dx, dy) #弾速変更↓
        self.velocity = (dx / length * 15, dy / length * 15) if length != 0 else (10, 0)

        angle = -math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self,dt):
        self.rect.x += self.velocity[0]*dt/16.666
        self.rect.y += self.velocity[1]*dt/16.666
        if (self.rect.right < 0 or self.rect.left > 1200 or
            self.rect.bottom < 0 or self.rect.top > 700):
            self.kill()