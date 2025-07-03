if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()
import pygame
import pygame
import random
import math
from entities.effects import Explosion,Fragment
from config import SCREEN_WIDTH,SCREEN_HEIGHT

class Mizuaka(pygame.sprite.Sprite):
    def __init__(self, image_surface):
        super().__init__()
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (80, 80))
        self.rect = self.image.get_rect(
            x=SCREEN_WIDTH + random.randint(0, 100),
            y=random.randint(50, SCREEN_HEIGHT - 50)
        )
        self.speed = 4
        self.hp = 4
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.rect.x -= self.speed*dt /16.666
        if self.rect.right < 0:
            self.kill()
    
    def take_damage(self, damage,all_sprites, enemies_group, explosions_group, fragment_group,):
        self.hp -= damage
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            for _ in range(4):  
                speed =  10
                frag = Fragment(self.fragment_image, self.rect.center, speed)
                all_sprites.add(frag)
                fragment_group.add(frag)    
            self.gm.score += 1
            self.gm.add_laser_score(1)
        self.kill()
            
class MizuakaShooter(pygame.sprite.Sprite):
    def __init__(self, image_surface, target_player, bullet_group, all_sprites):
        super().__init__()
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (80, 80))
        self.rect = self.image.get_rect(
            x=SCREEN_WIDTH + random.randint(0, 100),
            y=random.randint(50, SCREEN_HEIGHT - 50)
        )
        self.speed = random.randint(4, 7)
        self.hp = 4
        self.is_stopped = False
        self.wait_timer = 0  
        self.shoot_timer = 0  
        self.target_player = target_player  
        self.bullet_group = bullet_group
        self.all_sprites = all_sprites
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        current_time = pygame.time.get_ticks()

        if not self.is_stopped:
            self.rect.x -= self.speed*dt/16.666
            if self.rect.left <= 0:
                self.rect.left = 0
                self.is_stopped = True
                self.wait_timer = current_time  
        else:
            if current_time - self.wait_timer >= 1000:
                if current_time - self.shoot_timer >= 1000:
                    self.shoot_bullet()
                    self.shoot_timer = current_time

    def shoot_bullet(self):
        bullet = MizuakaBullet(self.rect.centerx, self.rect.centery, self.target_player.rect.center)
        self.all_sprites.add(bullet)
        self.bullet_group.add(bullet)

    def take_damage(self, damage,all_sprites, enemies_group, explosions_group, fragment_group,):
        self.hp -= damage
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            for _ in range(4):  
                speed =  10
                frag = Fragment(self.fragment_image, self.rect.center, speed)
                all_sprites.add(frag)
                fragment_group.add(frag)    
            self.gm.score += 1
            self.gm.add_laser_score(1)
        self.kill()
        
class MizuakaBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 150, 255))  
        self.rect = self.image.get_rect(center=(x, y))

        dx = target_pos[0] - x
        dy = target_pos[1] - y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance == 0:
            distance = 1 

        speed = 6
        self.velocity_x = speed * dx / distance
        self.velocity_y = speed * dy / distance
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.rect.x += self.velocity_x*dt/16.666
        self.rect.y += self.velocity_y*dt/16.666

        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

class MizuakaZigZag(pygame.sprite.Sprite):
    def __init__(self, image_surface,all_sprites,enemies,speed):
        super().__init__()
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (80, 80))
        self.rect = self.image.get_rect(
            x=SCREEN_WIDTH + 50,  
            y=random.randint(100, SCREEN_HEIGHT - 100)
        )
        
        self.hp = 4
        self.speed = 5
        self.phase2_speed = 8
        
        self.phase = 0  # 0: 左へ → 1: 右上へ → 2: 左へ → 3: 終了
        self.phase_timer = 0  # phase 用のタイマー（必要なら使う）
        
        # 移動量管理
        self.move_counter = 0  # phase内でどのくらい移動したか記録
        
        # 移動設定（どのくらい動いたら次phaseへ行くか）
        self.left_move_distance1 = 500 # 最初の左移動距離
        self.diagonal_move_distance = 200  # 右上への移動距離（X成分で測る）
        self.left_move_distance2 = SCREEN_WIDTH  # 画面左へ出るまで
        self.alive_flag = True
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        if not self.alive_flag:
            return
        
        if self.phase == 0:
            # phase0
            self.rect.x -= self.speed*dt/16.666
            self.move_counter += self.speed
            if self.move_counter >= self.left_move_distance1:
                self.phase = 1
                self.move_counter = 0
                
        elif self.phase == 1:
            # phase1
            diag_speed = self.speed*dt/16.666
            self.rect.x += diag_speed
            self.rect.y -= diag_speed
            self.move_counter += diag_speed
            if self.move_counter >= self.diagonal_move_distance:
                self.phase = 2
                self.move_counter = 0
                
        elif self.phase == 2:
            # phase2
            self.rect.x -= self.phase2_speed*dt/16.666
            if self.rect.right < 0:
                self.phase = 3
                
        elif self.phase == 3:
            self.alive_flag = False
            self.kill()
                
    def take_damage(self, damage, all_sprites, enemies_group, explosions_group, fragment_group):
        frag_img = self.fragment_image
        gm = self.gm
        if not self.alive_flag:
            return
        self.hp -= damage
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            for _ in range(4):  
                speed =  10
                frag = Fragment(self.fragment_image, self.rect.center, speed)
                all_sprites.add(frag)
                fragment_group.add(frag)    
            self.gm.score += 1
            self.gm.add_laser_score(1)
        self.kill()
            
