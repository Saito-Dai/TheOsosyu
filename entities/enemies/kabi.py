if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()
import pygame
import random
from entities.effects import Explosion,Fragment
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Kabi(pygame.sprite.Sprite):
    def __init__(self, image_surface, smoke_image, all_sprites, enemies_group,gm,fragment_image=None,fragment_group=None):
        super().__init__()
        self.gm = gm
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.image = pygame.transform.scale(image_surface.convert_alpha(), (80,80))
        self.rect = self.image.get_rect(
            x=SCREEN_WIDTH + random.randint(0, 100),
            y=random.randint(50, SCREEN_HEIGHT - 50)
        )
        self.speed = random.randint(3,4)
        self.hp = 4
        self.smoke_image = smoke_image
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.rect.x -= self.speed*dt/16.666
        if self.rect.right < 0:
            self.kill()

    def take_damage(self, damage, all_sprites, enemies_group, explosions_group,fragment_group):
        self.hp -= damage
        if self.hp <= 0:
            SmokeClass = random.choice(SMOKE_CLASS)
            smoke = SmokeClass(self.smoke_image,self.rect.center)
            self.all_sprites.add(smoke)
            self.enemies_group.add(smoke)
            for _ in range(4):
                speed = 10
                frag = Fragment(self.fragment_image,self.rect.center,speed)
                all_sprites.add(frag)
                fragment_group.add(frag)
            self.gm.score += 1
            self.gm.add_laser_score(1)
            self.kill()

class KabiRight(pygame.sprite.Sprite):
    def __init__(self,image_surface,smoke_image,all_sprites,enemies_group,gm,fragment_image=None,fragment_group=None):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(80,80))
        self.rect = self.image.get_rect(
            x = -100+random.randint(0,50),
            y = random.randint(50,SCREEN_HEIGHT-50)
        )
        self.speed = 4
        self.hp = 4
        self.smoke_image = smoke_image
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.radius = self.rect.width // 2
        self.gm = gm
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        
    def update(self,dt):
        self.rect.x += self.speed*dt/16.666
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
            
    def take_damage(self,damage,all_sprites,enemies_group,explosions_group,fragment_group):
        self.hp -= damage
        if self.hp <= 0:
            smoke = KabiRightSmoke(self.smoke_image,self.rect.center)
            self.all_sprites.add(smoke)
            self.enemies_group.add(smoke)
            for _ in range(4):
                speed = 10
                frag = Fragment(self.fragment_image,self.rect.center,speed)
                all_sprites.add(frag)
                fragment_group.add(frag)
            self.gm.score += 1
            self.gm.add_laser_score(1)
            self.kill()

class KabiRightSmoke(pygame.sprite.Sprite):
    def __init__(self,image_surface,center):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(80,80))
        self.rect = self.image.get_rect(center=center)
        self.speed = 3
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.rect.x += self.speed*dt/16.666
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class KabiSmoke(pygame.sprite.Sprite):
    def __init__(self, image_surface, center):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(), (80, 80))
        self.rect = self.image.get_rect(center=center)
        self.speed = 3
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.rect.x -= self.speed*dt/16.666
        if self.rect.right < 0:
            self.kill()
            
class KabiRateSmoke(pygame.sprite.Sprite):
    def __init__(self, image_surface,center):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(80,80))
        self.rect = self.image.get_rect(center=center)
        self.speed = 3
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.rect.x -= self.speed*dt/16.666
        if self.rect.right < 0:
            self.kill()
            
SMOKE_CLASS = [KabiSmoke,KabiRateSmoke]

