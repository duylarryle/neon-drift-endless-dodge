import os
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

BASE_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(BASE_DIR, "assets")

# Colors
BACKGROUND = (8, 8, 18)
PLAYER_COLOR = (0, 255, 200)

SHIELD_COLOR = (0, 180, 255)
SLOW_COLOR = (180, 80, 255)
MULTIPLIER_COLOR = (255, 220, 60)

OBSTACLE_COLORS = [
    (255, 80, 80),
    (255, 120, 40),
    (255, 50, 160),
    (180, 80, 255)
]

# Player
player_size = 64
player = pygame.Rect(0, 0, player_size, player_size)
player.center = (WIDTH // 2, HEIGHT - 110)
player_speed = 6

# Smaller collision box
player_hitbox_size = 38
player_hitbox = pygame.Rect(0, 0, player_hitbox_size, player_hitbox_size)

# Obstacles
obstacles = []
asteroid_1_size = 51
asteroid_2_size = 56
spawn_timer = 0
base_spawn_delay = 30
min_spawn_delay = 8

# Power-ups
powerups = []
powerup_size = 48
powerup_spawn_timer = 0
powerup_spawn_delay = 360

shield_active = False
shield_end_time = 0
shield_duration = 5000

slow_active = False
slow_end_time = 0
slow_duration = 4000

multiplier_active = False
multiplier_end_time = 0
multiplier_duration = 6000
multiplier_value = 2

# Background stars
stars = []

# Effect particles
particles = []

# Game state
game_over = False
score = 0
score_value = 0.0
high_score = 0
difficulty_level = 1


def load_image(filename, size=None):
    """Load an image from the assets folder."""
    path = os.path.join(ASSET_DIR, filename)

    try:
        image = pygame.image.load(path).convert_alpha()

        if size is not None:
            image = pygame.transform.scale(image, size)

        return image

    except FileNotFoundError:
        print(f"Warning: Missing asset file: {filename}")
        return None

    except pygame.error:
        print(f"Warning: Could not load asset file: {filename}")
        return None


# Load assets
background_image = load_image("background.png", (WIDTH, HEIGHT))
player_image = load_image("player.png", (player_size, player_size))

asteroid_image_1 = load_image(
    "asteroid.png",
    (asteroid_1_size, asteroid_1_size)
)

asteroid_image_2 = load_image(
    "asteroid_2.png",
    (asteroid_2_size, asteroid_2_size)
)

obstacle_assets = []

if asteroid_image_1 is not None:
    obstacle_assets.append({
        "image": asteroid_image_1,
        "size": asteroid_1_size
    })

if asteroid_image_2 is not None:
    obstacle_assets.append({
        "image": asteroid_image_2,
        "size": asteroid_2_size
    })

powerup_images = {
    "shield": load_image("shield.png", (powerup_size, powerup_size)),
    "slow": load_image("slow.png", (powerup_size, powerup_size)),
    "multiplier": load_image("multiplier.png", (powerup_size, powerup_size))
}


def update_player_hitbox():
    """Keep the smaller hitbox centered inside the player sprite."""
    player_hitbox.center = player.center


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


def draw_background():
    """Draw the background image and moving star layer."""
    if background_image is not None:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(BACKGROUND)

    draw_stars()


def draw_stars():
    """Move and draw background stars."""
    for star in stars:
        star["y"] += star["speed"]

        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            (90, 130, 200),
            (int(star["x"]), int(star["y"])),
            star["size"]
        )


def spawn_obstacle(difficulty):
    """Create a falling obstacle with speed based on difficulty."""
    if obstacle_assets:
        asset = random.choice(obstacle_assets)
        image = asset["image"]
        obstacle_size = asset["size"]
    else:
        image = None
        obstacle_size = random.choice([asteroid_1_size, asteroid_2_size])

    x = random.randint(0, WIDTH - obstacle_size)
    y = -obstacle_size
    speed = random.randint(3, 6) + difficulty
    color = random.choice(OBSTACLE_COLORS)

    rect = pygame.Rect(x, y, obstacle_size, obstacle_size)

    return {
        "rect": rect,
        "y": float(y),
        "speed": speed,
        "color": color,
        "image": image
    }


