if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()
import pygame
import random
import math
from entities.effects import Explosion,Fragment
from config import SCREEN_WIDTH,SCREEN_HEIGHT
from asset_loader import load_images

class Sabi(pygame.sprite.Sprite):
    def __init__(self, image_surface, dy=0, can_split=True,gm=None,fragment_image=None,fragment_group=None):
        super().__init__()
        self.original_surface = image_surface
        self.raw_image_surface = image_surface
        self.raw_image_path = image_surface
        self.target_pos = None
        self.moving_timer = 0
        raw_image =self.raw_image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (80, 80))
        self.rect = self.image.get_rect(
            x=SCREEN_WIDTH + random.randint(0, 100),
            y=random.randint(50, SCREEN_HEIGHT - 50)
        )
        self.speed = 4
        self.hp = 2
        self.dy = dy
        self.dy_timer = 45
        self.can_split = can_split
        self.split_timer = 180
        self.radius = self.rect.width // 2
        self.gm = gm   
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.gm = gm 

    def split(self, all_sprites, enemies_group):
        changed_angle = random.random() < 0.40
        num_split = 3
        r = 150
        base_angle = math.radians(60 if changed_angle else 30)

        offsets = []
        for i in range(num_split):
            angle = base_angle + math.radians(360 / num_split * i)
            x_offset = r * math.cos(angle)
            y_offset = r * math.sin(angle)
            offsets.append((x_offset, y_offset))

        for x_offset, y_offset in offsets:
            new_sabi = Sabi(self.raw_image_surface, dy=0, can_split=False,gm=self.gm,fragment_image=self.fragment_image,fragment_group=self.fragment_group)
            new_sabi.rect.center = self.rect.center
            new_sabi.target_pos = (
                self.rect.centerx + int(x_offset),
                self.rect.centery + int(y_offset)
            )
            new_sabi.moving_timer = 45

            raw_image = self.raw_image_surface.convert_alpha()
            scaled_image = pygame.transform.scale(self.original_surface,(60,60))
            new_sabi.image = scaled_image
            new_sabi.rect = new_sabi.image.get_rect(center=new_sabi.rect.center)

            new_sabi.speed = self.speed + 2
            new_sabi.hp = 4

            all_sprites.add(new_sabi)
            enemies_group.add(new_sabi)

    def update(self,dt):
        if self.moving_timer > 0 and self.target_pos:
            move_rate = 1 / self.moving_timer
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            self.rect.centerx += int(dx * move_rate)
            self.rect.centery += int(dy * move_rate)
            self.moving_timer -= 1
            if self.moving_timer == 0:
                self.target_pos = None

        self.rect.x -= self.speed*dt/16.666
        self.rect.y += self.dy
        if self.dy_timer > 0:
            self.dy_timer -= 1
            if self.dy_timer == 0:
                self.dy = 0

        if (self.rect.left > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT or
            self.rect.bottom < 0):
            self.kill()

    def take_damage(self, damage,all_sprites, enemies_group, explosions_group,fragment_group):
        self.hp -= damage
        if self.hp <= 0:
            if self.can_split:
                self.split(all_sprites, enemies_group)
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            for _ in range(4):
                speed = 10
                frag = Fragment(
                    self.fragment_image,
                    self.rect.center,
                    speed
                )
                all_sprites.add(frag)
                fragment_group.add(frag)
            self.gm.score += 1
            self.gm.add_laser_score(1)
            self.kill()
            