class KabiFormation(pygame.sprite.Sprite):
    def __init__(self, image_surface, all_sprites, enemies_group,gm,fragment_image=None,fragment_group=None):
        super().__init__()
        self.members = []
        self.gm = gm
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        
        self.image = pygame.Surface((1, 1))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(x=0, y=0)
        self.fragment_group = fragment_group
        start_x = SCREEN_WIDTH + 50
        start_y = 100

        spacing_x = 80
        spacing_y = 80

        formation_pattern = [
            (0, 3),  
            (1, 2),
            (2, 1),
            (3, 0), 
            (3, 1), 
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5),
            (3, 6),
            (2, 3), 
            (1, 3),
            (0, 3),
        ]

        for pos in formation_pattern:
            kabi = KabiFormationMember(
                image_surface,
                start_x + pos[0] * spacing_x,
                start_y + pos[1] * spacing_y,
                gm=self.gm,
                fragment_image=self.fragment_image,
                fragment_group=self.fragment_group
            )
            self.members.append(kabi)
            all_sprites.add(kabi)
            enemies_group.add(kabi)

        self.state = "entering"
        self.timer = 0
        self.enter_speed = 8  
        self.leave_speed = 2  
        self.radius = self.rect.width // 2
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        
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
        
class KabiFormationMember(pygame.sprite.Sprite):
    def __init__(self, image_surface, x, y,gm,fragment_image=None,fragment_group=None):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(), (60, 60))
        self.rect = self.image.get_rect(x=x, y=y)
        self.hp = 4
        self.radius = self.rect.width // 2
        self.gm = gm
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
    def update(self,dt):
        pass

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
            
class KabiDownMover(pygame.sprite.Sprite):
    def __init__(self, image_surface,smoke_image,all_sprites,enemies_group,gm,fragment_image=None,fragment_group=None):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(80,80))
        self.rect = self.image.get_rect(
            x=random.randint(100,SCREEN_WIDTH - 100),
            y = -80
        )
        self.speed = 3
        self.hp = 4 
        self.smoke_image = smoke_image
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.radius = self.rect.width // 2
        self.gm = gm
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        
    def update(self,dt):
        self.rect.y += self.speed*dt/16.666
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
    
    def take_damage(self,damage,all_sprites,enemies_group,explosions_group,fragment_group):
        self.hp -= damage
        if self.hp <=  0:
            smoke = DownMoverSmoke(self.smoke_image,self.rect.center)
            self.all_sprites.add(smoke)
            self.enemies_group.add(smoke)
            for _ in range(4):
                speed = 10
                frag = Fragment(self.fragment_image,self.rect.center,speed)
                all_sprites.add(frag)
                fragment_group.add(frag)
            self.gm.score += 1
            self.gm.add_laser_score(1)
            self.kill()
            
class DownMoverSmoke(pygame.sprite.Sprite):
    def __init__(self, image_surface,center):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(80,80))
        self.rect = self.image.get_rect(center=center)
        self.speed = 3
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.rect.y += self.speed*dt/16.666
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            
class KabiUpMover(pygame.sprite.Sprite):
    def __init__(self, image_surface,smoke_image,all_sprites,enemies_group,gm,fragment_image=None,fragment_group=None):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(80,80))
        self.rect = self.image.get_rect(
            x=random.randint(100,SCREEN_WIDTH - 100),
            y = 810
        )
        self.speed = 3
        self.hp = 4 
        self.smoke_image = smoke_image
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.radius = self.rect.width // 2
        self.gm = gm
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        
    def update(self,dt):
        self.rect.y -= self.speed*dt/16.666
        if self.rect.bottom < 0:
            self.kill()
    
    def take_damage(self,damage,all_sprites,enemies_group,explosions_group,fragment_group):
        self.hp -= damage
        if self.hp <=  0:
            smoke = UpMoverSmoke(self.smoke_image,self.rect.center)
            self.all_sprites.add(smoke)
            self.enemies_group.add(smoke)
            for _ in range(4):
                speed = 10
                frag = Fragment(self.fragment_image,self.rect.center,speed)
                all_sprites.add(frag)
                fragment_group.add(frag)
            self.gm.score += 1
            self.gm.add_laser_score(1)
            self.kill()

class UpMoverSmoke(pygame.sprite.Sprite):
    def __init__(self, image_surface,center):
        super().__init__()
        self.image = pygame.transform.scale(image_surface.convert_alpha(),(80,80))
        self.rect = self.image.get_rect(center=center)
        self.speed = 3
        self.radius = self.rect.width // 2
        
    def update(self,dt):
        self.rect.y -= self.speed*dt/16.666
        if self.rect.bottom < 0:
            self.kill()
            