def spawn_powerup():
    """Create a falling power-up."""
    x = random.randint(0, WIDTH - powerup_size)
    y = -powerup_size
    powerup_type = random.choice(["shield", "slow", "multiplier"])

    if powerup_type == "shield":
        color = SHIELD_COLOR
    elif powerup_type == "slow":
        color = SLOW_COLOR
    else:
        color = MULTIPLIER_COLOR

    return {
        "rect": pygame.Rect(x, y, powerup_size, powerup_size),
        "speed": 3,
        "type": powerup_type,
        "color": color,
        "image": powerup_images[powerup_type]
    }


def create_explosion(x, y, color=(180, 200, 255), amount=35):
    """Create particles for explosions and power-up effects."""
    for _ in range(amount):
        particle = {
            "x": x,
            "y": y,
            "vx": random.uniform(-5, 5),
            "vy": random.uniform(-5, 5),
            "life": random.randint(20, 40),
            "max_life": 40,
            "color": color
        }
        particles.append(particle)


def update_particles():
    """Update and draw effect particles."""
    for particle in particles[:]:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        particle["life"] -= 1

        fade_ratio = max(0, particle["life"] / particle["max_life"])
        base_color = particle["color"]

        color = (
            int(base_color[0] * fade_ratio),
            int(base_color[1] * fade_ratio),
            int(base_color[2] * fade_ratio)
        )

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
    global obstacles, powerups, particles, game_over
    global score, score_value, spawn_timer, difficulty_level
    global powerup_spawn_timer
    global shield_active, shield_end_time
    global slow_active, slow_end_time
    global multiplier_active, multiplier_end_time

    obstacles = []
    powerups = []
    particles = []

    game_over = False
    score = 0
    score_value = 0.0
    spawn_timer = 0
    powerup_spawn_timer = 0
    difficulty_level = 1

    shield_active = False
    shield_end_time = 0

    slow_active = False
    slow_end_time = 0

    multiplier_active = False
    multiplier_end_time = 0

    player.center = (WIDTH // 2, HEIGHT - 110)
    update_player_hitbox()


def draw_player():
    """Draw the player sprite with a thin outline around the real hitbox."""
    if player_image is not None:
        screen.blit(player_image, player.topleft)
    else:
        pygame.draw.rect(screen, PLAYER_COLOR, player, border_radius=6)

    # Thin hitbox outline. This shows the real collision area.
    # outline_rect = player_hitbox.inflate(10, 10)
    # pygame.draw.ellipse(screen, (0, 170, 255), outline_rect, 2)

    if shield_active:
        shield_rect = player.inflate(30, 30)
        pygame.draw.ellipse(screen, SHIELD_COLOR, shield_rect, 3)


def draw_obstacles():
    """Draw all obstacles as asteroid sprites or fallback circles."""
    for obs in obstacles:
        if obs["image"] is not None:
            screen.blit(obs["image"], obs["rect"].topleft)
        else:
            pygame.draw.ellipse(screen, obs["color"], obs["rect"])


def draw_powerups():
    """Draw all active power-ups as sprites or fallback symbols."""
    for powerup in powerups:
        if powerup["image"] is not None:
            screen.blit(powerup["image"], powerup["rect"].topleft)
        else:
            pygame.draw.ellipse(screen, powerup["color"], powerup["rect"])

            if powerup["type"] == "shield":
                label = "S"
            elif powerup["type"] == "slow":
                label = "T"
            else:
                label = "X"

            label_text = small_font.render(label, True, (255, 255, 255))
            label_rect = label_text.get_rect(center=powerup["rect"].center)
            screen.blit(label_text, label_rect)


def draw_ui():
    """Draw score, difficulty, high score, and power-up status."""
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    difficulty_text = small_font.render(
        f"Difficulty: {difficulty_level}",
        True,
        (220, 220, 255)
    )
    screen.blit(difficulty_text, (10, 45))

    high_score_text = small_font.render(
        f"High Score: {high_score}",
        True,
        (220, 220, 255)
    )
    screen.blit(high_score_text, (10, 70))

    y_position = 95

    if shield_active:
        shield_text = small_font.render(
            "Shield Active",
            True,
            SHIELD_COLOR
        )
        screen.blit(shield_text, (10, y_position))
        y_position += 25

    if slow_active:
        slow_text = small_font.render(
            "Slow Motion Active",
            True,
            SLOW_COLOR
        )
        screen.blit(slow_text, (10, y_position))
        y_position += 25

    if multiplier_active:
        multiplier_text = small_font.render(
            "2x Score Active",
            True,
            MULTIPLIER_COLOR
        )
        screen.blit(multiplier_text, (10, y_position))


def draw_game_over():
    """Draw the game over screen."""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(145)
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

    screen.blit(game_over_text, (WIDTH // 2 - 85, HEIGHT // 2 - 55))
    screen.blit(final_score_text, (WIDTH // 2 - 70, HEIGHT // 2 - 15))
    screen.blit(restart_text, (WIDTH // 2 - 75, HEIGHT // 2 + 20))


stars = create_stars(55)
update_player_hitbox()

while True:
    draw_background()

    current_time = pygame.time.get_ticks()

    # Turn off timed power-ups when they expire
    if shield_active and current_time > shield_end_time:
        shield_active = False

    if slow_active and current_time > slow_end_time:
        slow_active = False

    if multiplier_active and current_time > multiplier_end_time:
        multiplier_active = False

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
        update_player_hitbox()

        # Score system
        # Slow motion does NOT affect score.
        delta_time = clock.get_time() / 1000

        if multiplier_active:
            score_multiplier = multiplier_value
        else:
            score_multiplier = 1

        score_value += 10 * score_multiplier * delta_time
        score = int(score_value)

        # Difficulty scaling
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

        # Spawn power-ups
        powerup_spawn_timer += 1
        if powerup_spawn_timer >= powerup_spawn_delay:
            powerups.append(spawn_powerup())
            powerup_spawn_timer = 0

        # Slow motion only affects obstacle movement
        if slow_active:
            speed_multiplier = 0.45
        else:
            speed_multiplier = 1.0

        # Move obstacles smoothly using float y value
        for obs in obstacles:
            obs["y"] += obs["speed"] * speed_multiplier
            obs["rect"].y = int(obs["y"])

        # Move power-ups normally
        for powerup in powerups:
            powerup["rect"].y += powerup["speed"]

        # Remove off-screen obstacles and power-ups
        obstacles = [
            obs for obs in obstacles
            if obs["rect"].y < HEIGHT + 60
        ]

        powerups = [
            powerup for powerup in powerups
            if powerup["rect"].y < HEIGHT + 60
        ]

        # Power-up collection uses full player sprite area
        for powerup in powerups[:]:
            if player.colliderect(powerup["rect"]):
                if powerup["type"] == "shield":
                    shield_active = True
                    shield_end_time = current_time + shield_duration
                    create_explosion(
                        player.centerx,
                        player.centery,
                        SHIELD_COLOR,
                        25
                    )

                elif powerup["type"] == "slow":
                    slow_active = True
                    slow_end_time = current_time + slow_duration
                    create_explosion(
                        player.centerx,
                        player.centery,
                        SLOW_COLOR,
                        25
                    )

                elif powerup["type"] == "multiplier":
                    multiplier_active = True
                    multiplier_end_time = current_time + multiplier_duration
                    create_explosion(
                        player.centerx,
                        player.centery,
                        MULTIPLIER_COLOR,
                        25
                    )

                powerups.remove(powerup)

        # Obstacle collision uses smaller player hitbox
        for obs in obstacles[:]:
            if player_hitbox.colliderect(obs["rect"]):
                if shield_active:
                    obstacles.remove(obs)
                    create_explosion(
                        obs["rect"].centerx,
                        obs["rect"].centery,
                        SHIELD_COLOR,
                        20
                    )
                else:
                    game_over = True
                    high_score = max(high_score, score)
                    create_explosion(player.centerx, player.centery)
                    break

    draw_obstacles()
    draw_powerups()
    draw_player()
    update_particles()
    draw_ui()

    if game_over:
        draw_game_over()

    pygame.display.flip()
    clock.tick(60)