class SabiInversed(Sabi):
    def __init__(self,image_surface,dy=0,can_split=True,gm=None,fragment_image=None,fragment_group=None):
        super().__init__(image_surface,dy,can_split,gm=gm, fragment_image=fragment_image,fragment_group=fragment_group)
        self.hp = 2
        self.radius = self.rect.width // 2
        self.gm = gm
    def split(self,all_sprites,enemies_group):
        changed_angle = random.random() < 0.40
        num_split = 3
        r = 150
        base_angle = math.radians(60 if changed_angle else 30)  

        offsets = []
        for i in range(num_split):
            angle = base_angle + math.radians(360 / num_split * i)
            x_offset = r * math.cos(angle)
            y_offset = r * math.sin(angle)
            offsets.append((x_offset, y_offset))

        for x_offset, y_offset in offsets:
            new_sabi = SabiInversed(self.raw_image_surface, dy=0, can_split=False,gm=self.gm,fragment_image=self.fragment_image,fragment_group=self.fragment_group)
            new_sabi.rect.center = self.rect.center
            new_sabi.target_pos = (
                self.rect.centerx + int(x_offset),
                self.rect.centery + int(y_offset)
            )
            new_sabi.moving_timer = 45

            raw_image = self.raw_image_surface.convert_alpha()
            scaled_image = pygame.transform.scale(self.original_surface,(60,60))
            new_sabi.image = scaled_image
            new_sabi.rect = new_sabi.image.get_rect(center=new_sabi.rect.center)

            new_sabi.speed = self.speed + 2
            new_sabi.hp = 4

            all_sprites.add(new_sabi)
            enemies_group.add(new_sabi)  
                
    def update(self,dt):
        if self.moving_timer > 0 and self.target_pos:
            move_rate = 1 / self.moving_timer
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            self.rect.centerx += int(dx * move_rate)
            self.rect.centery += int(dy * move_rate)
            self.moving_timer -= 1
            if self.moving_timer == 0:
                self.target_pos = None   

        self.rect.x += self.speed*dt/16.666
        self.rect.y += self.dy
        if self.dy_timer > 0:
            self.dy_timer -= 1
            if self.dy_timer == 0:
                self.dy = 0

        if (self.rect.left > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT or
            self.rect.bottom < 0):
            self.kill()

    def take_damage(self, damage,all_sprites, enemies_group, explosions_group,fragment_group):
        self.hp -= damage
        if self.hp <= 0:
            if self.can_split:
                self.split(all_sprites, enemies_group)
            exp = Explosion(self.rect.center)
            all_sprites.add(exp)
            for _ in range(4):
                speed = 10
                frag = Fragment(self.fragment_image,self.rect.center,speed)
                all_sprites.add(frag)
                fragment_group.add(frag)
            self.gm.score += 1
            self.gm.add_laser_score(1)
            self.kill()
    
class SabiPlus(Sabi):
    def __init__(self, image_surface, dy=0, can_split=True,gm=None,fragment_image=None,fragment_group=None):
        super().__init__(image_surface, dy, can_split,gm=gm, fragment_image=fragment_image,fragment_group=fragment_group)
        self.hp = 2
        self.radius = self.rect.width // 2
        self.gm = gm
    def split(self, all_sprites, enemies_group):
        num_split = 6
        r = 120
        base_angle = math.radians(15)
        
        offsets = []
        for i in range(num_split):
            angle = base_angle + math.radians(360/num_split*i)
            x_offset = r*math.cos(angle)
            y_offset = r*math.sin(angle)
            offsets.append((x_offset,y_offset))
            
        for x_offset,y_offset in offsets:
            new_sabi = SabiPlus(self.raw_image_surface,dy=0,can_split=False,gm=self.gm,fragment_image=self.fragment_image,fragment_group=self.fragment_group)
            new_sabi.rect.center = self.rect.center
            new_sabi.target_pos = (
                self.rect.centerx + int(x_offset),
                self.rect.centery + int(y_offset)
            )
            new_sabi.moving_timer = 45
            
            scaled_image = pygame.transform.scale(self.original_surface,(50,50))
            new_sabi.image = scaled_image
            new_sabi.rect = new_sabi.image.get_rect(center=new_sabi.rect.center)
            
            new_sabi.speed = self.speed + 1
            new_sabi.hp = 4
            
            all_sprites.add(new_sabi)
            enemies_group.add(new_sabi)
    
    def update(self,dt):
        self.rect.x += self.speed*dt/16.666
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class SabiOrbit(Sabi):
    def __init__(self, image_surface, dy=0, can_split=True,is_child = False,shared_center=None,orbit_angle=0,gm=None,fragment_image=None,fragment_group=None):
        super().__init__(image_surface, dy, can_split,gm=gm, fragment_image=fragment_image,fragment_group=fragment_group)
        
        self.is_child = is_child
        self.orbit_radius = 100
        self.orbit_angle = orbit_angle
        self.orbit_speed = -0.05 # 時計回り
        self.radius = self.rect.width // 2
        self.gm = gm
        
        if self.is_child:
            self.center_point = shared_center
            self.target_pos = None
            self.moving_timer = 0
            self.is_orbiting = True
        else:
            self.rect.centerx = SCREEN_WIDTH -50
            self.rect.centery = random.randint(100,SCREEN_HEIGHT - 100)
            self.target_pos = None
            self.moving_timer = 0
            self.is_orbiting = False
        
    def update(self,dt):
        if self.is_child:
            if self.moving_timer > 0:
                self.moving_timer -= 1
                lerp_factor = 1 - (self.moving_timer / 45)
                new_x = int(self.rect.centerx + (self.target_pos[0] - self.rect.centerx) * lerp_factor)
                new_y = int(self.rect.centery + (self.target_pos[1] - self.rect.centery) * lerp_factor)
                self.rect.center = (new_x, new_y)
            
                if self.moving_timer == 0:
                    self.center_point = self.rect.center
                    self.is_orbiting = True
                       
            elif self.is_orbiting:
                self.center_point = (
                    self.center_point[0]+4,
                    self.center_point[1]
                )
                self.orbit_angle += self.orbit_speed
                self.rect.centerx = int(self.center_point[0] + self.orbit_radius * math.cos(self.orbit_angle))
                self.rect.centery = int(self.center_point[1] + self.orbit_radius * math.sin(self.orbit_angle))
            
            else:
                self.rect.x += self.speed*dt/16.666
        else:
            self.rect.x += self.speed*dt/16.666

            
        if (self.rect.left > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT or
        self.rect.bottom < 0 or self.rect.right < 0):
            self.kill()
            
    def split(self, all_sprites, enemies_group):
        num_split = 3
        r = 100
        base_angle = math.radians(0)
    
        shared_center = self.rect.center 
    
        offsets = []
        for i in range(num_split):
            angle = base_angle + math.radians(360 / num_split * i)
            x_offset = r * math.cos(angle)
            y_offset = r * math.sin(angle)
            offsets.append((angle, x_offset, y_offset))
    
        for angle, x_offset, y_offset in offsets:
            new_orbit = SabiOrbit(
                self.raw_image_surface,
                dy=0,
                can_split=False,
                is_child=True,
                shared_center=shared_center,
                orbit_angle=angle,
                gm= self.gm,
                fragment_image=self.fragment_image
            )
            new_orbit.rect.centerx = int(shared_center[0] + r * math.cos(angle))
            new_orbit.rect.centery = int(shared_center[1] + r * math.sin(angle))
        
            scaled_image = pygame.transform.scale(self.original_surface, (50, 50))
            new_orbit.image = scaled_image
            new_orbit.rect = new_orbit.image.get_rect(center=new_orbit.rect.center)
        
            new_orbit.speed = self.speed + 1
            new_orbit.hp = 4
        
            all_sprites.add(new_orbit)
            enemies_group.add(new_orbit)

