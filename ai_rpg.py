import pygame
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
MAP_WIDTH, MAP_HEIGHT = 1600, 1200
BEACH_COLOR = (255, 215, 0)
GRASS_COLOR = (0, 255, 0)
ENEMY_SIZE = 50
PROJECTILE_SIZE = 10
PROJECTILE_SPEED = 0.1

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the player
player = pygame.Rect(WIDTH / 2, HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE)

# Set up the enemy
enemy = pygame.Rect(MAP_WIDTH / 2 + MAP_WIDTH / 4, MAP_HEIGHT / 2, ENEMY_SIZE, ENEMY_SIZE)

# Set up the projectiles
projectiles = []

# Set up the map
map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
map_surface.fill(BEACH_COLOR)
pygame.draw.rect(map_surface, GRASS_COLOR, (MAP_WIDTH / 2, 0, MAP_WIDTH / 2, MAP_HEIGHT))

# Set up the map's position
map_x, map_y = 0, 0

# Game loop
last_projectile_time = time.time()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        map_y += 0.1
    if keys[pygame.K_s]:
        map_y -= 0.1
    if keys[pygame.K_a]:
        map_x += 0.1
    if keys[pygame.K_d]:
        map_x -= 0.1

    # Shoot projectiles
    current_time = time.time()
    if current_time - last_projectile_time >= 1:
        dx = player.x - (enemy.x + map_x)
        dy = player.y - (enemy.y + map_y)
        angle = math.atan2(dy, dx)
        projectiles.append({'x': enemy.x + map_x, 'y': enemy.y + map_y, 'dx': math.cos(angle) * PROJECTILE_SPEED, 'dy': math.sin(angle) * PROJECTILE_SPEED})
        last_projectile_time = current_time

    # Move projectiles
    for projectile in projectiles:
        projectile['x'] += projectile['dx']
        projectile['y'] += projectile['dy']

    # Update projectiles based on player's position and map's position
    for projectile in projectiles:
        dx = player.x - projectile['x']
        dy = player.y - projectile['y']
        angle = math.atan2(dy, dx)
        projectile['dx'] = math.cos(angle) * PROJECTILE_SPEED
        projectile['dy'] = math.sin(angle) * PROJECTILE_SPEED

    # Draw everything
    screen.fill((0, 0, 0))
    screen.blit(map_surface, (map_x, map_y))
    pygame.draw.rect(screen, (0, 0, 0), player)
    pygame.draw.rect(screen, (255, 0, 0), (enemy.x + map_x, enemy.y + map_y, ENEMY_SIZE, ENEMY_SIZE))
    for projectile in projectiles:
        pygame.draw.rect(screen, (0, 0, 255), (projectile['x'] + map_x, projectile['y'] + map_y, PROJECTILE_SIZE, PROJECTILE_SIZE))

    # Update the display
    pygame.display.flip()