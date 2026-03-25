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
        self.delta = [0, 0, 0, 0]               # 移動量（変化量）
        self.key_info = [pygame.K_LEFT, 
                         pygame.K_RIGHT, 
                         pygame.K_UP, 
                         pygame.K_DOWN]         # キー情報
        self.count_time = 0                     # 時間カウント
        self.speed = 5                          # 移動速度
        self.accel_gain = 1.5                   # 等加速度運動時の加速度（加速）
        self.brake_gain = 0.4                   # 等加速度運動時の加速度（減速）
        self.speed_limit = 25                   # 等加速度運動時の速度上限  
        self.move_gain = 0.1                    # 移動倍率
        self.radius = player.width // 2         # 円の半径
    
    # 描画 
    def draw(self, screen, enable_shaking = False):

        # 震えるアニメーションが有効なら半径をsin波的に動かす
        if enable_shaking:
            self.count_time += 1
            pygame.draw.circle(screen, (0, 0, 255), self.player.center, math.sin(self.count_time * 0.1) * 7 + self.radius)
        else:
            pygame.draw.circle(screen, (0, 0, 255), self.player.center, self.radius)
    
    # マウス追従（テスト中）←多分間に合わない！！
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
    
    # 等加速度運動（第3引数ではワープするか，第4引数では当たり判定を）
    def move_ice(self, keys, enable_warp = True, walls = None):
        
        for i in range(4):
            
            if keys[self.key_info[i]]:
                self.count_key[i] += self.accel_gain
                self.delta[i] += self.accel_gain
                
            if not keys[self.key_info[i]] and self.count_key[i] > 0:
                self.count_key[i] -= self.brake_gain
                self.delta[i] += self.brake_gain
                
            if self.count_key[i] < 0:
                self.count_key[i] = 0
                
            if self.count_key[i] > self.speed_limit:
                self.count_key[i] = self.speed_limit
            
        move_x = 0
        move_y = 0
        
        if self.count_key[0] > 0:
            move_x -= self.count_key[0] ** 2 * self.move_gain
        if self.count_key[1] > 0:
            move_x += self.count_key[1] ** 2 * self.move_gain
        if self.count_key[2] > 0:
            move_y -= self.count_key[2] ** 2 * self.move_gain
        if self.count_key[3] > 0:
            move_y += self.count_key[3] ** 2 * self.move_gain

        self.player.x += int(move_x)
        
        # 当たり判定有の処理
        if walls:
            for wall in walls:
                if self.player.colliderect(wall):
                    if move_x > 0:
                        self.player.right = wall.left
                        self.count_key[1] = 0
                    elif move_x < 0:
                        self.player.left = wall.right
                        self.count_key[0] = 0

        self.player.y += int(move_y)

        # 当たり判定有の処理        
        if walls:
            for wall in walls:
                if self.player.colliderect(wall):
                    if move_y > 0:
                        self.player.bottom = wall.top
                        self.count_key[3] = 0
                    elif move_y < 0:
                        self.player.top = wall.bottom
                        self.count_key[2] = 0

        if enable_warp: self.warp(pygame.display.get_surface().get_rect())
        
        
