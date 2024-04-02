import pygame
import sys

# Game Variables
gravity = 0.75
jump_height = 20

# Player Properties
player_size = 50
player_pos = [50, 50]
player_vel = [0, 0]
is_jumping = False

# Platform Properties
platforms = [
    {"x": 0, "y": 550, "w": 800, "h": 50},
    {"x": 200, "y": 400, "w": 200, "h": 50},
    {"x": 500, "y": 300, "w": 100, "h": 50},
    {"x": 700, "y": 200, "w": 50, "h": 50},
]

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_vel[1] -= jump_height
                is_jumping = True

    # Move Player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] -= 5
    if keys[pygame.K_d]:
        player_pos[0] += 5

    player_pos[1] += player_vel[1]

    # Apply Gravity
    player_vel[1] += gravity

    # Collision with Platforms
    for platform in platforms:
        if (player_pos[1] + player_size > platform["y"] and
            player_pos[1] < platform["y"] + platform["h"] and
            player_pos[0] + player_size > platform["x"] and
            player_pos[0] < platform["x"] + platform["w"]):
            player_pos[1] = platform["y"] - player_size
            player_vel[1] = 0
            is_jumping = False

    # Keep Player on Screen
    if player_pos[1] > screen.get_height() - player_size:
        player_pos[1] = screen.get_height() - player_size
        player_vel[1] = 0

    # Draw Everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (player_pos[0], player_pos[1], player_size, player_size))

    for platform in platforms:
        pygame.draw.rect(screen, (255, 255, 255), (platform["x"], platform["y"], platform["w"], platform["h"]))

    pygame.display.flip()

    # Cap at 60 FPS
    clock.tick(60)