class SabiBind(Sabi):
    def __init__(self,image_surface,dy=0,can_split=True,gm=None,fragment_image=None,fragment_group=None):
        super().__init__(image_surface,dy,can_split,gm=gm, fragment_image=fragment_image,fragment_group=fragment_group)
        self.contact_damage = 1
        self.bind_duration = 120
        self.gm = gm
        self.radius = self.rect.width // 2
        
    def update(self):
        super().update()
        
        if pygame.sprite.collide_rect(self,self.gm.player):
            if not self.gm.player_bound:
                self.gm.player_bound = True
                self.gm.bound_timer = self.bind_duration
                self.gm.lives -= self.contact_damage

class SabiFormation(pygame.sprite.Sprite):
    def __init__(self, image_surface, all_sprites, enemies_group,gm=None,fragment_image=None,fragment_group=None):
        super().__init__()
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.members = []

        self.image = pygame.Surface((1, 1))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(x=0, y=0)

        start_x = SCREEN_WIDTH + 50
        start_y = 100

        spacing_x = 80
        spacing_y = 80
        self.gm = gm
        formation_pattern = [
            (0, 0), (1, 0), (2, 0),
            (3, 1), (3, 2),
            (0, 3), (1, 3), (2, 3), 
            (3, 4), (3, 5),
            (0, 6), (1, 6), (2, 6), 
        ]

        for pos in formation_pattern:
            sabi = SabiFormationMember(
                image_surface,
                start_x + pos[0] * spacing_x,
                start_y + pos[1] * spacing_y,
                gm=self.gm,
                fragment_image=self.fragment_image,
                fragment_group=self.fragment_group
            )
            self.members.append(sabi)
            all_sprites.add(sabi)
            enemies_group.add(sabi)

        self.state = "entering"
        self.timer = 0
        self.enter_speed = 8  # 速め
        self.leave_speed = 2  # ゆっくり
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        current_time = pygame.time.get_ticks()

        if self.state == "entering":
            all_inside = True
            for member in self.members:
                member.rect.x -= self.enter_speed
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

