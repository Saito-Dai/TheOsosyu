if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()

import pygame
import math

class Laser(pygame.sprite.Sprite):
    def __init__(self, player, target_pos):
        super().__init__()
        self.player = player
        self.target_pos = target_pos
        self.start_pos = self.player.rect.center

        self.color = (0, 255, 255)
        self.width = 6

        self.start_time = pygame.time.get_ticks()
        self.lifetime = 2000  # 2秒
        self.hit_interval = 50
        self.last_hit_time = 0
        self.hit_enemies = set()

    def update(self, dt):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        
        self.start_pos = self.player.rect.center
        self.target_pos = pygame.mouse.get_pos()

        # --- カーソル位置をリアルタイム追従 ---
        self.start_pos = self.player.rect.center
        self.target_pos = pygame.mouse.get_pos()

    def draw(self, screen):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        fade_ratio = max(0, 1 - elapsed / self.lifetime)
        alpha = int(fade_ratio * 255)

        color_with_alpha = (*self.color, alpha)
        temp_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.line(temp_surface, color_with_alpha, self.start_pos, self.target_pos, self.width)
        screen.blit(temp_surface, (0, 0))

    def can_hit(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit_time >= self.hit_interval:
            self.last_hit_time = now
            return True
        return False
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time >= self.lifetime
    
def point_to_line_distance(p, a, b):
        px, py = p
        ax, ay = a
        bx, by = b
        apx, apy = px - ax, py - ay
        abx, aby = bx - ax, by - ay
        ab_len_sq = abx**2 + aby**2
        if ab_len_sq == 0:
            return math.hypot(px - ax, py - ay)
        dot = apx * abx + apy * aby
        t = max(0, min(1, dot / ab_len_sq))
        closest_x = ax + t * abx
        closest_y = ay + t * aby
        return math.hypot(px - closest_x, py - closest_y)
