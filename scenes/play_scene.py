if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()

import pygame
from entities.bullet import Bullet
from entities.laser import Laser
from entities.enemies import Mizuaka, Abura, Sabi
from entities.enemies.mizuaka import Mizuaka,MizuakaShooter,MizuakaZigZag,MizuakaZigZagInversed,MizuakaRightMover,MizuakaFormation,MizuakaUpLeftMover,MizuakaDownLeftMover,MizuakaFormationMember,MizuakaDirectedMover,MizuakaRotationSpawner,MizuakaCircleTrap
from entities.enemies.abura import AburaSlow,AburaFormationMember,AburaUp,AburaDown,AburaRight,AburaStopShooter,AburaCurveCharger
from entities.enemies.sabi import Sabi,SabiInversed,SabiPlus,SabiOrbit,SabiBind,SabiCharger,SabiChargerChild,SabiChargerInversed,SabiFormationMember
from entities.enemies.kabi import Kabi,KabiRight,KabiRightSmoke,KabiSmoke,KabiRateSmoke,KabiFormationMember,KabiUpMover,KabiDownMover,UpMoverSmoke,DownMoverSmoke
from entities.enemies.boss import Boss
from entities.laser import point_to_line_distance
from ui.draw_bg import draw_bg
from ui.render_text import render_text
from ui.draw_gauge import draw_gauge
from config import SCREEN_HEIGHT, GREEN,BLACK
from core.gamestate import GameState

