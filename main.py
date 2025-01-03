import pygame
import sys
import random
from PIL import Image

# Initialize Pygame
pygame.init()

# Initialize Pygame Mixer for background music
pygame.mixer.init()

# Load background music and set it to loop indefinitely
pygame.mixer.music.load("background_music.mp3")  # Replace with your music file path
pygame.mixer.music.set_volume(0.3)  # Adjust volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)

# Mario character properties
mario_width, mario_height = 70, 70
mario_x, mario_y = 100, HEIGHT - mario_height - 107
mario_speed = 5  # Initial speed
jump_height = 15
is_jumping = False
velocity_y = 0
speed_increment_interval = 5000  # Mario speed increases every 5 seconds
last_speed_increase = 0

# Load new character images for running animation
mario_frames = [
    pygame.image.load('character 2.png'),
    pygame.image.load('character 3.png')
]
mario_frames = [pygame.transform.scale(frame, (mario_width, mario_height)) for frame in mario_frames]

# Animation properties for Mario
mario_frame_index = 0
mario_animation_speed = 0.1  # Controls how fast the frames switch
mario_timer = 0

# Load obstacle images
obstacle_images = [
    pygame.transform.scale(pygame.image.load('cactus.jpeg'), (60, 60)),
    pygame.transform.scale(pygame.image.load('obstacle2.png'), (60, 60))
]

# Load animated obstacle frames
obstacle3_frames = [
    pygame.image.load('obstacle3_1.png'),
    pygame.image.load('obstacle3_2.png')
]

# Scale animated obstacle frames
obstacle3_frames = [pygame.transform.scale(frame, (60, 60)) for frame in obstacle3_frames]

# Animation properties
obstacle3_frame_index = 0
obstacle3_animation_speed = 0.2  # Controls how fast the frames switch
obstacle3_timer = 0

# Obstacle properties
obstacle_width, obstacle_height = 30, 30
obstacle_x = WIDTH
obstacle_y = HEIGHT - obstacle_height - 120
current_obstacle_image = random.choice(obstacle_images + [obstacle3_frames])

# Score properties
score = 0
last_score_update = 0
font = pygame.font.Font(None, 36)

