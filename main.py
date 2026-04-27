import pygame
import random
import sys

# Initialize
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
spawn_delay = 30

# Game state
game_over = False
score = 0
start_time = pygame.time.get_ticks()

def spawn_obstacle():
    x = random.randint(0, WIDTH - obstacle_size)
    y = -obstacle_size
    speed = random.randint(3, 6)
    return {"rect": pygame.Rect(x, y, obstacle_size, obstacle_size), "speed": speed}

def reset_game():
    global obstacles, game_over, start_time, score
    obstacles = []
    game_over = False
    start_time = pygame.time.get_ticks()
    score = 0
    player.x = WIDTH // 2
    player.y = HEIGHT - 80

# Game loop
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

        # Keep player on screen
        player.clamp_ip(screen.get_rect())

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            obstacles.append(spawn_obstacle())
            spawn_timer = 0

        # Move obstacles
        for obs in obstacles:
            obs["rect"].y += obs["speed"]

        # Remove off-screen obstacles
        obstacles = [obs for obs in obstacles if obs["rect"].y < HEIGHT + 50]

        # Collision
        for obs in obstacles:
            if player.colliderect(obs["rect"]):
                game_over = True

        # Score (based on survival time)
        score = (pygame.time.get_ticks() - start_time) // 100

    # Draw player
    pygame.draw.rect(screen, (0, 255, 200), player)

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, (255, 80, 80), obs["rect"])

    # Draw score
    score_text = font.render(f"Score: {score}", True, (200, 200, 255))
    screen.blit(score_text, (10, 10))

    # Game over text
    if game_over:
        over_text = font.render("GAME OVER - Press R to Restart", True, (255, 255, 255))
        screen.blit(over_text, (WIDTH // 2 - 180, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)