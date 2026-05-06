# Neon Drift: Endless Dodge

## Demo
Demo Video: (https://youtu.be/Mz29g49hC1Y)

## GitHub Repository
GitHub Repo: (https://github.com/duylarryle/neon-drift-endless-dodge)

## Description
Neon Drift: Endless Dodge is a one-screen arcade survival game created with Python and Pygame. The player controls a spaceship and tries to survive as long as possible by dodging incoming asteroids. The game becomes more difficult over time as the asteroids spawn faster and move at higher speeds.

The project is connected to digital arts and media because it combines programming, interactive design, pixel art, animation, visual effects, and game feel. The main goal was to create a small but polished arcade-style experience that demonstrates movement, collision detection, scoring, sprites, power-ups, and visual feedback.

## Gameplay
The player moves the spaceship using the keyboard and avoids falling asteroids. The score increases the longer the player survives. If the player collides with an asteroid without a shield active, the game ends and the player can restart.

The game includes several power-ups:
- **Shield**: protects the player from asteroid collisions for a short time.
- **Slow Motion**: temporarily slows down the falling asteroids.
- **2x Score**: temporarily doubles the score gain.

## Controls
- `WASD` or `Arrow Keys` - Move the spaceship
- `R` - Restart after game over
- Close the window - Quit the game

## Design Considerations
One of the main design goals was to keep the game simple but satisfying to play. Instead of building a large game with multiple levels, the project focuses on one strong arcade gameplay loop: dodge, survive, collect power-ups, and beat your high score.

The player sprite is visually larger than the actual collision area. This was intentional because a smaller centered hitbox makes the game feel more fair. The full sprite is still used for collecting power-ups, so power-up collection feels easier and more rewarding.

The difficulty increases over time by raising the obstacle speed and reducing the delay between obstacle spawns. This creates an endless survival challenge where the game starts approachable but becomes more intense the longer the player survives.

## Credits

### Pixel Art Assets
Pixel art assets used in this project are from:

- **Free Shoot'em Up starter Asset Pack** by Timberlate007 on itch.io  
  https://timberlate007.itch.io/shootem-up

Assets from this pack were used or adapted for the player ship, asteroids, power-ups, and space background.

### Programming References
The following resources were used as references for learning Pygame concepts used in this project:

- **Pygame Rect Documentation**  
  Used for rectangle positioning and collision detection.  
  https://www.pygame.org/docs/ref/rect.html

- **Pygame Image Documentation**  
  Used for loading PNG image assets.  
  https://www.pygame.org/docs/ref/image.html

- **Pygame Transform Documentation**  
  Used for scaling sprites to the correct game size.  
  https://www.pygame.org/docs/ref/transform.html

- **Pygame Draw Documentation**  
  Used for drawing fallback shapes, circles, outlines, and particle effects.  
  https://www.pygame.org/docs/ref/draw.html

- **Pygame “Move It” Tutorial**  
  Used as a reference for drawing and moving images on screen with `blit()`.  
  https://www.pygame.org/docs/tut/MoveIt.html

- **KidsCanCode - Pygame Shmup Part 12: Powerups**  
  Used as a general reference for collectible power-up behavior in an arcade-style game.  
  https://youtu.be/z6h6l1yJ5-w