import pygame
import sys
from PIL import Image

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)

# Mario character properties
mario_width, mario_height = 70, 70
mario_x, mario_y = 100, HEIGHT - mario_height - 107
mario_speed = 5
jump_height = 15
is_jumping = False
velocity_y = 0

# Load Mario image
mario_image = pygame.image.load('mario_image.png')
mario_image = pygame.transform.scale(mario_image, (mario_width, mario_height))

# Load obstacle image
obstacle_image = pygame.image.load('cactus.jpeg')
obstacle_image = pygame.transform.scale(obstacle_image, (60, 60))

# Load and prepare the GIF as an animated background
gif_path = "background.gif"
gif = Image.open(gif_path)
frames = []
frame_durations = []

# Extract each frame and its duration
try:
    while True:
        frame = gif.copy().convert("RGBA")
        pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
        frames.append(pygame.transform.scale(pygame_frame, (WIDTH, HEIGHT)))
        frame_durations.append(gif.info['duration'] / 1000)  # Convert duration to seconds
        gif.seek(len(frames))  # Move to the next frame
except EOFError:
    pass

# Ensure at least one frame is available
if not frames:
    raise ValueError("The GIF has no frames!")

current_frame = 0
frame_timer = 0

# Gravity
gravity = 0.8

# Obstacle properties
obstacle_width, obstacle_height = 30, 115
obstacle_x = WIDTH
obstacle_y = HEIGHT - 50 - obstacle_height
obstacle_speed = 5

def draw_mario(x, y):
    screen.blit(mario_image, (x, y))

def draw_obstacle(x, y):
    screen.blit(obstacle_image, (x, y))

def show_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, BLACK)
    restart_text = pygame.font.Font(None, 36).render("Press R to Restart", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()

def reset_game():
    global mario_x, mario_y, is_jumping, velocity_y, obstacle_x
    mario_x = 100
    mario_y = HEIGHT - mario_height - 107
    is_jumping = False
    velocity_y = 0
    obstacle_x = WIDTH

def main():
    global mario_x, mario_y, is_jumping, velocity_y, obstacle_x, current_frame, frame_timer

    running = True
    game_over = False

    while running:
        dt = clock.tick(FPS) / 1000  # Get the time elapsed since the last frame (in seconds)

        # Update the frame timer for the GIF
        frame_timer += dt
        if frame_timer >= frame_durations[current_frame]:
            frame_timer = 0
            current_frame = (current_frame + 1) % len(frames)

        # Draw the current background frame
        screen.blit(frames[current_frame], (0, 0))

        if game_over:
            show_game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game_over = False
                    reset_game()
        else:
            draw_mario(mario_x, mario_y)
            draw_obstacle(obstacle_x, HEIGHT - 50 - obstacle_height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Key controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                mario_x -= mario_speed
            if keys[pygame.K_RIGHT]:
                mario_x += mario_speed
            if keys[pygame.K_SPACE] and not is_jumping:
                is_jumping = True
                velocity_y = -jump_height

            # Apply gravity and jumping
            if is_jumping:
                mario_y += velocity_y
                velocity_y += gravity
                if mario_y >= HEIGHT - mario_height - 100:
                    mario_y = HEIGHT - mario_height - 107
                    is_jumping = False

            # Prevent Mario from going out of bounds
            mario_x = max(0, min(WIDTH - mario_width, mario_x))

            # Move obstacle
            obstacle_x -= obstacle_speed
            if obstacle_x < -obstacle_width:
                obstacle_x = WIDTH

            # Check collision
            if (mario_x < obstacle_x + obstacle_width and
                mario_x + mario_width > obstacle_x and
                mario_y < obstacle_y + obstacle_height and
                mario_y + mario_height > obstacle_y):
                game_over = True

        # Update display
        pygame.display.flip()

if __name__ == "__main__":
    main()