class SabiFormationMember(Sabi):
    def __init__(self, image_surface, x, y,gm=None, fragment_image=None,fragment_group=None):
        super().__init__(image_surface, dy=0, can_split=False,gm=gm,fragment_image=fragment_image,fragment_group=fragment_group)
        raw_image = self.raw_image_surface.convert_alpha()
        self.image = pygame.transform.scale(raw_image, (60, 60))  
        self.rect = self.image.get_rect(x=x, y=y)
        self.hp = 4
        self.radius = self.rect.width // 2
        self.gm = gm
        self.fragment_image = fragment_image
    def update(self,dt):
        pass   
    
class SabiCharger(Sabi):
    def __init__(self, image_surface, dy=0, can_split=True,player = None,all_sprites=None,enemies_group=None,gm=None,fragment_image=None,fragment_group=None):
        super().__init__(image_surface, dy=dy, can_split=can_split,gm=gm, fragment_image=fragment_image,fragment_group=fragment_group)
        self.player = player
        self.spawn_time = pygame.time.get_ticks()
        self.split_triggered = False
        
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.radius = self.rect.width // 2
        self.gm = gm
        
    def update(self,dt):
        self.rect.x -= self.speed*dt/16.666
        self.rect.y += self.dy
        
        current_time = pygame.time.get_ticks()
        if not self.split_triggered and (current_time - self.spawn_time >= 2000):
            self.split_triggered = True
            self.split(self.all_sprites,self.enemies_group)
            self.kill()
            
        if (self.rect.right < 0 or self.rect.top > SCREEN_HEIGHT or
            self.rect.bottom < 0):
            self.kill()
            
    def split(self, all_sprites, enemies_group):
        new_sabi = Sabi(
        self.raw_image_surface,
        dy=0,
        can_split=False,
        gm=self.gm,
        fragment_image=self.fragment_image,
        fragment_group=self.fragment_group
    )
        spacing = 100 #縦の感覚
        positions = [
            (self.rect.centerx,self.rect.centery - spacing),
            (self.rect.centerx,self.rect.centery),
            (self.rect.centerx,self.rect.centery + spacing)
        ]
        
        for pos in positions:
            child = SabiChargerChild(
                self.raw_image_surface,
                start_pos=pos,
                player=self.player,
                fragment_image=self.fragment_image,
                gm=self.gm
            )
            all_sprites.add(child)
            enemies_group.add(child)

class SabiChargerInversed(Sabi):
    def __init__(self, image_surface, dy=0, can_split=True,player = None,all_sprites=None,enemies_group=None,gm=None,fragment_image=None,fragment_group=None):
        super().__init__(image_surface,dy, can_split,gm=gm, fragment_image=fragment_image,fragment_group=fragment_group)
        self.player = player
        self.spawn_time = pygame.time.get_ticks()
        self.split_triggered = False
        
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.radius = self.rect.width // 2
        self.gm = gm
        
    def update(self,dt):
        self.rect.x += self.speed*dt/16.666
        self.rect.y += self.dy
        
        current_time = pygame.time.get_ticks()
        if not self.split_triggered and (current_time - self.spawn_time >= 1500):
            self.split_triggered = True
            self.split(self.all_sprites,self.enemies_group)
            self.kill()
            
        if (self.rect.right > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT or
            self.rect.bottom < 0):
            self.kill()
            
    def split(self, all_sprites, enemies_group):
        new_sabi = Sabi(
        self.raw_image_surface,
        dy=0,
        can_split=False,
        gm=self.gm,
        fragment_image=self.fragment_image,
        fragment_group=self.fragment_group
    )
        spacing = 100 #縦の感覚
        positions = [
            (self.rect.centerx,self.rect.centery - spacing),
            (self.rect.centerx,self.rect.centery),
            (self.rect.centerx,self.rect.centery + spacing)
        ]
        
        for pos in positions:
            child = SabiChargerChild(
                self.raw_image_surface,
                start_pos=pos,
                player=self.player,
                fragment_image=self.fragment_image,
                gm=self.gm
            )
            all_sprites.add(child)
            enemies_group.add(child)
            
class SabiChargerChild(pygame.sprite.Sprite):
    def __init__(self,image_surface,start_pos,player,gm=None,fragment_image=None):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(50,50))
        self.rect = self.image.get_rect(center=start_pos)
        self.player = player
        self.speed = 7
        self.hp = 4
        self.radius = self.rect.width // 2
        self.fragment_image = fragment_image
        self.gm = gm
        
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dx,dy)
        self.gm = gm
        if distance == 0:
            distance = 1
            
        self.velocity_x = self.speed * dx / distance
        self.velocity_y = self.speed*dy / distance
        
    def update(self,dt):
        self.rect.x += self.velocity_x*dt/16.666
        self.rect.y += self.velocity_y*dt/16.666
        
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
