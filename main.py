import pygame
import sys
import random

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
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Mario character properties
mario_width, mario_height = 50, 50
mario_x, mario_y = 100, HEIGHT - mario_height - 50
mario_speed = 5
jump_height = 15
is_jumping = False
velocity_y = 0

# Load Mario image
mario_image = pygame.image.load('mario_image.png')
mario_image = pygame.transform.scale(mario_image, (mario_width, mario_height))

# Gravity
gravity = 0.8

# Ground properties
ground_height = 50

# Obstacle properties
obstacle_width, obstacle_height = 40, 40
obstacle_x = WIDTH
obstacle_y = HEIGHT - ground_height - obstacle_height
obstacle_speed = 5

def draw_ground():
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - ground_height, WIDTH, ground_height))

def draw_mario(x, y):
    screen.blit(mario_image, (x, y))

def draw_obstacle(x, y):
    pygame.draw.rect(screen, RED, (x, y, obstacle_width, obstacle_height))

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
    mario_y = HEIGHT - mario_height - ground_height
    is_jumping = False
    velocity_y = 0
    obstacle_x = WIDTH

def main():
    global mario_x, mario_y, is_jumping, velocity_y, obstacle_x

    running = True
    game_over = False

    while running:
        screen.fill(BLUE)  # Clear the screen with a sky-blue background
        draw_ground()

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
            draw_obstacle(obstacle_x, obstacle_y)

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
                if mario_y >= HEIGHT - mario_height - ground_height:
                    mario_y = HEIGHT - mario_height - ground_height
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
        clock.tick(FPS)

if __name__ == "__main__":
    main()