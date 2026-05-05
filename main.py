import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Drift: Endless Dodge")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Player
player_size = 40
player = pygame.Rect(WIDTH // 2, HEIGHT - 80, player_size, player_size)
player_speed = 6

# Obstacles
obstacles = []
obstacle_size = 30
spawn_timer = 0
base_spawn_delay = 30
min_spawn_delay = 8

# Game state
game_over = False
score = 0
difficulty_level = 1
start_time = pygame.time.get_ticks()


def spawn_obstacle(difficulty):
    x = random.randint(0, WIDTH - obstacle_size)
    y = -obstacle_size
    speed = random.randint(3, 6) + difficulty

    return {
        "rect": pygame.Rect(x, y, obstacle_size, obstacle_size),
        "speed": speed
    }


def reset_game():
    global obstacles, game_over, start_time, score, spawn_timer, difficulty_level

    obstacles = []
    game_over = False
    start_time = pygame.time.get_ticks()
    score = 0
    spawn_timer = 0
    difficulty_level = 1

    player.x = WIDTH // 2
    player.y = HEIGHT - 80


while True:
    screen.fill((10, 10, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:
        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += player_speed

        player.clamp_ip(screen.get_rect())

        # Score and difficulty
        score = (pygame.time.get_ticks() - start_time) // 100
        difficulty_level = 1 + score // 100
        current_spawn_delay = max(
            min_spawn_delay,
            base_spawn_delay - difficulty_level
        )

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer >= current_spawn_delay:
            obstacles.append(spawn_obstacle(difficulty_level))
            spawn_timer = 0

        # Move obstacles
        for obs in obstacles:
            obs["rect"].y += obs["speed"]

        # Remove off-screen obstacles
        obstacles = [
            obs for obs in obstacles
            if obs["rect"].y < HEIGHT + 50
        ]

        # Collision
        for obs in obstacles:
            if player.colliderect(obs["rect"]):
                game_over = True

    # Draw player
    pygame.draw.rect(screen, (0, 255, 200), player)

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, (255, 80, 80), obs["rect"])

    # Draw UI
    score_text = font.render(f"Score: {score}", True, (200, 200, 255))
    screen.blit(score_text, (10, 10))

    difficulty_text = font.render(
        f"Difficulty: {difficulty_level}",
        True,
        (200, 200, 255)
    )
    screen.blit(difficulty_text, (10, 45))

    if game_over:
        over_text = font.render(
            "GAME OVER - Press R to Restart",
            True,
            (255, 255, 255)
        )
        screen.blit(over_text, (WIDTH // 2 - 180, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)