# 背景
class Background:
    
    # 背景コンストラクタ
    def __init__(self):

        display_info = pygame.display.Info()
        window_w = max(960, display_info.current_w - 60)
        window_h = max(640, display_info.current_h - 60)
        screen = pygame.display.set_mode((window_w, window_h), pygame.RESIZABLE)
        pygame.display.set_caption("2026 spring program")
        self.font_H = pygame.font.SysFont("msgothic", 32)            # フォント設定
        self.font_P = pygame.font.SysFont("arial", 24)            # フォント設定
        self.screen = screen                                           # 背景インスタンス
        
        self.init_background_0()
        self.init_background_1()
        self.init_background_2()
        
        
    def init_background_0(self):
        self.text_location_0 = self.font_H.render("0", True, (0, 0, 0))  # テキスト設定
        self.text_jamission_0 = self.font_H.render("チュートリアル", True, (0, 0, 0))  # テキスト設定
        self.text_enmission_0 = self.font_P.render("Tutorial", True, (0, 0, 0))  # テキスト設定
    
    # 背景0描画
    def draw_background_0(self):
        
        self.screen.fill((255, 255, 255))                           # 画面描画
        self.screen.blit(self.text_location_0, (50, 50))            # テキスト描画
        self.screen.blit(self.text_jamission_0, (100, 50))          # テキスト描画
        self.screen.blit(self.text_enmission_0, (400, 55))          # テキスト描画
    
    def init_background_1(self):
        
        self.text_location_1 = self.font_H.render("1", True, (0, 0, 0))  # テキスト設定
        self.text_jamission_1 = self.font_H.render("たどり着け", True, (0, 0, 0))  # テキスト設定
        self.text_enmission_1 = self.font_P.render("Arrive", True, (0, 0, 0))  # テキスト設定
    
    def draw_background_1(self):
        
        self.screen.fill((255, 255, 255))                           # 画面描画
        self.screen.blit(self.text_location_1, (50, 50))            # テキスト描画
        self.screen.blit(self.text_jamission_1, (100, 50))          # テキスト描画
        self.screen.blit(self.text_enmission_1, (400, 55))          # テキスト描画
        
    def init_background_2(self):
        
        self.text_location_2 = self.font_H.render("2", True, (0, 0, 0))  # テキスト設定
        self.text_jamission_2 = self.font_H.render("ここから退出しろ", True, (0, 0, 0))  # テキスト設定
        self.text_enmission_2 = self.font_P.render("Exit", True, (0, 0, 0))  # テキスト設定
    
    def draw_background_2(self):
        
        self.screen.fill((255, 255, 255))                           # 画面描画
        self.screen.blit(self.text_location_2, (50, 50))            # テキスト描画
        self.screen.blit(self.text_jamission_2, (100, 50))          # テキスト描画
        self.screen.blit(self.text_enmission_2, (400, 55))          # テキスト描画
    
    

