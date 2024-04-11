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

isFirst = True

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
    
    if isFirst: 
        offset_y = -1300
        isFirst = False
    else: offset_y = 0
    offset_x = 0



    if keys[pygame.K_w]:
        offset_y += PLAYER_SPEED
    if keys[pygame.K_s]:
        offset_y -= PLAYER_SPEED
    if keys[pygame.K_a]:
        offset_x += PLAYER_SPEED
    if keys[pygame.K_d]:
        offset_x -= PLAYER_SPEED

    map_all = map_elements + map_entities

    screen.fill((0, 0, 0))
    for element in map_all:
        element[0].x += offset_x
        element[0].y += offset_y
        top_left = [element[0].left,element[0].top]
        bottom_right = [element[0].left + element[0].width, element[0].top + element[0].height]
        if(bottom_right[0] > 0 and top_left[0] < WIDTH and bottom_right[1] > 0 and top_left[1] < HEIGHT):
            pygame.draw.rect(screen, element[1], element[0])

    total_len = 1000
    total_height = 800
    temp_x = 0
    temp_y = 0
    image_x += offset_x
    image_y += offset_y
    while total_height > temp_y:
        while total_len > temp_x:
            screen.blit(resized_image, (image_x + temp_x, image_y + temp_y))
            temp_x += 128
        temp_y += 128
        temp_x = 0
        
    print(enemy1.x)

    pygame.draw.rect(screen, (255, 255, 255), player)

    offset_x = 0
    offset_y = 0


    pygame.display.flip()
    clock.tick(60)
