import pygame
import random
import math
from entities.effects import Explosion
from core.gamestate import GameState

class Boss(pygame.sprite.Sprite):
    def __init__(self,image_surface,spawn_func,bullet_group,all_sprites,gm=None):
        super().__init__()
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (100, 100))
        self.rect = self.image.get_rect(center=(1100, 350)) 
        self.state = "entering"
        self.wait_timer = 0
        self.current_action = None
        self.actions = [self.act1_radial, self.act2_summon, self.act3_chasers, self.act4_stream,]
        self.action_phase = 0
        self.action_timer = 0
        self.action_done = False
        self.radius = self.rect.width // 2
        self.gm = gm
        
        self.bullet_group = bullet_group
        self.all_sprites = all_sprites
        self.hp = 200
        self.spawn = spawn_func
        
        self.home_x,self.home_y = 900,350
        self.center_x,self.center_y = 600,350
        
        self.move_dir = 1
        
        
    def update(self, dt, player):
        if self.state == "entering":
            self.rect.x -= 4
            if self.rect.x <= self.home_x:
                self.rect.x = self.home_x
                self.state = "waiting"
                self.wait_timer = 0

        elif self.state == "waiting":
            self.wait_timer += dt
            if self.wait_timer >= 2000:
                self.current_action = random.choice(self.actions)
                self.action_phase = 0
                self.action_timer = 0
                self.action_done = False
                
                if self.current_action == self.act1_radial:
                    self.state = "move_to_center"
                else:
                    self.state = "acting"
                if self.current_action == self.act3_chasers:
                    self.move_dir = 1
                    
        elif self.state == "move_to_center":
            if abs(self.rect.x - self.center_x) > 4:
                step = 4 if self.rect.x > self.center_x else -4
                self.rect.x -= step
            else:
                self.rect.x = self.center_x
                self.rect.y = self.center_y
                self.state="acting"
                
        elif self.state == "acting":
            if self.current_action == self.act3_chasers:
                self.rect.y += 4 * self.move_dir
                if self.rect.y <= self.center_y - 150 or self.rect.y >= self.center_y + 150:
                    self.move_dir = -self.move_dir
                
            self.current_action(dt, player)
            if self.action_done:
                self.state = "returning"

        elif self.state == "returning":
            done_x = False
            done_y = False
            
            if abs(self.rect.x - self.home_x) > 4:
                self.rect.x += 4 if self.rect.x < self.home_x else -4
            else:
                self.rect.x = self.home_x
                done_x = True
            if abs(self.rect.y - self.home_y) > 2:
                self.rect.y += 2 if self.rect.y < self.home_y else -2
            else:
                self.rect.y = self.home_y
                done_y = True
            if done_x and done_y:
                self.state = "waiting"
                self.wait_timer = 0

    def act1_radial(self, dt, player):
        self.action_timer += dt
        if self.action_phase == 0 and self.action_timer >= 300:
            for i in range(18):
                angle = math.radians(i * 20)
                vx = math.cos(angle) * 5
                vy = math.sin(angle) * 5
                spawn_bullet(self.rect.center, vx, vy,self.bullet_group,self.all_sprites)
            self.action_phase = 1
            self.action_timer = 0
        elif self.action_phase == 1 and self.action_timer >= 300:
            for i in range(18):
                angle = math.radians(i * 20 + 10)
                vx = math.cos(angle) * 5
                vy = math.sin(angle) * 5
                spawn_bullet(self.rect.center, vx, vy,self.bullet_group,self.all_sprites)
            self.action_phase = 2
            self.action_timer = 0
        elif self.action_phase == 2 and self.action_timer >=300:
            for i in range(18):
                angle = math.radians(i * 20 + 20)
                vx = math.cos(angle) * 5
                vy = math.sin(angle) * 5
                spawn_bullet(self.rect.center, vx, vy,self.bullet_group,self.all_sprites)
            self.action_done = True

    def act2_summon(self, dt, player):
        self.spawn("AburaCurveCharger", 1100, 200)
        self.spawn("AburaCurveCharger", 1100, 400)
        self.spawn("AburaCurveCharger", 1100, 600)
        self.spawn("SabiCharger", 1150, 100)
        self.spawn("SabiCharger", 1150, 300)
        self.spawn("SabiCharger", 1150, 500)
        self.action_done = True

    def act3_chasers(self, dt, player):
        self.action_timer += dt
        if self.action_phase < 4 and self.action_timer >= 500:
            px, py = player.rect.center
            bx, by = self.rect.center
            angle = math.atan2(py - by, px - bx)
            for offset in [-0.3, 0, 0.3]:
                a = angle + offset
                vx = math.cos(a) * 8
                vy = math.sin(a) * 8
                spawn_tracking_bullet((bx, by), vx, vy,self.bullet_group, self.all_sprites)
            self.action_phase += 1
            self.action_timer = 0
            
        elif self.action_phase >= 4:
            self.action_done = True
            self.move_dir = 0

    def act4_stream(self, dt, player):
        self.action_timer += dt
        if self.action_timer >= 70:
            self.action_timer = 0
            self.action_phase += 1
            if self.action_phase <= 30:
                px, py = player.rect.center
                bx, by = self.rect.center
                angle = math.atan2(py - by, px - bx)
                vx = math.cos(angle) * 7
                vy = math.sin(angle) * 7
                spawn_bullet((bx, by), vx, vy,self.bullet_group, self.all_sprites)
            else:
                self.action_done = True
        
    def take_damage(self, damage,all_sprites, enemies_group, explosions_group, gm):
        self.hp -= damage
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            self.gm.score += 1
            self.gm.add_laser_score(1)
            self.kill()
            self.gm.state = GameState.CLEAR

class BossBullet(pygame.sprite.Sprite):
    def __init__(self,pos,vx,vy):
        super().__init__()
        self.image = pygame.Surface((8,8))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect(center=pos)
        self.vx = vx
        self.vy = vy
        
    def update(self,dt):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if not (0 <= self.rect.x <= 1300 and 0 <= self.rect.y <= 800):
            self.kill()

class TrackingBullet(pygame.sprite.Sprite):
    def __init__(self, pos, vx, vy):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.vx = vx
        self.vy = vy

    def update(self,dt):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if not (0 <= self.rect.x <= 1300 and 0 <= self.rect.y <= 800):
            self.kill()
          
def spawn_bullet(pos,vx,vy,bullet_group, all_sprites):
    bullet = BossBullet(pos,vx,vy)
    all_sprites.add(bullet)
    bullet_group.add(bullet)

def spawn_tracking_bullet(pos,vx,vy,bullet_group, all_sprites):
    bullet = TrackingBullet(pos,vx,vy)
    all_sprites.add(bullet)
    bullet_group.add(bullet)