class MizuakaZigZagInversed(pygame.sprite.Sprite):
    def __init__(self, image_surface,all_sprites,enemies,speed):
        super().__init__()
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (80, 80))
        self.rect = self.image.get_rect(
            x=SCREEN_WIDTH + 50,
            y=random.randint(100, SCREEN_HEIGHT - 100)
        )
        
        self.hp = 4
        self.speed = 5
        self.phase2_speed = 8
        
        self.phase = 0
        self.phase_timer = 0
        self.move_counter = 0
        
        self.left_move_distance1 = 500
        self.diagonal_move_distance = 200
        self.left_move_distance2 = SCREEN_WIDTH
        self.alive_flag = True
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        if not self.alive_flag:
            return
        if self.phase == 0:
            # phase0: 左へ移動
            self.rect.x -= self.speed*dt/16.666
            self.move_counter += self.speed*dt/16.666
            if self.move_counter >= self.left_move_distance1:
                self.phase = 1
                self.move_counter = 0
                
        elif self.phase == 1:
            # phase1: 右下へ斜め移動
            diag_speed = self.speed*dt/16.666
            self.rect.x += diag_speed
            self.rect.y += diag_speed  # ← ここが「下向き」に変わるポイント
            self.move_counter += diag_speed
            if self.move_counter >= self.diagonal_move_distance:
                self.phase = 2
                self.move_counter = 0
                
        elif self.phase == 2:
            # phase2: 左へ移動（画面外へ向かう）
            self.rect.x -= self.phase2_speed
            if self.rect.right < 0:
                self.phase = 3
                
        elif self.phase == 3:
            self.alive_flag = False
            self.kill()
                
    def take_damage(self, damage,all_sprites, enemies_group, explosions_group, fragment_group):
        self.hp -= damage
        gm = self.gm
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            for _ in range(4):  
                speed =  10
                frag = Fragment(self.fragment_image, self.rect.center, speed)
                all_sprites.add(frag)
                fragment_group.add(frag)    
            self.gm.score += 1
            self.gm.add_laser_score(1)
        self.kill()
            
class MizuakaRightMover(pygame.sprite.Sprite):
    def __init__(self, image_surface,all_sprites,enemies,speed):
        super().__init__()
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (80, 80))
        self.rect = self.image.get_rect(
            x=-80,  
            y=random.randint(50, SCREEN_HEIGHT - 50)
        )
        
        self.hp = 4
        self.speed = 0.5
        self.accelation = 0.05
        self.max_speed = 100.0
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.speed += self.accelation*dt/16.666
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        self.rect.x += self.speed
        
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
            
    def take_damage(self, damage,all_sprites, enemies_group, explosions_group, fragment_group):
        self.hp -= damage
        gm = self.gm
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            for _ in range(4):  
                speed =  10
                frag = Fragment(self.fragment_image, self.rect.center, speed)
                all_sprites.add(frag)
                fragment_group.add(frag)    
            self.gm.score += 1
            self.gm.add_laser_score(1)
        self.kill()        
    
            
