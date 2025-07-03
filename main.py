#---ライブラリとモジュールの読み込み---
import pygame
import pygame.freetype
import os, random, math

from entities.player import Player 
from entities.bullet import Bullet
from entities.laser import Laser
from entities.enemies import Mizuaka, Abura, Sabi,Kabi
from entities.effects import Explosion
from ui.render_text import render_text,render_text_center
from ui import draw_bg, draw_gauge
from core.gamemanager import GameManager  
from core.gamestate import GameState
from core.save_load import load_game,delete_save
from scenes.play_scene import run_play_logic
from config import SCREEN_WIDTH,SCREEN_HEIGHT,FPS,WHITE,BLACK,RED,GREEN
from asset_loader import load_images,load_sounds,load_bgm,load_font
from core.stage_controller import StageController
from core.spawn_enemy import spawn_enemy

#---定数とパス管理の設定---
BASE = os.path.dirname(__file__)
def path(*p): return os.path.join(BASE, *p)

#---全体処理---
def main():
    pygame.init()
    pygame.mixer.init()
    pygame.freetype.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("おそしゅー")
    IMG = load_images()
    SE = load_sounds()
    BGM = load_bgm()
    font = load_font()
    clock = pygame.time.Clock()
    gm=GameManager()
    
    current_bgm = None
    
    def play_bgm(bgm_key):
        nonlocal current_bgm
        if current_bgm != bgm_key:
            pygame.mixer.music.load(BGM[bgm_key])
            pygame.mixer.music.play(-1)
            current_bgm = bgm_key
    
    #上下2分割背景
    bg_top = pygame.transform.scale(IMG["bg_top"], (SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    bg_bot = pygame.transform.scale(IMG["bg_bot"], (SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    
    #背景描画
    def draw_background(screen,gm,bg_top,bg_bot):
        if gm.state == GameState.PLAY:
            screen.blit(bg_top,(0,0))
            screen.blit(bg_bot,(0,SCREEN_HEIGHT // 2))
            if gm.active_laser:
                gm.active_laser.update(dt)
                gm.active_laser.draw(screen)
            if gm.laser_unlocked:
                draw_gauge.draw_gauge(screen,gm.score,max_gauge=100)
        else:
            screen.fill(BLACK)
    
    
    #---スプライト/ゲーム状態の初期化---
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    mizuaka_bullets_group = pygame.sprite.Group()
    slow_bullets_group =pygame.sprite.Group()
    boss_bullets_group = pygame.sprite.Group()
    fragment_group = pygame.sprite.Group()
    
    fragment_img = pygame.image.load("assets/image/fragment.png").convert_alpha()
    #初期状態を整える
    from core.save_load import load_game
    gm = GameManager()
    gm.font = font
    data = load_game()
    loaded = False
    if data:
        loaded = gm.load_from_file()
        gm.state = GameState.START
    
    if gm.state == GameState.START:
        play_bgm("start")
        
    #---初期化関数の定義---
    def full_reset():
        all_sprites.empty(); enemies.empty(); explosions.empty(); bullets.empty()
        player = Player(IMG["player"]); all_sprites.add(player)
        gm.reset(gm=gm,all_sprites=all_sprites,enemies_group=enemies,spawn_enemy_func=(
            lambda e,x,y,s=None,x_speed_factor=None,enemy_data=None:
                spawn_enemy(e,x,y,IMG,all_sprites,enemies,gm,
                            fragment_group,fragment_image,
                            extra_groups={
                                "slow_bullets":slow_bullets_group,
                                "mizuaka_bullets":mizuaka_bullets_group,
                            },
                            player=player,
                            speed=s,
                            x_speed_factor=x_speed_factor,
                            enemy_data=enemy_data,
                            bullet_group=boss_bullets_group)
            ),
            fragment_image=fragment_image,
            fragment_group=fragment_group
        )
        gm.player=player
        return player

    def resume_from_save():
        all_sprites.empty(); enemies.empty(); explosions.empty(); bullets.empty()
        player = Player(IMG["player"]); all_sprites.add(player)
        return player

    #---自機作成---
    player = Player(IMG["player"])
    all_sprites.add(player)
    scroll = 0
    is_shooting = False
    last_shot_time = 0
    gm.player = player
    
    #各変数初期化
    fragment_image = IMG["fragment"]
    gm.stage_controller = StageController(
        gm,all_sprites,enemies,
        lambda e, x, y,s=None,x_speed_factor=None,enemy_data=None: spawn_enemy(
            e,x,y,IMG,all_sprites,enemies,gm,fragment_group,fragment_image,
            extra_groups={
                "slow_bullets":slow_bullets_group,
                "mizuaka_bullets":mizuaka_bullets_group,
            },
            player=player,
            speed=s,
            x_speed_factor=x_speed_factor,
            enemy_data=enemy_data,
            bullet_group=boss_bullets_group
        )
    )
    #---メインループ開始---
    running = True
    while running:
        dt = clock.tick(60)
        now = pygame.time.get_ticks()
        
        gm.update_bullet_cooldown(now)
        gm.update_laser_gauge(dt)
        fragment_group.update()
        fragment_group.draw(screen)
        #---ユーザー入力反応---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_n and gm.state == GameState.START:
                    delete_save()
                    loaded = False
                    player = full_reset()
                    gm.state = GameState.START
                    play_bgm("start")
                                     
                elif e.key == pygame.K_RETURN:
                    if gm.state == GameState.START:
                        gm.state = GameState.INSTR
                        play_bgm("start")
                    elif gm.state in [GameState.INSTR,GameState.CLEAR,GameState.GAMEOVER]:
                        if not loaded:
                            player = full_reset()
                        else:
                            player = resume_from_save()
                            loaded = False
                        gm.state = GameState.PLAY
                        play_bgm("play")

                #---1~4key(弾種変更)---
                elif e.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        gm.bullet_type = int(e.key - pygame.K_0)
                    
                #---Esc-key(セーブ＆終了)---
                elif e.key == pygame.K_ESCAPE and gm.state == GameState.PLAY:
                    gm.save_to_file()
                    running = False

            #---マウス操作(弾/レーザー)---
            elif e.type == pygame.MOUSEBUTTONDOWN and gm.state == GameState.PLAY:
                if e.button == 1:
                    is_shooting = True
                elif e.button == 3 and gm.can_use_laser:
                    laser = Laser(player,pygame.mouse.get_pos())
                    gm.active_laser = laser
                    gm.activate_laser()
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                is_shooting = False
                 
        draw_background(screen,gm,bg_top,bg_bot)
        if gm.active_laser:
            gm.active_laser.draw(screen)
            
        #---タイトル画面---
        if gm.state == GameState.START:
            render_text_center(screen, font, "おそしゅー！", (SCREEN_WIDTH//2,200))
            if loaded:
                render_text_center(screen, font, "続きから再開：Enterキー", (SCREEN_WIDTH//2,250))
                render_text_center(screen, font, "中断データ削除：Nキー", (SCREEN_WIDTH//2,300))
            else:
                render_text_center(screen, font, "Enterキーで開始", (SCREEN_WIDTH//2,250))
        #---タイトル画面２(操作説明)---
        elif gm.state == GameState.INSTR:
            for i, line in enumerate(["方向キーで移動", "敵本体に当たってもライフ減少", "左クリック長押しで連射", "Enterキーでゲーム開始"]):
                render_text_center(screen, font, line, (SCREEN_WIDTH//2, 250+i*50))
                
        elif gm.state == GameState.PLAY:
            scroll, last_shot_time = run_play_logic(
            dt,screen, gm, player, all_sprites, enemies, bullets, explosions,
            IMG, SE, now,  scroll, is_shooting, last_shot_time,slow_bullets_group,mizuaka_bullets_group,boss_bullets_group
            )
            
            gm.stage_controller.update(gm.elapsed_time)

        #---結果画面(CLEAR/GAMEOVER)
        elif gm.state in [GameState.CLEAR, GameState.GAMEOVER]:
            txt = "クリア！" if gm.state == GameState.CLEAR else "ゲームオーバー"
            render_text(screen, font, txt, (480, 200))
            render_text(screen, font, f"スコア: {gm.score}", (500, 300))
            if gm.state == GameState.GAMEOVER:
                m, s = gm.elapsed_time // 60000, (gm.elapsed_time % 60000) // 1000
                render_text(screen, font, f"時間: {m:02d}:{s:02d}", (500, 360))
            render_text(screen, font, "Enterキーでステージ最初から", (400, 450))
            
        #---画面の更新---
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()