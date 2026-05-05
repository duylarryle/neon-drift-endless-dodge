import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Drift: Endless Dodge")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 26)

# Colors
BACKGROUND = (8, 8, 18)
PLAYER_COLOR = (0, 255, 200)
PLAYER_GLOW = (0, 120, 255)
OBSTACLE_COLORS = [
    (255, 80, 80),
    (255, 120, 40),
    (255, 50, 160),
    (180, 80, 255)
]

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

# Background stars
stars = []

# Explosion particles
particles = []

# Game state
game_over = False
score = 0
high_score = 0
difficulty_level = 1
start_time = pygame.time.get_ticks()


def create_stars(amount):
    """Create background stars for a moving space effect."""
    new_stars = []

    for _ in range(amount):
        star = {
            "x": random.randint(0, WIDTH),
            "y": random.randint(0, HEIGHT),
            "speed": random.uniform(0.5, 2.0),
            "size": random.randint(1, 3)
        }
        new_stars.append(star)

    return new_stars


def draw_stars():
    """Move and draw background stars."""
    for star in stars:
        star["y"] += star["speed"]

        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            (80, 100, 160),
            (int(star["x"]), int(star["y"])),
            star["size"]
        )


def spawn_obstacle(difficulty):
    """Create a falling obstacle with speed based on difficulty."""
    x = random.randint(0, WIDTH - obstacle_size)
    y = -obstacle_size
    speed = random.randint(3, 6) + difficulty
    color = random.choice(OBSTACLE_COLORS)

    return {
        "rect": pygame.Rect(x, y, obstacle_size, obstacle_size),
        "speed": speed,
        "color": color
    }


def create_explosion(x, y):
    """Create particles when the player loses."""
    for _ in range(35):
        particle = {
            "x": x,
            "y": y,
            "vx": random.uniform(-5, 5),
            "vy": random.uniform(-5, 5),
            "life": random.randint(20, 40),
            "max_life": 40
        }
        particles.append(particle)


def update_particles():
    """Update and draw explosion particles."""
    for particle in particles[:]:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        particle["life"] -= 1

        fade = max(0, int(255 * (particle["life"] / particle["max_life"])))
        color = (fade, fade, 255)

        pygame.draw.circle(
            screen,
            color,
            (int(particle["x"]), int(particle["y"])),
            3
        )

        if particle["life"] <= 0:
            particles.remove(particle)


def reset_game():
    """Reset all gameplay values to start a new run."""
    global obstacles, particles, game_over, start_time
    global score, spawn_timer, difficulty_level

    obstacles = []
    particles = []
    game_over = False
    start_time = pygame.time.get_ticks()
    score = 0
    spawn_timer = 0
    difficulty_level = 1

    player.x = WIDTH // 2
    player.y = HEIGHT - 80


def draw_player():
    """Draw the player with a simple neon glow outline."""
    glow_rect = player.inflate(12, 12)
    pygame.draw.rect(screen, PLAYER_GLOW, glow_rect, border_radius=8)
    pygame.draw.rect(screen, PLAYER_COLOR, player, border_radius=6)


def draw_ui():
    """Draw score, difficulty, and high score."""
    score_text = font.render(f"Score: {score}", True, (220, 220, 255))
    screen.blit(score_text, (10, 10))

    difficulty_text = small_font.render(
        f"Difficulty: {difficulty_level}",
        True,
        (180, 180, 230)
    )
    screen.blit(difficulty_text, (10, 45))

    high_score_text = small_font.render(
        f"High Score: {high_score}",
        True,
        (180, 180, 230)
    )
    screen.blit(high_score_text, (10, 70))


def draw_game_over():
    """Draw the game over screen."""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(120)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
    restart_text = small_font.render(
        "Press R to Restart",
        True,
        (220, 220, 255)
    )
    final_score_text = small_font.render(
        f"Final Score: {score}",
        True,
        (220, 220, 255)
    )

    screen.blit(game_over_text, (WIDTH // 2 - 85, HEIGHT // 2 - 50))
    screen.blit(final_score_text, (WIDTH // 2 - 70, HEIGHT // 2 - 10))
    screen.blit(restart_text, (WIDTH // 2 - 75, HEIGHT // 2 + 25))


stars = create_stars(80)

while True:
    screen.fill(BACKGROUND)
    draw_stars()

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
                high_score = max(high_score, score)
                create_explosion(player.centerx, player.centery)

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, obs["color"], obs["rect"], border_radius=5)

    draw_player()
    update_particles()
    draw_ui()

    if game_over:
        draw_game_over()

    pygame.display.flip()
    clock.tick(60)