if __name__ == "__main__":
    print("このファイルは直接実行しないで下さい。main.pyを起点にしてください。")
    exit()

import pygame
from entities.enemies import MizuakaRotationSpawner,MizuakaCircleTrap

class StageController:
    def __init__(self, gm, all_sprites, enemies_group, spawn_enemy_func,fragment_image=None,fragment_group=None):
        self.gm = gm
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.spawn_enemy_func = spawn_enemy_func
        self.fragment_image = fragment_image
        self.fragment_group = fragment_group
        self.controllers = []
        #画面サイズ(x:1200,y:700)
        #Mizuaka/Shooter/ZigZag/ZigZagInverted/RightMover/Formation/UpLeftMover/DownLeftMover
        #Abura/Slow/Shield/Formation/AburaBounce
        #Sabi/Plus/Orbit/Bind/Formation/Charger/ChargerInversed
        #Kabi/Formation/DownMover
        self.schedule = [
            {"time": 1000, "enemy_type": "MizuakaFormation", "x": 1200,"y": 100},
            {"time": 4000, "enemy_type": "Mizuaka", "x": 1200,"y": 150,"speed":4},
            {"time": 4000, "enemy_type": "Mizuaka", "x": 1200,"y": 330,"speed":5},
            {"time": 4000, "enemy_type": "Mizuaka", "x": 1200,"y": 500,"speed":4},
            {"time": 10000, "enemy_type": "AburaFormation", "x": 1200,"y": 100},
            {"time": 13000, "enemy_type": "Abura", "x": 1200,"y": 150,"speed":4},
            {"time": 13000, "enemy_type": "Abura", "x": 1200,"y": 330,"speed":5},
            {"time": 13000, "enemy_type": "Abura", "x": 1200,"y": 500,"speed":4},
            {"time": 19000, "enemy_type": "SabiFormation", "x": 1200,"y": 450},
            {"time": 20000, "enemy_type": "Sabi", "x": 1200,"y": 350,"speed":3},
            {"time": 28000, "enemy_type": "KabiFormation", "x": 1200,"y": 350},
            {"time": 31000, "enemy_type": "Kabi", "x": 1200,"y": 150,"speed":4},
            {"time": 31000, "enemy_type": "Kabi", "x": 1200,"y": 330,"speed":5},
            {"time": 31000, "enemy_type": "Kabi", "x": 1200,"y": 500,"speed":4},
            # #エリアA 基準38000
            {"time": 38000, "enemy_type": "AburaSlow", "x": 1200,"y": 50, "speed": 3},
            {"time": 38000, "enemy_type": "AburaSlow", "x": 1200,"y": 615, "speed": 3},
            {"time": 40000, "enemy_type": "AburaSlow", "x": 1200,"y": 50, "speed": 3},
            {"time": 40000, "enemy_type": "AburaSlow", "x": 1200,"y": 615, "speed": 3},
            {"time": 40000, "enemy_type": "MizuakaZigZagInversed", "x": 1200,"y": 200, "speed": 5},
            {"time": 40200, "enemy_type": "MizuakaZigZagInversed", "x": 1200,"y": 200, "speed": 5},
            {"time": 40400, "enemy_type": "MizuakaZigZagInversed", "x": 1200,"y": 200, "speed": 5},
            {"time": 40000, "enemy_type": "MizuakaZigZag", "x": 1200,"y": 500, "speed": 5},
            {"time": 40200, "enemy_type": "MizuakaZigZag", "x": 1200,"y": 500, "speed": 5},
            {"time": 40400, "enemy_type": "MizuakaZigZag", "x": 1200,"y": 500, "speed": 5},
            
            # #エリアB 基準45000
            {"time": 44999, "enemy_type": "MizuakaShooter", "x": 1200,"y": 100, "speed": 5},
            {"time": 45000, "enemy_type": "MizuakaShooter", "x": 1200,"y": 600, "speed": 5},
            
            {"time": 46000, "enemy_type": "MizuakaUpLeftMover", "x":1200 ,"y": 800, "speed": 6,"x_speed_factor":0.4},
            {"time": 46200, "enemy_type": "MizuakaUpLeftMover", "x":1200 ,"y": 800, "speed": 6,"x_speed_factor":0.4},
            {"time": 46400, "enemy_type": "MizuakaUpLeftMover", "x":1200 ,"y": 800, "speed": 6,"x_speed_factor":0.4},
            {"time": 46600, "enemy_type": "MizuakaUpLeftMover", "x":1200 ,"y": 800, "speed": 6,"x_speed_factor":0.4},
            {"time": 46800, "enemy_type": "MizuakaUpLeftMover", "x":1200 ,"y": 800, "speed": 6,"x_speed_factor":0.4},
            
            # #2200
            {"time": 49000, "enemy_type": "MizuakaRightMover", "x": -100,"y": 100},
            {"time": 49001, "enemy_type": "MizuakaRightMover", "x": -100,"y": 600},
            {"time": 49500, "enemy_type": "MizuakaDownLeftMover", "x":950 ,"y": -100, "speed": 8,"x_speed_factor":0.4},
            {"time": 49700, "enemy_type": "MizuakaDownLeftMover", "x":950 ,"y": -100, "speed": 8,"x_speed_factor":0.4},
            {"time": 49900, "enemy_type": "MizuakaDownLeftMover", "x":950 ,"y": -100, "speed": 8,"x_speed_factor":0.4},
            {"time": 50100, "enemy_type": "MizuakaDownLeftMover", "x":950 ,"y": -100, "speed": 8,"x_speed_factor":0.4},
            {"time": 50300, "enemy_type": "MizuakaDownLeftMover", "x":950 ,"y": -100, "speed": 8,"x_speed_factor":0.4},
            {"time": 49000, "enemy_type": "MizuakaShooter", "x": 1200,"y": 200, "speed": 5},
            {"time": 49000, "enemy_type": "MizuakaShooter", "x": 1200,"y": 400, "speed": 5},
            # #2200
            {"time": 52500, "enemy_type": "MizuakaRightMover", "x": -100,"y": 200},
            {"time": 52500, "enemy_type": "MizuakaRightMover", "x": -100,"y": 500},
            {"time": 53000, "enemy_type": "MizuakaUpLeftMover", "x":700 ,"y": 800, "speed": 10,"x_speed_factor":0.3},
            {"time": 53200, "enemy_type": "MizuakaUpLeftMover", "x":700 ,"y": 800, "speed": 10,"x_speed_factor":0.3},
            {"time": 53400, "enemy_type": "MizuakaUpLeftMover", "x":700 ,"y": 800, "speed": 10,"x_speed_factor":0.3},
            {"time": 53600, "enemy_type": "MizuakaUpLeftMover", "x":700 ,"y": 800, "speed": 10,"x_speed_factor":0.3},
            {"time": 53800, "enemy_type": "MizuakaUpLeftMover", "x":700 ,"y": 800, "speed": 10,"x_speed_factor":0.3},

            # #700
            {"time": 545500, "enemy_type": "MizuakaDownLeftMover", "x":450 ,"y": -100, "speed": 12,"x_speed_factor":0.3},
            {"time": 54700, "enemy_type": "MizuakaDownLeftMover", "x":450 ,"y": -100, "speed": 12,"x_speed_factor":0.3},
            {"time": 54900, "enemy_type": "MizuakaDownLeftMover", "x":450 ,"y": -100, "speed": 12,"x_speed_factor":0.3},
            {"time": 55100, "enemy_type": "MizuakaDownLeftMover", "x":450 ,"y": -100, "speed": 12,"x_speed_factor":0.3},
            {"time": 55300, "enemy_type": "MizuakaDownLeftMover", "x":450 ,"y": -100, "speed": 12,"x_speed_factor":0.3},
            # #400
            {"time": 55700, "enemy_type": "MizuakaRightMover", "x": -100,"y": 300},
            {"time": 55700, "enemy_type": "MizuakaRightMover", "x": -100,"y": 400},
            {"time": 56200, "enemy_type": "MizuakaUpLeftMover", "x":350 ,"y": 800, "speed": 14,"x_speed_factor":0.2},
            {"time": 56400, "enemy_type": "MizuakaUpLeftMover", "x":350 ,"y": 800, "speed": 14,"x_speed_factor":0.2},
            {"time": 56600, "enemy_type": "MizuakaUpLeftMover", "x":350 ,"y": 800, "speed": 14,"x_speed_factor":0.2},
            {"time": 56800, "enemy_type": "MizuakaUpLeftMover", "x":350 ,"y": 800, "speed": 14,"x_speed_factor":0.2},
            {"time": 57000, "enemy_type": "MizuakaUpLeftMover", "x":350 ,"y": 800, "speed": 14,"x_speed_factor":0.2},
            # #400
            {"time": 57400, "enemy_type": "MizuakaDownLeftMover", "x":250 ,"y": -100, "speed": 16,"x_speed_factor":0.2},
            {"time": 57600, "enemy_type": "MizuakaDownLeftMover", "x":250 ,"y": -100, "speed": 16,"x_speed_factor":0.2},
            {"time": 57800, "enemy_type": "MizuakaDownLeftMover", "x":250 ,"y": -100, "speed": 16,"x_speed_factor":0.2},
            {"time": 58000, "enemy_type": "MizuakaDownLeftMover", "x":250 ,"y": -100, "speed": 16,"x_speed_factor":0.2},
            {"time": 58200, "enemy_type": "MizuakaDownLeftMover", "x":250 ,"y": -100, "speed": 16,"x_speed_factor":0.2},
            # #300
            {"time": 58500, "enemy_type": "MizuakaUpLeftMover", "x":200 ,"y": 800, "speed": 18,"x_speed_factor":0.2},
            {"time": 58700, "enemy_type": "MizuakaUpLeftMover", "x":200 ,"y": 800, "speed": 18,"x_speed_factor":0.2},
            {"time": 58900, "enemy_type": "MizuakaUpLeftMover", "x":200 ,"y": 800, "speed": 18,"x_speed_factor":0.2},
            {"time": 59100, "enemy_type": "MizuakaUpLeftMover", "x":200 ,"y": 800, "speed": 18,"x_speed_factor":0.2},
            {"time": 59300, "enemy_type": "MizuakaUpLeftMover", "x":200 ,"y": 800, "speed": 18,"x_speed_factor":0.2},
            
            {"time": 61000, "enemy_type": "KabiDownMover", "x": 650,"y": -100, "speed": 5},
            {"time": 61200, "enemy_type": "KabiDownMover", "x": 730,"y": -100, "speed": 5},
            {"time": 61400, "enemy_type": "KabiDownMover", "x": 810,"y": -100, "speed": 5},
            {"time": 61600, "enemy_type": "KabiDownMover", "x": 890,"y": -100, "speed": 5},
            {"time": 61400, "enemy_type": "KabiDownMover", "x": 970,"y": -100, "speed": 5},
            {"time": 61200, "enemy_type": "KabiDownMover", "x": 1050,"y": -100, "speed": 5},
            {"time": 61000, "enemy_type": "KabiDownMover", "x": 1130,"y": -100, "speed": 5},
            
            #エリアC 基準64000
            {"time": 64000, "enemy_type": "KabiDownMover", "x": 50,"y": -100, "speed": 5},
            {"time": 64300, "enemy_type": "KabiDownMover", "x": 270,"y": -100, "speed": 5},            
            {"time": 64600, "enemy_type": "KabiDownMover", "x": 490,"y": -100, "speed": 5},            
            {"time": 64900, "enemy_type": "KabiDownMover", "x": 710,"y": -100, "speed": 5},            
            {"time": 65200, "enemy_type": "KabiDownMover", "x": 930,"y": -100, "speed": 5}, 
            {"time": 65500, "enemy_type": "KabiDownMover", "x": 1150,"y": -100, "speed": 5}, 
            
            {"time": 65200, "enemy_type": "KabiUpMover", "x": 1040,"y": 810, "speed": 4}, 
            {"time": 65500, "enemy_type": "KabiUpMover", "x": 820,"y": 810, "speed": 4}, 
            {"time": 65800, "enemy_type": "KabiUpMover", "x": 600,"y": 810, "speed": 4}, 
            {"time": 66100, "enemy_type": "KabiUpMover", "x": 380,"y": 810, "speed": 4}, 
            {"time": 66400, "enemy_type": "KabiUpMover", "x": 160,"y": 810, "speed": 4}, 
            
            {"time": 66100, "enemy_type": "KabiDownMover", "x": 1150,"y": -100, "speed": 5},
            {"time": 66400, "enemy_type": "KabiDownMover", "x": 930,"y": -100, "speed": 5},            
            {"time": 66700, "enemy_type": "KabiDownMover", "x": 710,"y": -100, "speed": 5},            
            {"time": 67000, "enemy_type": "KabiDownMover", "x": 490,"y": -100, "speed": 5},            
            {"time": 67300, "enemy_type": "KabiDownMover", "x": 270,"y": -100, "speed": 5}, 
            {"time": 67600, "enemy_type": "KabiDownMover", "x": 50,"y": -100, "speed": 5}, 
            #1700
            {"time": 69300, "enemy_type": "Sabi", "x": 1200,"y": 50, "speed": 5}, 
            {"time": 69600, "enemy_type": "Sabi", "x": 1200,"y": 190, "speed": 5},
            {"time": 69900, "enemy_type": "Sabi", "x": 1200,"y": 330, "speed": 5},
            {"time": 70200, "enemy_type": "Sabi", "x": 1200,"y": 470, "speed": 5},
            {"time": 70500, "enemy_type": "Sabi", "x": 1200,"y": 610, "speed": 5},
            #2800
            {"time": 73300, "enemy_type": "SabiInversed", "x": -100,"y": 50, "speed": 5}, 
            {"time": 73600, "enemy_type": "SabiInversed", "x": -100,"y": 190, "speed": 5},
            {"time": 73900, "enemy_type": "SabiInversed", "x": -100,"y": 330, "speed": 5},
            {"time": 74200, "enemy_type": "SabiInversed", "x": -100,"y": 470, "speed": 5},
            {"time": 74500, "enemy_type": "SabiInversed", "x": -100,"y": 610, "speed": 5}, 
            #1600
            {"time": 76100, "enemy_type": "KabiUpMover", "x": 1100,"y": 810, "speed": 8},
            {"time": 76100, "enemy_type": "KabiDownMover", "x": 1100,"y": -100, "speed": 8},
            {"time": 76400, "enemy_type": "KabiUpMover", "x": 990,"y": 810, "speed": 8},
            {"time": 76400, "enemy_type": "KabiDownMover", "x": 990,"y": -100, "speed": 8},
            {"time": 76700, "enemy_type": "KabiUpMover", "x": 880,"y": 810, "speed": 8},
            {"time": 76700, "enemy_type": "KabiDownMover", "x": 880,"y": -100, "speed": 8},
            {"time": 77000, "enemy_type": "KabiUpMover", "x": 770,"y": 810, "speed": 9},
            {"time": 77000, "enemy_type": "KabiDownMover", "x": 770,"y": -100, "speed": 9},
            {"time": 77300, "enemy_type": "KabiUpMover", "x": 660,"y": 810, "speed": 9},
            {"time": 77300, "enemy_type": "KabiDownMover", "x": 660,"y": -100, "speed": 9},
            {"time": 77600, "enemy_type": "KabiUpMover", "x": 490,"y": 810, "speed": 9},
            {"time": 77600, "enemy_type": "KabiDownMover", "x": 490,"y": -100, "speed": 10},
            {"time": 77900, "enemy_type": "KabiUpMover", "x": 380,"y": 810, "speed": 10},
            {"time": 77900, "enemy_type": "KabiDownMover", "x": 380,"y": -100, "speed": 10},
            {"time": 78200, "enemy_type": "KabiUpMover", "x": 270,"y": 810, "speed": 10},
            {"time": 78200, "enemy_type": "KabiDownMover", "x": 270,"y": -100, "speed": 10},
            {"time": 78500, "enemy_type": "KabiUpMover", "x": 160,"y": 810, "speed": 10},
            {"time": 78500, "enemy_type": "KabiDownMover", "x": 160,"y": -100, "speed": 10},          
            #1600 next
            {"time": 80100, "enemy_type": "SabiCharger", "x": 1200,"y": 50, "speed": 5}, 
            {"time": 80400, "enemy_type": "SabiCharger", "x": 1200,"y": 330, "speed": 5}, 
            {"time": 80700, "enemy_type": "SabiCharger", "x": 1200,"y": 610, "speed": 5}, 
            
            {"time": 83700, "enemy_type": "SabiChargerInversed", "x": -10,"y": 50, "speed": 5},
            {"time": 84000, "enemy_type": "SabiChargerInversed", "x": -10,"y": 190, "speed": 5},
            {"time": 84300, "enemy_type": "SabiChargerInversed", "x": -10,"y": 330, "speed": 5},
            {"time": 84600, "enemy_type": "SabiChargerInversed", "x": -10,"y": 470, "speed": 5},
            {"time": 84900, "enemy_type": "SabiChargerInversed", "x": -10,"y": 610, "speed": 5},
            
            
            {"time": 87000, "enemy_type": "AburaUp", "x": 930,"y": 810,"speed":4.3},
            {"time": 87000, "enemy_type": "AburaRight", "x": -100,"y": 150,"speed":6},
            
            {"time": 91000, "enemy_type": "AburaRight", "x": -100,"y": 70,"speed":11},
            {"time": 91000, "enemy_type": "AburaRight", "x": -100,"y": 310,"speed":11},
            {"time": 91000, "enemy_type": "AburaRight", "x": -100,"y": 390,"speed":11},
            {"time": 91000, "enemy_type": "AburaRight", "x": -100,"y": 470,"speed":11},
            {"time": 91000, "enemy_type": "AburaRight", "x": -100,"y": 550,"speed":11},
            {"time": 91000, "enemy_type": "AburaRight", "x": -100,"y": 630,"speed":11},
            {"time": 91000, "enemy_type": "AburaRight", "x": -100,"y": 710,"speed":11},
            {"time": 91000, "enemy_type": "AburaRight", "x": -100,"y": 790,"speed":11},
            
            {"time": 91000, "enemy_type": "AburaUp", "x": 1170,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 1090,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 850,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 770,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 690,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 610,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 530,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 450,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 370,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 290,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 210,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 130,"y": 810,"speed":9},
            {"time": 91000, "enemy_type": "AburaUp", "x": 50,"y": 810,"speed":9},
            {"time": 94000, "enemy_type": "Abura", "x": 1250,"y": 610,"speed":11},
            {"time": 94000, "enemy_type": "AburaDown", "x": 210,"y": -10,"speed":7.5},
            
            {"time": 96000, "enemy_type": "Abura", "x": 1250,"y": 70,"speed":12},
            {"time": 96000, "enemy_type": "Abura", "x": 1250,"y": 150,"speed":12},
            {"time": 96000, "enemy_type": "Abura", "x": 1250,"y": 230,"speed":12},
            {"time": 96000, "enemy_type": "Abura", "x": 1250,"y": 310,"speed":12},
            {"time": 96000, "enemy_type": "Abura", "x": 1250,"y": 390,"speed":12},
            {"time": 96000, "enemy_type": "Abura", "x": 1250,"y": 470,"speed":12},
            {"time": 96000, "enemy_type": "Abura", "x": 1250,"y": 550,"speed":12},
            {"time": 96000, "enemy_type": "Abura", "x": 1250,"y": 710,"speed":12},
            {"time": 96000, "enemy_type": "Abura", "x": 1250,"y": 790,"speed":12},
            
            {"time": 96000, "enemy_type": "AburaDown", "x": 50,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 130,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 290,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 370,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 450,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 530,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 610,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 690,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 770,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 850,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 930,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 1010,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 1090,"y": -10,"speed":10},
            {"time": 96000, "enemy_type": "AburaDown", "x": 1170,"y": -10,"speed":10},
            
            {"time": 98000, "enemy_type": "AburaUp", "x": 930,"y": 810,"speed":11},
            {"time": 98000, "enemy_type": "AburaRight", "x": -100,"y": 150,"speed":14},
            
            {"time": 99000, "enemy_type": "AburaRight", "x": -100,"y": 70,"speed":14},
            {"time": 99000, "enemy_type": "AburaRight", "x": -100,"y": 310,"speed":14},
            {"time": 99000, "enemy_type": "AburaRight", "x": -100,"y": 390,"speed":14},
            {"time": 99000, "enemy_type": "AburaRight", "x": -100,"y": 470,"speed":14},
            {"time": 99000, "enemy_type": "AburaRight", "x": -100,"y": 550,"speed":14},
            {"time": 99000, "enemy_type": "AburaRight", "x": -100,"y": 630,"speed":14},
            {"time": 99000, "enemy_type": "AburaRight", "x": -100,"y": 710,"speed":14},
            {"time": 99000, "enemy_type": "AburaRight", "x": -100,"y": 790,"speed":14},
            #1500
            {"time": 100000, "enemy_type": "AburaDown", "x": 50,"y": -10,"speed":10},
            {"time": 100200, "enemy_type": "AburaDown", "x": 130,"y": -10,"speed":10},
            {"time": 100400, "enemy_type": "AburaDown", "x": 210,"y": -10,"speed":10},
            {"time": 100600, "enemy_type": "AburaDown", "x": 290,"y": -10,"speed":10},
            {"time": 100800, "enemy_type": "AburaDown", "x": 370,"y": -10,"speed":10},
            {"time": 101000, "enemy_type": "AburaDown", "x": 450,"y": -10,"speed":10},
            {"time": 101200, "enemy_type": "AburaDown", "x": 530,"y": -10,"speed":10},
            {"time": 101400, "enemy_type": "AburaDown", "x": 610,"y": -10,"speed":10},
            {"time": 101200, "enemy_type": "AburaDown", "x": 690,"y": -10,"speed":10},
            {"time": 101000, "enemy_type": "AburaDown", "x": 770,"y": -10,"speed":10},
            {"time": 100800, "enemy_type": "AburaDown", "x": 850,"y": -10,"speed":10},
            {"time": 100400, "enemy_type": "AburaDown", "x": 1010,"y": -10,"speed":10},
            {"time": 100200, "enemy_type": "AburaDown", "x": 1090,"y": -10,"speed":10},
            {"time": 100000, "enemy_type": "AburaDown", "x": 1170,"y": -10,"speed":10},
            #3000
            {"time": 103000, "enemy_type": "AburaCurveCharger", "x": 1010,"y": -10},
            {"time": 103000, "enemy_type": "AburaCurveCharger", "x": 130,"y": -10},
            
            #2000
            {"time": 105000, "enemy_type": "AburaStopShooter", "x": 1010,"y": -10,"speed":8},
            {"time": 105000, "enemy_type": "AburaStopShooter", "x": 130,"y": -10,"speed":8},
            #2000
            {"time": 107000, "enemy_type": "AburaCurveCharger", "x": 210,"y": -10},
            {"time": 107000, "enemy_type": "AburaCurveCharger", "x": 130,"y": -10},
            {"time": 107000, "enemy_type": "AburaCurveCharger", "x": 50,"y": -10},
            {"time": 107000, "enemy_type": "AburaCurveCharger", "x": 1010,"y": -10},
            {"time": 107000, "enemy_type": "AburaCurveCharger", "x": 1090,"y": -10},
            {"time": 107000, "enemy_type": "AburaCurveCharger", "x": 930,"y": -10},
            #2000
            {"time": 109000, "enemy_type": "AburaStopShooter", "x": 1010,"y": -10,"speed":8},
            {"time": 109000, "enemy_type": "AburaStopShooter", "x": 130,"y": -10,"speed":8},
            #1000
            {"time": 110000, "enemy_type": "AburaCurveCharger", "x": 1010,"y": -10},
            {"time": 110000, "enemy_type": "AburaCurveCharger", "x": 930,"y": -10},
            {"time": 110000, "enemy_type": "AburaCurveCharger", "x": 850,"y": -10},
            {"time": 110000, "enemy_type": "AburaCurveCharger", "x": 770,"y": -10},
            {"time": 110000, "enemy_type": "AburaCurveCharger", "x": 690,"y": -10},
            #2000
            {"time": 112000, "enemy_type": "AburaCurveCharger", "x": 530,"y": -10},
            {"time": 112000, "enemy_type": "AburaCurveCharger", "x": 450,"y": -10},
            {"time": 112000, "enemy_type": "AburaCurveCharger", "x": 370,"y": -10},
            {"time": 112000, "enemy_type": "AburaCurveCharger", "x": 290,"y": -10},
            {"time": 112000, "enemy_type": "AburaCurveCharger", "x": 210,"y": -10},
            #3500
            {"time": 115500, "enemy_type": "AburaDown", "x": 50,"y": -10,"speed":10},
            {"time": 115700, "enemy_type": "AburaDown", "x": 130,"y": -10,"speed":10},
            {"time": 115900, "enemy_type": "AburaDown", "x": 210,"y": -10,"speed":10},
            {"time": 116100, "enemy_type": "AburaDown", "x": 290,"y": -10,"speed":10},
            {"time": 116300, "enemy_type": "AburaDown", "x": 370,"y": -10,"speed":10},
            {"time": 116500, "enemy_type": "AburaDown", "x": 450,"y": -10,"speed":10},
            {"time": 116500, "enemy_type": "AburaDown", "x": 770,"y": -10,"speed":10},
            {"time": 116300, "enemy_type": "AburaDown", "x": 850,"y": -10,"speed":10},
            {"time": 116100, "enemy_type": "AburaDown", "x": 930,"y": -10,"speed":10},
            {"time": 115900, "enemy_type": "AburaDown", "x": 1010,"y": -10,"speed":10},
            {"time": 115700, "enemy_type": "AburaDown", "x": 1090,"y": -10,"speed":10},
            {"time": 115500, "enemy_type": "AburaDown", "x": 1170,"y": -10,"speed":10},
            #3500
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 50,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 130,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 210,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 290,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 370,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 450,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 770,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 850,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 930,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 1010,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 1090,"y": -10},
            {"time": 119000, "enemy_type": "AburaCurveCharger", "x": 1170,"y": -10},
            
            {"time": 121000, "enemy_type": "KabiRight", "x": -50,"y": 130,"speed":3},
            {"time": 121600, "enemy_type": "KabiRight", "x": -50,"y": 130,"speed":3},
            {"time": 121300, "enemy_type": "KabiRight", "x": -50,"y": 50,"speed":3},
            {"time": 121300, "enemy_type": "KabiRight", "x": -50,"y": 210,"speed":3},
            
            {"time": 123000, "enemy_type": "KabiRight", "x": -50,"y": 530,"speed":3},
            {"time": 123600, "enemy_type": "KabiRight", "x": -50,"y": 530,"speed":3},
            {"time": 123300, "enemy_type": "KabiRight", "x": -50,"y": 450,"speed":3},
            {"time": 123300, "enemy_type": "KabiRight", "x": -50,"y": 610,"speed":3},
            
            {"time": 125000, "enemy_type": "KabiRight", "x": -50,"y": 130,"speed":3},
            {"time": 125600, "enemy_type": "KabiRight", "x": -50,"y": 130,"speed":3},
            {"time": 125300, "enemy_type": "KabiRight", "x": -50,"y": 50,"speed":3},
            {"time": 125300, "enemy_type": "KabiRight", "x": -50,"y": 210,"speed":3},
            
            {"time": 127000, "enemy_type": "KabiRight", "x": -50,"y": 530,"speed":3},
            {"time": 127600, "enemy_type": "KabiRight", "x": -50,"y": 530,"speed":3},
            {"time": 127300, "enemy_type": "KabiRight", "x": -50,"y": 450,"speed":3},
            {"time": 127400, "enemy_type": "KabiRight", "x": -50,"y": 610,"speed":3},
  
            {"time": 127500, "enemy_type": "SabiInversed", "x": -50,"y": 130,"speed":3},
            {"time": 127500, "enemy_type": "SabiInversed", "x": -50,"y": 210,"speed":3},
            {"time": 127500, "enemy_type": "SabiInversed", "x": -50,"y": 290,"speed":3},
            {"time": 128900, "enemy_type": "KabiRight", "x": -50,"y": 530,"speed":3},
            {"time": 129500, "enemy_type": "KabiRight", "x": -50,"y": 530,"speed":3},
            {"time": 129200, "enemy_type": "KabiRight", "x": -50,"y": 450,"speed":3},
            {"time": 129200, "enemy_type": "KabiRight", "x": -50,"y": 610,"speed":3},            

            {"time": 130900, "enemy_type": "KabiRight", "x": -50,"y": 130,"speed":3},
            {"time": 131500, "enemy_type": "KabiRight", "x": -50,"y": 130,"speed":3},
            {"time": 131200, "enemy_type": "KabiRight", "x": -50,"y":  50,"speed":3},
            {"time": 131200, "enemy_type": "KabiRight", "x": -50,"y": 210,"speed":3},

            {"time": 132900, "enemy_type": "KabiRight", "x": -50,"y": 530,"speed":3},
            {"time": 133500, "enemy_type": "KabiRight", "x": -50,"y": 530,"speed":3},
            {"time": 133200, "enemy_type": "KabiRight", "x": -50,"y": 450,"speed":3},
            {"time": 133200, "enemy_type": "KabiRight", "x": -50,"y": 610,"speed":3}, 

            {"time": 134000, "enemy_type": "SabiOrbit", "x": -50,"y": 210,"speed":3}, 
            {"time": 135200, "enemy_type": "KabiRight", "x": -50,"y": 130,"speed":3},
            {"time": 135800, "enemy_type": "KabiRight", "x": -50,"y": 130,"speed":3},
            {"time": 135500, "enemy_type": "KabiRight", "x": -50,"y":  50,"speed":3},
            {"time": 135500, "enemy_type": "KabiRight", "x": -50,"y": 210,"speed":3},
            {"time": 135500, "enemy_type": "SabiOrbit", "x": -50,"y": 450,"speed":3}, 
            
            

            {"time": 138500, "enemy_type": "KabiDownMover", "x": 600,"y": -100,"speed":6}, 
            {"time": 139300, "enemy_type": "KabiDownMover", "x": 600,"y": -100,"speed":6}, 
            {"time": 140100, "enemy_type": "KabiDownMover", "x": 600,"y": -100,"speed":6}, 
            {"time": 140900, "enemy_type": "KabiDownMover", "x": 600,"y": -100,"speed":6}, 
            {"time": 141700, "enemy_type": "KabiDownMover", "x": 600,"y": -100,"speed":6}, 
            {"time": 142500, "enemy_type": "KabiDownMover", "x": 600,"y": -100,"speed":6}, 
            {"time": 143300, "enemy_type": "KabiDownMover", "x": 600,"y": -100,"speed":6}, 
            {"time": 144100, "enemy_type": "KabiDownMover", "x": 600,"y": -100,"speed":6}, 
            {"time": 144900, "enemy_type": "KabiDownMover", "x": 600,"y": -100,"speed":6}, 
            
            {"time": 146500, "enemy_type": "KabiRight", "x": -100,"y": 320,"speed":6}, 
            {"time": 147300, "enemy_type": "KabiRight", "x": -100,"y": 320,"speed":6}, 
            {"time": 148100, "enemy_type": "KabiRight", "x": -100,"y": 320,"speed":6}, 
            {"time": 148900, "enemy_type": "KabiRight", "x": -100,"y": 320,"speed":6}, 
            {"time": 149700, "enemy_type": "KabiRight", "x": -100,"y": 320,"speed":6}, 
            {"time": 150500, "enemy_type": "KabiRight", "x": -100,"y": 320,"speed":6},   

            {"time": 142300, "enemy_type": "AburaCurveCharger", "x": 300,"y": -10,"speed":4}, 
            {"time": 142300, "enemy_type": "AburaCurveCharger", "x": 200,"y": -10,"speed":4}, 
            {"time": 142300, "enemy_type": "AburaCurveCharger", "x": 100,"y": -10,"speed":4}, 
            {"time": 142300, "enemy_type": "AburaCurveCharger", "x": 900,"y": -10,"speed":4}, 
            {"time": 142300, "enemy_type": "AburaCurveCharger", "x": 1000,"y": -10,"speed":4}, 
            {"time": 142300, "enemy_type": "AburaCurveCharger", "x": 1100,"y": -10,"speed":4}, 

            {"time": 147500, "enemy_type": "SabiCharger", "x": 1250,"y": 100,"speed":6}, 
            {"time": 149500, "enemy_type": "SabiCharger", "x": 1250,"y": 500,"speed":6},
            {"time": 147500, "enemy_type": "SabiChargerInversed", "x": -100,"y": 500,"speed":6}, 
            {"time": 149500, "enemy_type": "SabiChargerInversed", "x": -100,"y": 100,"speed":6}, 
            
            {"time": 151500, "enemy_type": "MizuakaCircleTrapBatch","angle_deg":120,"center_x":600,"center_y":350, "num":6,"speed":2}, 
            {"time": 154500, "enemy_type": "MizuakaCircleTrapBatch","angle_deg":120,"center_x":600,"center_y":350, "num":8,"speed":2}, 
            {"time": 157500, "enemy_type": "MizuakaCircleTrapBatch","angle_deg":120,"center_x":600,"center_y":350, "num":16,"speed":2}, 
            {"time": 160500, "enemy_type": "MizuakaCircleTrapBatch","angle_deg":120,"center_x":600,"center_y":350, "num":16,"speed":2}, 
            {"time": 163500, "enemy_type": "MizuakaCircleTrapBatch","angle_deg":120,"center_x":600,"center_y":350, "num":16,"speed":2},
            {"time": 165500, "enemy_type": "MizuakaCircleTrapBatch","angle_deg":120,"center_x":600,"center_y":350, "num":16,"speed":2},
            {"time": 170500, "enemy_type": "MizuakaCircleTrapBatch","angle_deg":120,"center_x":600,"center_y":350, "num":32,"speed":4}, 
            {"time": 176500, "enemy_type": "MizuakaRotationSpawner", "x": 600, "y": 350, "speed": 10}, 
            {"time": 190000, "enemy_type": "Boss", "x": 1200,"y": 350},
            ]
        

        self.current_index = 0
        
    def spawn_circle_trap_enemies(image_surface,all_sprites,enemies_group,center_pos,num=12,speed=4):
        angle_step = 360/num
        for i in range(num):
            angle = i*angle_step
            enemy = MizuakaCircleTrap(image_surface,angle,center_pos,speed)
            all_sprites.add(enemy)
            enemies_group.add(enemy)

    def update(self, current_time_ms):
        effective_time = current_time_ms - self.gm._resume_offset
        
        for entry in self.schedule:
            # 出現済みならスキップ
            if entry.get("spawned", False):
                continue
            
            if effective_time >= entry["time"]:
                speed = entry.get("speed",None)
                x_speed_factor = entry.get("x_speed_factor",None)
                
                if entry["enemy_type"] == "MizuakaRotationSpawner":
                    controller = MizuakaRotationSpawner(
                        image=self.gm.img["mizuaka"],
                        all_sprites=self.all_sprites,
                        enemies_group=self.enemies_group,
                        center_pos=(entry["x"], entry["y"]),
                        speed=speed if speed is not None else 4,
                        gm=self.gm,
                        fragment_image=self.gm.img["fragment"],
                        fragment_group=self.fragment_group
                    )
                    self.controllers.append(controller)

                else:
                    self.spawn_enemy_func(entry["enemy_type"], entry.get("x",0), entry.get("y",0), entry.get("speed"), entry.get("x_speed_factor"),enemy_data=entry)

                entry["spawned"] = True

    # コントローラーの更新
        for controller in self.controllers:
            controller.update()