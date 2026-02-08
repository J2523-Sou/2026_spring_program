import pygame
import sys
import math

# プレイヤー（円）
class Player:
    
    # プレイヤーコンストラクタ
    def __init__(self):
        
        player = pygame.Rect(400, 300, 50, 50)  # 初期位置
        self.player = player                    # プレイヤーの情報
        self.count_key = [0, 0, 0, 0]           # 上下左右のキー入力カウント
        self.count_time = 0                     # 時間カウント
        self.speed = 5                          # 移動速度
        self.accel_gain = 1.5                   # 当加速度運動時の加速度（加速）
        self.brake_gain = 0.4                   # 当加速度運動時の加速度（減速）
        self.move_gain = 0.1                    # 移動倍率
        self.radius = player.width // 2         # 円の半径
    
    # 描画 
    def draw(self, screen, enable_shaking = False):

        # 震えるアニメーションが有効なら
        if enable_shaking:
            self.count_time += 1
            pygame.draw.circle(screen, (0, 0, 255), self.player.center, math.sin(self.count_time * 0.1) * 7 + self.radius)
        else:
            pygame.draw.circle(screen, (0, 0, 255), self.player.center, self.radius)
    
    # マウス追従（テスト中）
    def track_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_x, player_y = self.player.center
        dx = mouse_x - player_x
        dy = mouse_y - player_y
        
        if dx < 0:
            self.count_key[1] = dx * 0.05
        elif dx > 0:
            self.count_key[0] = dx * -1 * 0.05
        if dy < 0:
            self.count_key[3] = dy * 0.05
        elif dy > 0:
            self.count_key[2] = dy * -1 * 0.05
    
    # 端でワープするよ
    def warp(self, screen_rect):
        
        if self.player.left > screen_rect.right:
            self.player.right = screen_rect.left
        elif self.player.right < screen_rect.left:
            self.player.left = screen_rect.right
        if self.player.top > screen_rect.bottom:
            self.player.bottom = screen_rect.top
        elif self.player.bottom < screen_rect.top:
            self.player.top = screen_rect.bottom
    
    # 等速直線運動
    def move_ulm(self, keys, enable_warp = True):
        
        if keys[pygame.K_LEFT]:
            self.player.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.player.x += self.speed
        if keys[pygame.K_UP]:
            self.player.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.player.y += self.speed
        
        if enable_warp: self.warp(pygame.display.get_surface().get_rect())
    
    # 等加速度運動
    def move_ice(self, keys, enable_warp = True):
        if keys[pygame.K_LEFT]:
            self.count_key[0] += self.accel_gain
        if keys[pygame.K_RIGHT]:
            self.count_key[1] += self.accel_gain
        if keys[pygame.K_UP]:
            self.count_key[2] += self.accel_gain
        if keys[pygame.K_DOWN]:
            self.count_key[3] += self.accel_gain

        if not keys[pygame.K_LEFT] and self.count_key[0] > 0:
            self.count_key[0] -= self.brake_gain
        if not keys[pygame.K_RIGHT] and self.count_key[1] > 0:
            self.count_key[1] -= self.brake_gain
        if not keys[pygame.K_UP] and self.count_key[2] > 0:
            self.count_key[2] -= self.brake_gain
        if not keys[pygame.K_DOWN] and self.count_key[3] > 0:
            self.count_key[3] -= self.brake_gain
            
        if self.count_key[0] > 0:
            self.player.x -= self.count_key[0] ** 2 * self.move_gain
        if self.count_key[1] > 0:
            self.player.x += self.count_key[1] ** 2 * self.move_gain
        if self.count_key[2] > 0:
            self.player.y -= self.count_key[2] ** 2 * self.move_gain
        if self.count_key[3] > 0:
            self.player.y += self.count_key[3] ** 2 * self.move_gain

        for i in range(4):
            if self.count_key[i] < 0:
                self.count_key[i] = 0

        if enable_warp: self.warp(pygame.display.get_surface().get_rect())
        
        