def run_play_logic(dt,screen, gm, player, all_sprites, enemies, bullets, explosions, IMG, SE, now, scroll, is_shooting, last_shot_time, slow_bullets_group, mizuaka_bullets_group,boss_bullets_group):
    from core.spawn_enemy import spawn_enemy
    fragment_group = pygame.sprite.Group()
    gm.img = IMG
    if pygame.mouse.get_pressed()[2]:
        if gm.can_use_laser and not gm.laser_active:
            gm.want_to_fire_laser = True

    def wrapped_spawn_enemy(enemy_type, x, y, speed=None, x_speed_factor=None):
        spawn_enemy(
            enemy_type, x, y,
            IMG,
            all_sprites,
            enemies,gm,
            extra_groups={
                "slow_bullets": slow_bullets_group,
                "mizuaka_bullets": mizuaka_bullets_group
            },
            player=player,
            speed=speed,
            x_speed_factor=x_speed_factor
        )

    if not hasattr(gm, "active_laser"):
        gm.active_laser = None

    if gm.player_bound:
        gm.bound_timer -= 1
        if gm.bound_timer <= 0:
            gm.player_bound = False

    player.update(gm)

    if gm.stage_controller is None:
        from core.stage_controller import StageController
        gm.stage_controller = StageController(gm, all_sprites, enemies, wrapped_spawn_enemy)

    gm.stage_controller.update(gm.elapsed_time)

    if is_shooting and now - last_shot_time > gm.bullet_cooldown:
        b = Bullet(player.rect.center, pygame.mouse.get_pos(), gm.bullet_type)
        all_sprites.add(b)
        bullets.add(b)
        last_shot_time = now

    if getattr(gm, "want_to_fire_laser", False):
        gm.want_to_fire_laser = False  # フラグを折る
        gm.activate_laser()
        gm.active_laser = Laser(player,pygame.mouse.get_pos())

    if gm.active_laser and not gm.active_laser.is_expired():
        gm.active_laser.update(dt)
        gm.active_laser.draw(screen)
        if not gm.active_laser.is_expired():
            for enemy in enemies:
                dist = point_to_line_distance(enemy.rect.center,gm.active_laser.start_pos,gm.active_laser.target_pos)
                if dist < enemy.radius:
                    if hasattr(enemy,"take_damage"):
                        enemy.take_damage(9999,all_sprites,enemies,explosions,fragment_group)

    if gm.laser_active and now - gm.laser_start_time >= 2000:
        gm.laser_active = False
        if gm.active_laser:
            gm.active_laser.kill()
            gm.active_laser = None
            
    for sprite in all_sprites:
        if isinstance(sprite,Boss):
            sprite.update(dt,player)
        elif sprite != player:
            sprite.update(dt)

    for enemy in enemies:
        if isinstance(enemy, SabiBind):
            if enemy.rect.colliderect(player.hitbox):
                if not gm.player_bound:
                    gm.player_bound = True
                    gm.bound_timer = enemy.bind_duration
                    gm.lives -= enemy.contact_damage
                    SE["hit"].play()
                    enemy.kill()
            continue

        if isinstance(enemy, KabiRateSmoke) and enemy.rect.colliderect(player.hitbox):
            enemy.kill()
            gm.rate_down_timer = pygame.time.get_ticks()
            gm.rate_down_active = True
            continue

        if enemy.rect.colliderect(player.hitbox):
            enemy.kill()
            SE["hit"].play()
            gm.lives -= 1
            if gm.laser_active:
                gm.laser_active = False
                if gm.active_laser:
                    gm.active_laser.kill()
                    gm.active_laser = None
            if gm.lives <= 0:
                gm._resume_offset = gm.elapsed_time
                gm.state = GameState.GAMEOVER

    hit = pygame.sprite.groupcollide(enemies, bullets, False, False)
    for enemy, bullet_list in hit.items():
        if isinstance(enemy, (KabiSmoke, KabiRateSmoke, UpMoverSmoke, DownMoverSmoke, KabiRightSmoke)):
            continue
        total_damage = 0
        for bullet in bullet_list:
            if not isinstance(bullet, Bullet):
                continue
            damage = 2
            if isinstance(enemy, (Mizuaka, MizuakaRightMover, MizuakaFormation, MizuakaShooter, MizuakaZigZag, MizuakaZigZagInversed, MizuakaFormationMember, MizuakaUpLeftMover, MizuakaDownLeftMover, MizuakaDirectedMover, MizuakaCircleTrap)) and bullet.type == 1:
                damage = 4
            elif isinstance(enemy, (Abura, AburaSlow, AburaFormationMember, AburaUp, AburaRight, AburaDown, AburaStopShooter, AburaCurveCharger)) and bullet.type == 2:
                damage = 4
            elif isinstance(enemy, (Sabi, SabiInversed, SabiPlus, SabiOrbit, SabiBind, SabiCharger, SabiChargerInversed, SabiFormationMember, SabiChargerChild)) and bullet.type == 3:
                damage = 4
            elif isinstance(enemy, (Kabi, KabiUpMover, KabiDownMover, KabiFormationMember, KabiRight)) and bullet.type == 4:
                damage = 4
            total_damage += damage
            bullet.kill()
        if hasattr(enemy, "take_damage"):
            enemy.take_damage(total_damage, all_sprites, enemies, explosions,fragment_group)

    slowhit = pygame.sprite.spritecollide(player, slow_bullets_group, True)
    if slowhit:
        player.slow_timer = 120

    mizuaka_hits = pygame.sprite.spritecollide(player, mizuaka_bullets_group, True)
    if mizuaka_hits:
        for hit in mizuaka_hits:
            gm.lives -= 1
            SE["hit"].play()
            if gm.lives <= 0:
                gm._resume_offset = gm.elapsed_time
                gm.state = GameState.GAMEOVER
    
    boss_hits = pygame.sprite.spritecollide(player, boss_bullets_group, True)
    if boss_hits:
        for hit in boss_hits:
            gm.lives -= 1
            SE["hit"].play()
            if gm.lives <= 0:
                gm._resume_offset = gm.elapsed_time
                gm.state = GameState.GAMEOVER
    
    scroll += 1.0
    draw_bg(screen, IMG["bg_top"], scroll, 0)
    draw_bg(screen, IMG["bg_bot"], scroll, SCREEN_HEIGHT // 2)
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)
    if gm.active_laser:
        gm.active_laser.draw(screen)
    if gm.laser_active:
        elapsed = now - gm.laser_start_time
        gm.laser_gauge = max(0, 100 * (1 - elapsed / 2000))
    else:
        gm.update_laser_gauge(dt)

    render_text(screen, gm.font, f"スコア: {gm.score}", (900, 20), BLACK)
    m, s = gm.minutes, gm.seconds
    render_text(screen, gm.font, f"時間: {m:02d}:{s:02d}", (20, 20), BLACK)
    
    player_icon = pygame.transform.scale(gm.img["player"],(40,40))
    for i in range(gm.lives):
        x = 60 + i*50
        y = 60
        screen.blit(player_icon,(x - player_icon.get_width()//2,
                                 y - player_icon.get_height()//2))
    draw_gauge(screen, gm.laser_gauge)

    return scroll, last_shot_time