# Load and prepare the GIF as an animated background
gif_path = "background.gif"
gif = Image.open(gif_path)
frames = []
frame_durations = []
# Settings menu
def settings_menu():
    running = True
    volume = pygame.mixer.music.get_volume()

    while running:
        screen.fill(WHITE)  # Use a distinct background for the settings menu

        # Draw menu options
        title_text = font.render("Settings", True, BLACK)
        volume_text = font.render(f"Volume: {int(volume * 100)}%", True, BLACK)
        quit_text = font.render("Quit Game", True, BLACK)
        back_text = font.render("Back", True, BLACK)

        # Draw rectangles for buttons
        volume_up_rect = pygame.Rect(100, 150, 50, 30)
        volume_down_rect = pygame.Rect(200, 150, 50, 30)
        quit_rect = pygame.Rect(100, 200, 200, 40)
        back_rect = pygame.Rect(100, 250, 200, 40)

        # Render text and buttons
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(volume_text, (WIDTH // 2 - volume_text.get_width() // 2, 100))
        pygame.draw.rect(screen, DARK_GRAY, volume_up_rect)
        pygame.draw.rect(screen, DARK_GRAY, volume_down_rect)
        screen.blit(font.render("+", True, WHITE), (volume_up_rect.x + 15, volume_up_rect.y))
        screen.blit(font.render("-", True, WHITE), (volume_down_rect.x + 15, volume_down_rect.y))
        pygame.draw.rect(screen, DARK_GRAY, quit_rect)
        pygame.draw.rect(screen, DARK_GRAY, back_rect)
        screen.blit(quit_text, (quit_rect.x + 50, quit_rect.y + 5))
        screen.blit(back_text, (back_rect.x + 50, back_rect.y + 5))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if volume_up_rect.collidepoint(event.pos):
                    volume = min(1.0, volume + 0.1)  # Increase volume
                    pygame.mixer.music.set_volume(volume)
                elif volume_down_rect.collidepoint(event.pos):
                    volume = max(0.0, volume - 0.1)  # Decrease volume
                    pygame.mixer.music.set_volume(volume)
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif back_rect.collidepoint(event.pos):
                    running = False  # Exit settings menu

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

def draw_mario(x, y):
    global mario_frame_index, mario_timer
    mario_timer += 1 / FPS
    if mario_timer >= mario_animation_speed:
        mario_timer = 0
        mario_frame_index = (mario_frame_index + 1) % len(mario_frames)
    screen.blit(mario_frames[mario_frame_index], (x, y))

def draw_obstacle(x, y, obstacle):
    if obstacle == obstacle3_frames:
        global obstacle3_frame_index, obstacle3_timer
        obstacle3_timer += 1 / FPS
        if obstacle3_timer >= obstacle3_animation_speed:
            obstacle3_timer = 0
            obstacle3_frame_index = (obstacle3_frame_index + 1) % len(obstacle3_frames)
        screen.blit(obstacle3_frames[obstacle3_frame_index], (x, y))
    else:
        screen.blit(obstacle, (x, y))

def draw_score(score):
    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

def reset_obstacle():
    global obstacle_x, current_obstacle_image
    obstacle_x = WIDTH
    current_obstacle_image = random.choice(obstacle_images + [obstacle3_frames])

def show_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, BLACK)
    restart_text = pygame.font.Font(None, 36).render("Press SPACE to Restart", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()

def show_start_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("Press SPACE to Start", True, BLACK)
    alpha = 0
    increment = 5
    fading_in = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        screen.fill(WHITE)
        text_surface = font.render("Press SPACE to Start", True, BLACK)
        temp_surface = text_surface.copy()
        temp_surface.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(temp_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 50))

        if fading_in:
            alpha += increment
            if alpha >= 255:
                alpha = 255
                fading_in = False
        else:
            alpha -= increment
            if alpha <= 0:
                alpha = 0
                fading_in = True

        pygame.display.flip()
        pygame.time.delay(30)

def reset_game():
    global mario_x, mario_y, is_jumping, velocity_y, mario_speed, last_speed_increase, score, last_score_update, obstacle_x
    mario_x = 100
    mario_y = HEIGHT - mario_height - 107
    is_jumping = False
    velocity_y = 0
    mario_speed = 5
    last_speed_increase = pygame.time.get_ticks()
    score = 0
    last_score_update = pygame.time.get_ticks()
    obstacle_x = WIDTH

def main():
    global mario_x, mario_y, is_jumping, velocity_y, mario_speed, last_speed_increase, obstacle_x, score, last_score_update, current_frame, frame_timer

    show_start_screen()

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
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game_over = False
                        reset_game()
                        waiting = False
        else:
            draw_mario(mario_x, mario_y)
            draw_obstacle(obstacle_x, obstacle_y, current_obstacle_image)
            draw_score(score)

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
                if mario_y >= HEIGHT - mario_height - 107:
                    mario_y = HEIGHT - mario_height - 107
                    is_jumping = False

                       # Prevent Mario from going out of bounds
            mario_x = max(0, min(WIDTH - mario_width, mario_x))

            # Move obstacle
            obstacle_x -= mario_speed
            if obstacle_x < -obstacle_width:  # Reset obstacle if it moves out of the screen
                reset_obstacle()

            # Mario speed and score increment logic
            current_time = pygame.time.get_ticks()
            if current_time - last_speed_increase > speed_increment_interval:
                mario_speed += 0.5  # Increase Mario's speed
                last_speed_increase = current_time

            if current_time - last_score_update > 100:
                score += mario_speed * 0.1  # Increase score based on Mario's speed
                last_score_update = current_time

            # Check collision
            if (mario_x < obstacle_x + obstacle_width and
                mario_x + mario_width > obstacle_x and
                mario_y < obstacle_y + obstacle_height and
                mario_y + mario_height > obstacle_y):
                game_over = True
                # Draw settings button
        settings_rect = pygame.Rect(10, 10, 140, 40)  # Move to the top-left corner
        pygame.draw.rect(screen, DARK_GRAY, settings_rect)
        settings_text = font.render("Settings", True, WHITE)
        screen.blit(settings_text, (settings_rect.x + 25, settings_rect.y + 5))
          # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if settings_rect.collidepoint(event.pos):
                    settings_menu()
        # Update display
        pygame.display.flip()

if __name__ == "__main__":
    main()

