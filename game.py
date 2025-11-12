import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaga Style Game")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 시계
clock = pygame.time.Clock()
FPS = 60

# 폰트
font = pygame.font.SysFont("malgungothic", 36)
small_font = pygame.font.SysFont("malgungothic", 24)

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, BLUE, [(25, 0), (0, 40), (50, 40)])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 8
        self.lives = 3
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# 적군 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, RED, [(20, 0), (0, 30), (40, 30)])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(1, 3)
        self.direction = 1  # 1: 오른쪽, -1: 왼쪽
        self.move_counter = 0

    def update(self):
        self.rect.x += self.speed * self.direction
        self.move_counter += 1
        if self.move_counter > 80:
            self.rect.y += 30
            self.direction *= -1
            self.move_counter = 0

# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# 스프라이트 그룹
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# 적 생성 함수
def spawn_enemies():
    for row in range(3):
        for col in range(8):
            enemy = Enemy(100 + col * 50, 100 + row * 50)
            all_sprites.add(enemy)
            enemies.add(enemy)

spawn_enemies()

# 게임 루프
running = True
game_over = False

while running:
    clock.tick(FPS)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()
            if event.key == pygame.K_r and game_over:
                # 재시작
                player = Player()
                all_sprites.add(player)
                for sprite in all_sprites:
                    if sprite != player:
                        sprite.kill()
                spawn_enemies()
                game_over = False

    if not game_over:
        # 업데이트
        all_sprites.update()

        # 충돌: 총알 ↔ 적
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            player.score += 10

        # 충돌: 적 ↔ 플레이어
        if pygame.sprite.spritecollide(player, enemies, True):
            player.lives -= 1
            if player.lives <= 0:
                game_over = True

        # 적이 화면 아래로 내려오면 게임 오버
        for enemy in enemies:
            if enemy.rect.top > HEIGHT:
                game_over = True

        # 모든 적 제거 시 새로운 웨이브
        if len(enemies) == 0:
            spawn_enemies()

    # 화면 그리기
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # UI
    score_text = small_font.render(f"점수: {player.score}", True, WHITE)
    lives_text = small_font.render(f"목숨: {player.lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    if game_over:
        game_over_text = font.render("GAME OVER", True, RED)
        restart_text = small_font.render("R 키를 눌러 재시작", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()

pygame.quit()
sys.exit()