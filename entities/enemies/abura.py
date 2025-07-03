if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()
import pygame
import random
import math
from entities.effects import Explosion,Fragment
from config import SCREEN_WIDTH,SCREEN_HEIGHT
class Abura(pygame.sprite.Sprite):
    def __init__(self, image_surface,fragment_image=None,fragment_group=None,gm=None):
        super().__init__()
        self.raw_image_surface = image_surface
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (80, 80))
        self.rect = self.image.get_rect(
            x=SCREEN_WIDTH + random.randint(0, 100),
            y=random.randint(50, SCREEN_HEIGHT - 50)
        )
        self.speed = 4
        self.hp = 8
        self.radius = self.rect.width // 2
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.gm = gm
        
    def take_damage(self, damage,all_sprites, enemies_group, explosions_group,fragment_group):
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

    def update(self,dt):
        self.rect.x -= self.speed*dt/16.666
        if self.rect.right < 0:
            self.kill()
        
class AburaRight(Abura):
    def __init__(self,image_surface,fragment_image=None,fragment_group=None,gm=None):
        super().__init__(image_surface,fragment_image=fragment_image,fragment_group=fragment_group,gm=gm)
        self.raw_image_surface = image_surface
        raw_image = pygame.transform.flip(image_surface.convert_alpha(),True,False)
        self.image = pygame.transform.scale(raw_image,(80,80))
        self.rect = self.image.get_rect(
            x=-100,
            y=random.randint(50,SCREEN_HEIGHT-50)    
        )
        self.speed = 4
        self.hp = 8
        self.radius = self.rect.width // 2
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.gm = gm
        
    def update(self,dt):
        self.rect.x += self.speed*dt/16.666
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
            
class AburaUp(Abura):
    def __init__(self,image_surface,fragment_image=None,fragment_group=None,gm=None):
        super().__init__(image_surface,fragment_image=fragment_image,fragment_group=fragment_group,gm=gm)
        self.raw_image_surface = image_surface
        raw_image = pygame.transform.rotate(image_surface.convert_alpha(),90)
        self.image  = pygame.transform.scale(raw_image,(80,80))
        self.rect = self.image.get_rect(
            x=random.randint(50,SCREEN_WIDTH-50),
            y=SCREEN_HEIGHT + 100
        )
        self.speed = 4
        self.hp = 8
        self.radius = self.rect.width // 2
        self.fragment_image=fragment_image
        self.fragment_group=fragment_group
    
    def update(self,dt):
        self.rect.y -= self.speed*dt/16.666
        if self.rect. bottom < 0:
            self.kill()

class AburaDown(Abura):
    def __init__(self,image_surface,fragment_image=None,fragment_group=None,gm=None):
        super().__init__(image_surface,fragment_image=fragment_image,fragment_group=fragment_group,gm=gm)
        self.raw_image_surface = image_surface
        raw_image = pygame.transform.rotate(image_surface.convert_alpha(),-90)
        self.image = pygame.transform.scale(raw_image,(80,80))
        self.rect = self.image.get_rect(
            x=random.randint(50,SCREEN_WIDTH-50),
            y=-100
        )
        self.speed=4
        self.hp = 8
        self.radius = self.rect.width // 2
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.gm = gm

    def update(self,dt):
        self.rect.y += self.speed*dt/16.666
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            
            

                
class AburaSlow(Abura):
    def __init__(self, image_surface,all_sprites,slow_bullet_group,fragment_image=None,fragment_group=None,gm=None):
        super().__init__(image_surface,fragment_image=fragment_image,fragment_group=fragment_group,gm=gm)
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(100,100))
        self.rect = self.image.get_rect(x=SCREEN_WIDTH + 50,y=random.randint(50,SCREEN_HEIGHT-50))
        self.speed = 3
        self.shot_timer = 0
        self.hp = 8
        self.all_sprites = all_sprites
        self.slow_bullets_group = slow_bullet_group
        self.radius = self.rect.width // 2
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.gm = gm
                
    def update(self,dt):
        self.rect.x -= self.speed*dt/16.666
        self.shot_timer += 1
        if self.shot_timer % 150 == 0:
            self.shoot()
            
        if self.rect.right < 0 :
            self.kill()
            
    def shoot(self):
        for angle in [-30,0,30]:
            slow_bullet = SlowBullet(self.rect.center,angle)
            self.all_sprites.add(slow_bullet)
            self.slow_bullets_group.add(slow_bullet)
            
class SlowBullet(pygame.sprite.Sprite):
    def __init__(self,pos,angle_deg):
        super().__init__()
        self.image = pygame.Surface((12,12),pygame.SRCALPHA)
        pygame.draw.circle(self.image,(255,200,100),(6,6),6)
        self.rect = self.image.get_rect(center=pos)
        self.angle = math.radians(angle_deg+180)
        self.speed = 5
        self.radius = self.rect.width // 2
    
        
    def update(self,dt):
        self.rect.x += self.speed*math.cos(self.angle)*dt/16.666
        self.rect.y += self.speed*math.sin(self.angle)*dt/16.666
        if not (0 <= self.rect.x <= SCREEN_WIDTH and 0 <= self.rect.y <= SCREEN_HEIGHT):
            self.kill()
            
