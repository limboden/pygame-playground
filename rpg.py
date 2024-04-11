import pygame
import sys
import random
from Enemy import Enemy

pygame.init()
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
BORDER_SIZE = 10
PLAYER_SPEED = 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WATER = {
    "x1": 0,
    "y1": 1800,
    'x2': 1000,
    'y2': 2000,
    'color': (0, 150, 255)
}

#holds projectiles
projectiles = []

enemy1 = pygame.Rect(400, 300, 30, 30)

map_elements = [
    [pygame.Rect(WATER['x1'], WATER['y1'], WATER['x2'], WATER['y2']), WATER['color']],
    [pygame.Rect(0, 0, 1000, 1000), (0, 255, 0)],  # Green for grass
    [pygame.Rect(1000, 0, 500, 1000), (139, 69, 19)], # Brown for dirt
]

#creating randomly generated grass in the grass area.
#currently between 0,0 and 1000, 1000
GRASS_SIZE = 20
GRASS_COLOR = (0, 200, 0)
for _ in range(0, 100): #number of grass
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    map_elements.append([pygame.Rect(x, y, GRASS_SIZE, GRASS_SIZE), GRASS_COLOR])


map_entities = [
    [enemy1, (255,0,0)]
]



image = pygame.image.load('sand2.jpg')
        
image_x = 0
image_y = 1000
original_width = original_height = 512 
new_width = int(original_width * 0.25)
new_height = int(original_height * 0.25)

resized_image = pygame.transform.scale(image, (new_width, new_height))

player = pygame.Rect(WIDTH / 2, HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE)
offset_x = 0
offset_y = -1300 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if player.colliderect((0, 1800),(1000,2000)):
        PLAYER_SPEED = 3
    else:
        PLAYER_SPEED = 5
    
    if keys[pygame.K_w]:
        offset_y += PLAYER_SPEED
    if keys[pygame.K_s]:
        offset_y -= PLAYER_SPEED
    if keys[pygame.K_a]:
        offset_x += PLAYER_SPEED
    if keys[pygame.K_d]:
        offset_x -= PLAYER_SPEED

    # Make the enemy shoot every second
    if random.random() < 1/60: 
        projectile = pygame.Rect(enemy1.x, enemy1.y, 10, 10)
        dx = (player.centerx - projectile.centerx) * 0.05
        dy = (player.centery - projectile.centery) * 0.05
        projectiles.append([projectile, [dx, dy]])

    map_all = map_elements + map_entities

    screen.fill((0, 0, 0))
    for element in map_all:
        pygame.draw.rect(screen, element[1], element[0].move(offset_x, offset_y))

    total_len = 1000
    total_height = 800
    temp_x = 0
    temp_y = 0
    while total_height > temp_y:
        while total_len > temp_x:
            screen.blit(resized_image, (image_x + temp_x + offset_x, image_y + temp_y + offset_y))
            temp_x += 128
        temp_y += 128
        temp_x = 0

    # Move and draw projectiles
    for i, (projectile, direction) in enumerate(projectiles):
        projectile.move_ip(direction)
        pygame.draw.rect(screen, (255, 0, 0), projectile.move(offset_x, offset_y))

        # Check collision with player
        if projectile.colliderect(player):
            print("Player hit!")
            #del projectiles[i]

    pygame.draw.rect(screen, (255, 255, 255), player)

    pygame.display.flip()
    clock.tick(60)