class MizuakaFormation(pygame.sprite.Sprite):
    def __init__(self, image_surface, all_sprites, enemies_group):
        super().__init__()
        self.members = []
        
        self.image = pygame.Surface((1,1))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(x=0,y=0)
        start_x = SCREEN_WIDTH + 50
        start_y = 100 

        spacing_x = 100  # 横方向の間隔
        spacing_y = 100  # 縦方向の間隔
        
        formation_pattern = [
            (0, 2),
            (1, 1),  # 出っ張り部分 
            (2, 0),  # 頂点
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
            (2, 7),  
            (2, 8),
        ]

        for pos in formation_pattern:
            mizu = MizuakaFormationMember(
                image_surface,
                start_x + pos[0] * spacing_x,
                start_y + pos[1] * spacing_y
            )
            self.members.append(mizu)
            all_sprites.add(mizu)
            enemies_group.add(mizu)

        self.state = "entering"  # "entering" → "waiting" → "leaving"
        self.timer = 0
        self.enter_speed = 8
        self.leave_speed = 2
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        current_time = pygame.time.get_ticks()

        if self.state == "entering":
            # 右→左に移動
            all_inside = True
            for member in self.members:
                member.rect.x -= self.enter_speed*dt/16.666
                if member.rect.right > SCREEN_WIDTH - 50:
                    all_inside = False
            if all_inside:
                self.state = "waiting"
                self.timer = current_time

        elif self.state == "waiting":
            # 停止
            if current_time - self.timer >= 3000:
                self.state = "leaving"

        elif self.state == "leaving":
        # 退場フェーズ開始時、メンバーに is_leaving をセット
            for member in self.members:
                if not member.is_leaving:
                    member.is_leaving = True
    # 生存メンバー更新
            self.members = [m for m in self.members if m.alive_flag]
            if not self.members:
                self.kill()
                
class MizuakaFormationMember(pygame.sprite.Sprite):
    def __init__(self, image_surface, x, y):
        super().__init__()
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (50, 50))
        self.rect = self.image.get_rect(x=x, y=y)
        self.hp = 4
        self.alive_flag = True
        self.is_leaving = False   #退場フェーズフラグ
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        if self.is_leaving and self.alive_flag:
            self.rect.x -= 2*dt/16.666  # Formation の leave_speed
            if self.rect.right < 0:
                self.alive_flag = False
                self.kill()
    
    def take_damage(self, damage, all_sprites, enemies_group, explosions_group, fragment_group):
        if not self.alive_flag:
            return
        self.hp -= damage
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            for _ in range(4):  
                speed =  10
                frag = Fragment(self.fragment_image, self.rect.center, speed)
                all_sprites.add(frag)
                fragment_group.add(frag) 
            self.gm.score += 1
            self.gm.add_laser_score(1)
            self.alive_flag = False
            self.kill()
     
class MizuakaUpLeftMover(pygame.sprite.Sprite):
    def __init__(self, image_surface, x, y, speed, x_speed_factor):
        super().__init__()
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (80, 80))
        self.rect = self.image.get_rect(x=x, y=y)

        self.hp = 4
        self.speed = speed  
        self.x_speed_factor = x_speed_factor  

        self.velocity_x = -self.speed * self.x_speed_factor
        self.velocity_y = -self.speed * (1 - self.x_speed_factor)
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.rect.x += self.velocity_x*dt/16.666
        self.rect.y += self.velocity_y*dt/16.666

        if (self.rect.right < 0 or self.rect.bottom < 0):
            self.kill()

    def take_damage(self, damage,all_sprites, enemies_group, explosions_group, fragment_group,):
        self.hp -= damage
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            for _ in range(4):  
                speed =  10
                frag = Fragment(self.fragment_image, self.rect.center, speed)
                all_sprites.add(frag)
                fragment_group.add(frag)    
            self.gm.score += 1
            self.gm.add_laser_score(1)
        self.kill()
            