# 背景
class Background:
    
    # 背景コンストラクタ
    def __init__(self):
        
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)    # ウインドウサイズ指定
        self.font_H = pygame.font.SysFont("msgothic", 32)            # フォント設定
        self.font_P = pygame.font.SysFont("arial", 24)            # フォント設定
        self.screen = screen                                           # 背景インスタンス
        
        self.text_location_0 = self.font_H.render("0", True, (0, 0, 0))  # テキスト設定
        self.text_jamission_0 = self.font_H.render("チュートリアル", True, (0, 0, 0))  # テキスト設定
        self.text_enmission_0 = self.font_P.render("Tutorial", True, (0, 0, 0))  # テキスト設定
    
    # 背景0描画
    def draw_background_0(self):
        
        self.screen.fill((255, 255, 255))                           # 画面描画
        self.screen.blit(self.text_location_0, (50, 50))            # テキスト描画
        self.screen.blit(self.text_jamission_0, (100, 50))          # テキスト描画
        self.screen.blit(self.text_enmission_0, (400, 55))          # テキスト描画

# オブジェクトたち     
class Gameobject:
    
    # オブジェクトコンストラクタ
    def __init__(self, screen):
        
        # ウインドウの中心座標取得
        screen_rect = screen.get_rect()
        self.center_x, self.center_y = screen_rect.center
        
        # テキストのフォント
        self.font_jaobject_0 = pygame.font.SysFont("msgothic", 40)
        self.font_enobject_0 = pygame.font.SysFont("arial", 30)
        
        ##### ステージ0 #####
        
        # クリアフラグ（ステージ0）
        self.clear_up = True
        self.clear_down = True
        self.clear_left = True
        self.clear_right = True
        
        self.text_jaobject_0 = self.font_jaobject_0.render("移動せよ", True, (0, 0, 0))
        self.rect_ja = self.text_jaobject_0.get_rect(center=screen_rect.center)
        
        self.text_enobject_0 = self.font_enobject_0.render("Move", True, (0, 0, 0))
        self.rect_en = self.text_enobject_0.get_rect(center=(screen_rect.centerx, screen_rect.centery + 40))
        
        self.sym_object_0_1 = self.font_enobject_0.render("↑", True, (0, 0, 0))  
        self.rect_sym_0_1 = self.sym_object_0_1.get_rect(center=(screen_rect.centerx, screen_rect.centery - 120))
        
        self.sym_object_0_2 = self.font_enobject_0.render("↓", True, (0, 0, 0))  
        self.rect_sym_0_2 = self.sym_object_0_2.get_rect(center=(screen_rect.centerx, screen_rect.centery + 120))
        
        self.sym_object_0_3 = self.font_enobject_0.render("←", True, (0, 0, 0))  
        self.rect_sym_0_3 = self.sym_object_0_3.get_rect(center=(screen_rect.centerx - 120, screen_rect.centery))
        
        self.sym_object_0_4 = self.font_enobject_0.render("→", True, (0, 0, 0))
        self.rect_sym_0_4 = self.sym_object_0_4.get_rect(center=(screen_rect.centerx + 120, screen_rect.centery))
        
        #################

    # ステージ0
    def draw_object_0(self, screen, count_key, min_clear_move):
       
        if count_key[0] > min_clear_move and self.clear_left: self.clear_left = False
        if count_key[1] > min_clear_move and self.clear_right: self.clear_right = False
        if count_key[2] > min_clear_move and self.clear_up: self.clear_up = False
        if count_key[3] > min_clear_move and self.clear_down: self.clear_down = False
        
        if self.clear_up: screen.blit(self.sym_object_0_1, self.rect_sym_0_1)
        if self.clear_down: screen.blit(self.sym_object_0_2, self.rect_sym_0_2)
        if self.clear_left: screen.blit(self.sym_object_0_3, self.rect_sym_0_3)
        if self.clear_right: screen.blit(self.sym_object_0_4, self.rect_sym_0_4)
        
        if (self.clear_up == True or self.clear_down == True or self.clear_left == True or self.clear_right == True):
            screen.blit(self.text_jaobject_0, self.rect_ja)
            screen.blit(self.text_enobject_0, self.rect_en)
        
# ゲーム本体
class mainGame:
    
    def __init__(self):
        
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.background = Background()
        self.object = Gameobject(self.background.screen)
        
    def run_0(self):
        
        Clear_0 = True
        
        min_clear_move = 20
        
        while Clear_0:
            
            self.background.draw_background_0()
            
            self.player.draw(self.background.screen, 0)
            self.object.draw_object_0(self.background.screen, self.player.count_key, min_clear_move)
            
            keys = pygame.key.get_pressed()
            self.player.move_ice(keys)
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.flip()
            
            self.clock.tick(60)


# 各クラス呼び出し
if __name__ == "__main__":
    pygame.init()
    game = mainGame()
    
    game.run_0()