class AburaFormation(Abura):
    def __init__(self, image_surface, all_sprites, enemies_group,fragment_image=None,fragment_group=None,gm=None):
        super().__init__(image_surface,fragment_image=fragment_image,fragment_group=fragment_group,gm=gm)
        self.members = []

        self.image = pygame.Surface((1, 1))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(x=0, y=0)

        start_x = SCREEN_WIDTH + 50
        start_y = 100

        spacing_x = 80
        spacing_y = 80

        formation_pattern = [
            (0, 0), (1, 0), (2, 0), 
            (3, 1), (3, 2),
            (1, 3), (2, 3), (3, 3),
            (0, 4), (0, 5),
            (0, 6), (1, 6), (2, 6), (3, 6),
        ]

        for pos in formation_pattern:
            abura = AburaFormationMember(
                image_surface,
                start_x + pos[0] * spacing_x,
                start_y + pos[1] * spacing_y,
                fragment_image=fragment_image,
                fragment_group=fragment_group,
                gm=gm
            )
            self.members.append(abura)
            all_sprites.add(abura)
            enemies_group.add(abura)

        self.state = "entering"
        self.timer = 0
        self.enter_speed = 8  # 速め
        self.leave_speed = 2  # ゆっくり
        self.radius = self.rect.width // 2
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.gm = gm
        
    def update(self,dt):
        current_time = pygame.time.get_ticks()

        if self.state == "entering":
            all_inside = True
            for member in self.members:
                member.rect.x -= self.enter_speed*dt/16.666
                
                if member.rect.right > SCREEN_WIDTH - 50:
                    all_inside = False
            if all_inside:
                self.state = "waiting"
                self.timer = current_time

        elif self.state == "waiting":
            if current_time - self.timer >= 3000:
                self.state = "leaving"

        elif self.state == "leaving":
            for member in self.members:
                member.rect.x -= self.leave_speed*dt/16.666
                if member.rect.right < 0:
                    member.kill()

class AburaFormationMember(Abura):
    def __init__(self, image_surface, x, y,fragment_image=None,fragment_group=None,gm=None):
        super().__init__(image_surface,fragment_image=fragment_image,fragment_group=fragment_group,gm=gm)
        raw_image = image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (60, 60)) 
        self.rect = self.image.get_rect(x=x, y=y)
        self.hp = 4
        self.radius = self.rect.width // 2
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.gm = gm
    def update(self, dt):
        pass
            
class AburaStopShooter(Abura):
    def __init__(self,image_surface,all_sprites,slow_bullet_group,player,fragment_image=None,fragment_group=None,gm=None):
        super().__init__(image_surface,fragment_image=fragment_image,fragment_group=fragment_group,gm=gm)
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(80,80))
        self.rect = self.image.get_rect(
            x=random.randint(50,SCREEN_WIDTH-50),
            y=-80
        )
        self.speed = 4
        self.hp = 8
        self.has_stopped = False
        self.shoot_timer = 0
        self.all_sprites = all_sprites
        self.slow_bullet_group = slow_bullet_group
        self.player = player
        self.radius = self.rect.width // 2
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.gm = gm
        
    def update(self,dt):
        if not self.has_stopped:
            self.rect.y += self.speed*dt/16.666
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.has_stopped = True
                
        else:
            self.shoot_timer += 1
            if self.shoot_timer % 120 == 0:
                self.shoot()
                
    def shoot(self):
        target = self.player.rect.center
        pos = self.rect.center
        
        dx = target[0]-pos[0]
        dy = target[1] -pos[1]
        angle_rad = math.atan2(dy,dx)
        angle_deg = math.degrees(angle_rad) - 180
        
        slow_bullet = SlowBullet(pos,angle_deg)
        self.all_sprites.add(slow_bullet)
        self.slow_bullet_group.add(slow_bullet)
            
class AburaCurveCharger(Abura):
    def __init__(self, image_surface, player, all_sprites, enemies_group,fragment_image=None,fragment_group=None,gm=None):
        super().__init__(image_surface,fragment_image=fragment_image,fragment_group=fragment_group,gm=gm)
        self.image = pygame.transform.scale(image_surface.convert_alpha(), (80, 80))
        self.rect = self.image.get_rect(
            x=random.randint(100, SCREEN_WIDTH - 100),
            y=-80
        )
        self.state = "falling"
        self.timer = 0
        self.wait_time = 90
        self.hp = 16
        self.speed = 4
        self.player = player
        self.t = 0
        self.p1 = None
        self.p2 = None
        self.bezier_speed = 0.010

        self.all_sprites = all_sprites
        self.enemies_group = enemies_group

        self.direction = pygame.math.Vector2(0, 0)
        self.radius = self.rect.width // 2
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.gm = gm
        
    def update(self,dt):
        if self.state == "falling":
            self.rect.y += self.speed*dt/16.666
            if self.rect.y >= 50:
                self.rect.y = 50
                self.state = "waiting"
                self.timer = 0

        elif self.state == "waiting":
            self.timer += 1
            if self.timer >= self.wait_time:
                self.state = "charging"
                self.t = 0
                self.p0 = pygame.math.Vector2(self.rect.center)
                self.p2 = pygame.math.Vector2(self.player.rect.center)
                
                direction = self.p2 - self.p0
                normal = pygame.math.Vector2(-direction.y,direction.x).normalize()
                distance = direction.length()
                bend = random.uniform(-0.6,0.6)#曲げ強度調整
                self.p1 = self.p0 +direction*0.5+normal*distance*bend
    
                
        elif self.state == "charging":
            self.t += self.bezier_speed
                
            one_minus_t = 1 - self.t
            pos = (one_minus_t**2)*self.p0+\
                    2*one_minus_t*self.t*self.p1+\
                    (self.t**2)*self.p2
            
            self.rect.center = (int(pos.x),int(pos.y))
                
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()