import pygame
import sys

# 1. セットアップ
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# キャラクターのデータ（ただの変数）
x, y = 400, 300
speed = 5

player = pygame.Rect(x, y, 50, 50)


# 2. メインループ
while True:
    # 3. 描画
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 255), player.center, player.width // 2)

    screen_rect = screen.get_rect()

    # 右端から完全に消えたら、左端へ
    if player.left > screen_rect.right:
        player.right = screen_rect.left

    # 左端から完全に消えたら、右端へ
    elif player.right < screen_rect.left:
        player.left = screen_rect.right

    # 下端から完全に消えたら、上端へ
    if player.top > screen_rect.bottom:
        player.bottom = screen_rect.top

    # 上端から完全に消えたら、下端へ
    elif player.bottom < screen_rect.top:
        player.top = screen_rect.bottom

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キー入力と移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed


    pygame.display.flip()
    clock.tick(60)