class MizuakaDownLeftMover(pygame.sprite.Sprite):
    def __init__(self, image_surface, x, y, speed, x_speed_factor):
        super().__init__()
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (80, 80))
        self.rect = self.image.get_rect(x=x, y=y)

        self.hp = 4
        self.speed = speed
        self.x_speed_factor = x_speed_factor

        self.velocity_x = -self.speed * self.x_speed_factor
        self.velocity_y = self.speed * (1 - self.x_speed_factor)
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.rect.x += self.velocity_x*dt/16.666
        self.rect.y += self.velocity_y*dt/16.666

        if (self.rect.right < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

    def take_damage(self, damage,all_sprites, enemies_group, explosions_group, fragment_group):
        self.hp -= damage
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            for _ in range(4):  
                speed =  10
                frag = Fragment(self.fragment_image, self.rect.center, speed)
                all_sprites.add(frag)
                fragment_group.add(frag)    
            self.gm.score += 1
            self.gm.add_laser_score(1)
        self.kill()

class MizuakaDirectedMover(pygame.sprite.Sprite):
    def __init__(self, image_surface, x, y, speed, target_pos, start_immediately=True,gm=None,fragment_image=None,fragment_group=None):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(), (80, 80))
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 4

        self.pos = pygame.Vector2(x, y)
        self.target_pos = pygame.Vector2(target_pos)
        self.velocity = (self.target_pos - self.pos).normalize() * speed

        self.speed = speed
        self.started = start_immediately
        self.entered_screen = False
        self.radius = self.rect.width // 2
        self.fragment_image=fragment_image
        self.fragment_group = fragment_group
        self.gm = gm
        
    def update(self,dt):
        if self.started:
            self.pos += self.velocity*dt/16.666
            self.rect.center = (int(self.pos.x), int(self.pos.y))

            to_target = self.target_pos - self.pos
            if self.velocity.dot(to_target) <= 0:
                self.kill()

        if not self.entered_screen and self.rect.colliderect(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
            self.entered_screen = True

    def start_move(self):
        self.started = True

        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

    def take_damage(self, damage,all_sprites, enemies_group, explosions_group, fragment_group):
        self.hp -= damage
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            for _ in range(4):  
                speed =  10
                frag = Fragment(self.fragment_image, self.rect.center, speed)
                all_sprites.add(frag)
                fragment_group.add(frag)    
            self.gm.score += 1
            self.gm.add_laser_score(1)
        self.kill()
                
class MizuakaRotationSpawner:
    def __init__(self,image,all_sprites,enemies_group,center_pos,gm,fragment_image=None,fragment_group=None,speed=4,duration=1200):
        self.image = image
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.center = center_pos
        self.speed = speed
        
        self.frame_count = 0
        self.spawn_timer = 0
        self.duration = duration
        
        self.base_angles = [math.radians(a) for a in [0,120,240]]
        self.spawn_distance = 1000
        self.rotation_speed = math.radians(0.98) #0.85度毎フレーム
        self.gm = gm
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        
    def update(self):
        if self.frame_count >= self.duration:
            return
        
        self.spawn_timer += 1
        self.frame_count += 1
        
        if self.spawn_timer >=10:
            rotation_angle = self.frame_count*self.rotation_speed
            
            for base_angle in self.base_angles:
                angle = base_angle + rotation_angle
                x = self.center[0] + math.cos(angle)*self.spawn_distance
                y = self.center[1] + math.sin(angle)*self.spawn_distance
                
                enemy = MizuakaDirectedMover(self.image,x,y,self.speed,self.center,gm=self.gm,fragment_image=self.fragment_image,fragment_group=self.fragment_group)
                self.all_sprites.add(enemy)
                self.enemies_group.add(enemy)
                
            self.spawn_timer = 0
            
class MizuakaCircleTrap(pygame.sprite.Sprite):
    def __init__(self, image_surface,angle_deg,center_pos,speed=5,gm=None,fragment_image=None,fragment_group=None):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(80,80))
        self.rect = self.image.get_rect()
        
        self.hp = 4
        spawn_radius = 800
        angle_rad = math.radians(angle_deg)
        
        self.rect.centerx = center_pos[0] + math.cos(angle_rad)*spawn_radius
        self.rect.centery = center_pos[1] + math.sin(angle_rad)*spawn_radius
        
        self.pos_x = self.rect.centerx
        self.pos_y = self.rect.centery
        self.rect.center = (int(self.pos_x),int(self.pos_y))
        
        self.vx = -math.cos(angle_rad)*speed
        self.vy = -math.sin(angle_rad)*speed
        
        self.entered_screen = False
        self.radius = self.rect.width // 2
        self.gm = gm
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        
    def update(self,dt):
        self.pos_x += self.vx*dt/16.666
        self.pos_y += self.vy*dt/16.666
        
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)
        
        if not self.entered_screen and self.rect.colliderect(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
            self.entered_screen = True

        if self.entered_screen and (
            self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
            
    def take_damage(self, damage,all_sprites, enemies_group, explosions_group, fragment_group,):
        self.hp -= damage
        if self.hp <= 0:
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            explosions_group.add(exp)
            for _ in range(4):  
                speed =  10
                frag = Fragment(self.fragment_image, self.rect.center, speed)
                all_sprites.add(frag)
                fragment_group.add(frag)    
            self.gm.score += 1
            self.gm.add_laser_score(1)
        self.kill()