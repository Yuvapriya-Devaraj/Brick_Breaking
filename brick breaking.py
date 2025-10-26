import pygame
import sys

# Initialize
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker - Multi-Level")

# Load sounds
bounce_sound = pygame.mixer.Sound("bounce.wav")
brick_hit_sound = pygame.mixer.Sound("brick_hit.wav")
lose_life_sound = pygame.mixer.Sound("lose_life.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
win_sound = pygame.mixer.Sound("win.wav")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRICK_COLOR = (200, 0, 0)
BALL_COLOR = (0, 200, 255)
PADDLE_COLOR = (0, 255, 100)
BUTTON_COLOR = (100, 100, 255)

# Fonts
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

# Clock
clock = pygame.time.Clock()

# Game state
score = 0
lives = 3
paused = False
game_started = False
game_over = False
level = 1
max_level = 5

# Game objects
paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 30, 100, 10)
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2, 15, 15)
ball_vel = [4, -4]

brick_cols = 8
brick_width = WIDTH // brick_cols
brick_height = 25

def create_bricks(level):
    bricks = []
    rows = 3 + level
    for row in range(rows):
        for col in range(brick_cols):
            if level % 2 == 0:
                if (row + col) % 2 == 0:
                    brick = pygame.Rect(col * brick_width + 2, row * brick_height + 2, brick_width - 4, brick_height - 4)
                    bricks.append(brick)
            elif level % 3 == 0:
                if row % 2 == 0:
                    brick = pygame.Rect(col * brick_width + 2, row * brick_height + 2, brick_width - 4, brick_height - 4)
                    bricks.append(brick)
            else:
                brick = pygame.Rect(col * brick_width + 2, row * brick_height + 2, brick_width - 4, brick_height - 4)
                bricks.append(brick)
    return bricks

def get_ball_speed(level):
    base_speed = 4
    speed_increment = 1
    return [base_speed + (level - 1) * speed_increment, -(base_speed + (level - 1) * speed_increment)]

bricks = create_bricks(level)

# ... rest of the code remains unchanged
def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, w, h))
    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(label, label_rect)
    return pygame.Rect(x, y, w, h)

def reset_game():
    global paddle, ball, ball_vel, bricks, score, lives, paused, game_over, level
    paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 30, 100, 10)
    ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2, 15, 15)
    ball_vel[:] = get_ball_speed(1)
    level = 1
    bricks[:] = create_bricks(level)
    score = 0
    lives = 3
    paused = False
    game_over = False

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)
    pygame.draw.ellipse(screen, BALL_COLOR, ball)
    for brick in bricks:
        pygame.draw.rect(screen, BRICK_COLOR, brick)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))
    screen.blit(level_text, (WIDTH // 2 - 50, 10))
    if paused:
        pause_text = big_font.render("Paused", True, WHITE)
        screen.blit(pause_text, pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()

def show_message(message, sound=None):
    if sound:
        sound.play()
    text = big_font.render(message, True, WHITE)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, rect)
    restart_button = draw_button("Restart", WIDTH // 2 - 70, HEIGHT // 2 + 10, 140, 50)
    quit_button = draw_button("Quit", WIDTH // 2 - 70, HEIGHT // 2 + 70, 140, 50)
    pygame.display.flip()
    return restart_button, quit_button

def show_start_screen():
    screen.fill(BLACK)
    title = big_font.render("Brick Breaker", True, WHITE)
    start_button = draw_button("Start Game", WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
    pygame.display.flip()
    return start_button

start_screen = True
while start_screen:
    clock.tick(60)
    start_button = show_start_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
            start_screen = False
            game_started = True

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_started and not game_over:
            if event.key == pygame.K_p:
                paused = not paused
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button.collidepoint(event.pos):
                reset_game()
            elif quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    if not paused and game_started and not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-6, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(6, 0)

        ball.x += ball_vel[0]
        ball.y += ball_vel[1]

        if ball.left <= 0 or ball.right >= WIDTH:
            ball_vel[0] *= -1
            bounce_sound.play()
        if ball.top <= 0:
            ball_vel[1] *= -1
            bounce_sound.play()

        if ball.colliderect(paddle):
            ball_vel[1] = -abs(ball_vel[1])
            bounce_sound.play()

        hit_index = ball.collidelist(bricks)
        if hit_index != -1:
            del bricks[hit_index]
            ball_vel[1] *= -1
            brick_hit_sound.play()
            score += 10

        if ball.bottom >= HEIGHT:
            lives -= 1
            lose_life_sound.play()
            if lives > 0:
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_vel = get_ball_speed(level)
                pygame.time.delay(1000)
            else:
                game_over = True
                restart_button, quit_button = show_message(f"Game Over! Final Score: {score}", sound=game_over_sound)

        if not bricks and not game_over:
            if level < max_level:
                level += 1
                bricks = create_bricks(level)
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_vel = get_ball_speed(level)
                pygame.time.delay(1000)
            else:
                game_over = True
                restart_button, quit_button = show_message(f"You Win! Final Score: {score}", sound=win_sound)

    if not game_over:
        draw()