# オブジェクトたち     
class Gameobject:
    
    # オブジェクトコンストラクタ
    def __init__(self, screen):
        
        # ウインドウの中心座標取得
        self.screen_rect = screen.get_rect()
        self.center_x, self.center_y = self.screen_rect.center
        
        # テキストのフォント
        self.font_jaobject_0 = pygame.font.SysFont("msgothic", 40)
        self.font_enobject_0 = pygame.font.SysFont("arial", 30)
        
        self.clear_wait_frames = 30     # ステージクリア後の待機秒数
        self.clear_wait_count = 0
        
        self.fade_speed = 5
        
        self.init_object_0()
        self.init_object_1()
            
    def init_object_0(self):
        
        self.alpha_up = 255
        self.alpha_down = 255
        self.alpha_left = 255
        self.alpha_right = 255
        self.alpha_text = 255
        self.clear_wait_count = 0
        
        self.text_jaobject_0 = self.font_jaobject_0.render("移動せよ", True, (0, 0, 0)).convert_alpha()
        self.rect_ja = self.text_jaobject_0.get_rect(center=self.screen_rect.center)
        
        self.text_enobject_0 = self.font_enobject_0.render("Move", True, (0, 0, 0)).convert_alpha()
        self.rect_en = self.text_enobject_0.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 40))
        
        self.sym_object_0_1 = self.font_enobject_0.render("↑", True, (0, 0, 0)).convert_alpha()  
        self.rect_sym_0_1 = self.sym_object_0_1.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery - 120))
        
        self.sym_object_0_2 = self.font_enobject_0.render("↓", True, (0, 0, 0)).convert_alpha()  
        self.rect_sym_0_2 = self.sym_object_0_2.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 120))
        
        self.sym_object_0_3 = self.font_enobject_0.render("←", True, (0, 0, 0)).convert_alpha()  
        self.rect_sym_0_3 = self.sym_object_0_3.get_rect(center=(self.screen_rect.centerx - 120, self.screen_rect.centery))
        
        self.sym_object_0_4 = self.font_enobject_0.render("→", True, (0, 0, 0)).convert_alpha()
        self.rect_sym_0_4 = self.sym_object_0_4.get_rect(center=(self.screen_rect.centerx + 120, self.screen_rect.centery))

    # ステージ0
    def draw_object_0(self, screen, delta, min_clear_move):

        # キー入力カウントチェックとアルファ値更新
        if delta[0] > min_clear_move: self.alpha_left = max(0, self.alpha_left - self.fade_speed)
        if delta[1] > min_clear_move: self.alpha_right = max(0, self.alpha_right - self.fade_speed)
        if delta[2] > min_clear_move: self.alpha_up = max(0, self.alpha_up - self.fade_speed)
        if delta[3] > min_clear_move: self.alpha_down = max(0, self.alpha_down - self.fade_speed)
        
        # 矢印描画
        if self.alpha_up > 0:
            self.sym_object_0_1.set_alpha(self.alpha_up)
            screen.blit(self.sym_object_0_1, self.rect_sym_0_1)
        if self.alpha_down > 0:
            self.sym_object_0_2.set_alpha(self.alpha_down)
            screen.blit(self.sym_object_0_2, self.rect_sym_0_2)
        if self.alpha_left > 0:
            self.sym_object_0_3.set_alpha(self.alpha_left)
            screen.blit(self.sym_object_0_3, self.rect_sym_0_3)
        if self.alpha_right > 0:
            self.sym_object_0_4.set_alpha(self.alpha_right)
            screen.blit(self.sym_object_0_4, self.rect_sym_0_4)
        
        # 矢印が全部消えたらテキストをフェードアウトし、少し待ってからクリア
        if self.alpha_up <= 0 and self.alpha_down <= 0 and self.alpha_left <= 0 and self.alpha_right <= 0:
            self.alpha_text = max(0, self.alpha_text - self.fade_speed)
            if self.alpha_text <= 0:
                self.clear_wait_count += 1
                if self.clear_wait_count >= self.clear_wait_frames:
                    return 0  # ステージクリア
            else:
                self.clear_wait_count = 0

        if self.alpha_text > 0:
            self.text_jaobject_0.set_alpha(self.alpha_text)
            self.text_enobject_0.set_alpha(self.alpha_text)
            screen.blit(self.text_jaobject_0, self.rect_ja)
            screen.blit(self.text_enobject_0, self.rect_en)

        return 1
    
    def init_object_1(self):
        
        # 文字マップ: #=壁, .=通路, S=スタート, G=ゴール
        # プログラミング基礎の応用をAIさんに教えていただいたので実装してみた
        maze_map = [
            "##################",
            "#S..#........#...#",
            "#.#.#.######.#.#.#",
            "#.#...#....#...#.#",
            "#.#####.##.#####.#",
            "#.....#..#.....#.#",
            "###.#.####.###.#.#",
            "#...#......#...#.#",
            "#.##########.###.#",
            "#...............G#",
            "##################",
        ]

        tile = 50
        rows = len(maze_map)
        cols = len(maze_map[0])
        maze_width = cols * tile
        maze_height = rows * tile
        left = self.screen_rect.centerx - maze_width // 2
        top = self.screen_rect.centery - maze_height // 2 + 40

        self.maze_walls = []
        self.goal_rect = pygame.Rect(left, top, tile, tile)
        self.start_pos = (left + tile // 2, top + tile // 2)

        for row_idx, row in enumerate(maze_map):
            for col_idx, cell in enumerate(row):
                x = left + col_idx * tile
                y = top + row_idx * tile
                rect = pygame.Rect(x, y, tile, tile)
                if cell == "#":
                    self.maze_walls.append(rect)
                elif cell == "S":
                    self.start_pos = rect.center
                elif cell == "G":
                    self.goal_rect = rect.inflate(-16, -16)

    def draw_object_1(self, screen, player_rect):
        
        # 迷路の壁を描画
        for rect in self.maze_walls:
            pygame.draw.rect(screen, (20, 20, 20), rect)

        # ゴールを描画
        pygame.draw.rect(screen, (0, 180, 0), self.goal_rect)

        # プレイヤーがゴールに触れたらクリア
        if player_rect.colliderect(self.goal_rect):
            return 0

        return 1
    

        
        
# ゲーム本体
class mainGame:
    
    def __init__(self):
        
        # 各クラスから使いたい材料を取ってくる
        self.clock = pygame.time.Clock()
        
        
    def init_run_0(self):
        
        self.player = Player()
        self.background = Background()
        self.object = Gameobject(self.background.screen)
    
    def init_run1(self):
        
        self.player = Player()
        self.background = Background()
        self.object = Gameobject(self.background.screen)
    
    def init_run_2(self):
        
        self.player = Player()
        self.background = Background()
        self.object = Gameobject(self.background.screen)
        
    
    # ステージ0（チュートリアル）
    def run_0(self):
        
        self.init_run_0()
        
        Clear_0 = True          # クリアフラグ

        min_clear_move = 20     # クリアに必要な移動量の最小値
        
        # クリアするまで繰り返す
        while Clear_0:
            
            # 背景を描画する
            self.background.draw_background_0()
            
            # オブジェクトとプレイヤーを描画する
            self.player.draw(self.background.screen, 0)
            # オブジェクト描画時にクリア判定も一緒に行う（あんまりよくない設計な気がする．．．）
            Clear_0 = self.object.draw_object_0(self.background.screen, self.player.delta, min_clear_move)
            
            # 等加速度運動を行う
            keys = pygame.key.get_pressed()
            self.player.move_ice(keys)
            
            # 退出イベント
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.flip()
            
            self.clock.tick(60)
    
    def run_1(self):
        
        self.init_run1()
        
        Clear_1 = True          # クリアフラグ
        
        self.player.player.center = self.object.start_pos
        self.player.count_key = [0, 0, 0, 0]
        self.player.delta = [0, 0, 0, 0]
        
        while Clear_1:
            # 背景を描画する
            self.background.draw_background_1()
            
            # オブジェクトとプレイヤーを描画する
            Clear_1 = self.object.draw_object_1(self.background.screen, self.player.player)
            self.player.draw(self.background.screen, 0)
            
            # 等加速度運動を行う
            keys = pygame.key.get_pressed()
            self.player.move_ice(keys, enable_warp = False, walls = self.object.maze_walls)
            
            # 退出イベント
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.flip()
            
            self.clock.tick(60)
        
    def run_2(self):
        
        self.init_run_2()   
        
        Clear_2 = True          # クリアフラグ
        clear_triggered = False
        clear_alpha = 0
        clear_hold_count = 0
        clear_hold_frames = 30
        clear_text = self.background.font_H.render("Clear", True, (20, 140, 20)).convert_alpha()
        clear_rect = clear_text.get_rect(center=self.background.screen.get_rect().center)
        
        while Clear_2:
            
            self.background.draw_background_2()
            
            self.player.draw(self.background.screen, 0)  
            if not clear_triggered:
                keys = pygame.key.get_pressed()
                self.player.move_ice(keys, enable_warp = True, walls = None)
            else:
                clear_alpha = min(255, clear_alpha + 8)
                clear_text.set_alpha(clear_alpha)
                self.background.screen.blit(clear_text, clear_rect)
                if clear_alpha >= 255:
                    clear_hold_count += 1
                    if clear_hold_count >= clear_hold_frames:
                        Clear_2 = False
            
            # 退出イベント
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clear_triggered = True
                    
            pygame.display.flip()
            
            self.clock.tick(60)  
        
           


# 各クラス呼び出し（本体）
if __name__ == "__main__":
    pygame.init()
    game = mainGame()
    
    game.run_0()
    game.run_1()
    game.run_2()