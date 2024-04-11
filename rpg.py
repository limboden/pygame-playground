import pygame
from map import Map
import sys
import random
from Enemy import Enemy



class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.PLAYER_SIZE = 50
        self.BORDER_SIZE = 10
        self.PLAYER_SPEED = 5
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.WATER = {
            "x1": 0, 
            "y1": 1800, 
            'x2': 1000, 
            'y2': 2000, 
            'color': (0, 150, 255)
        }

        #holds projectiles
        self.projectiles = []

        self.enemy1 = Enemy(400, 1000, 30)
        self.enemy1mapped = Map(self.enemy1.x, self.enemy1.y, self.enemy1.size, self.enemy1.size)


        self.map_elements = [
            [Map(self.WATER['x1'],self.WATER['y1'],self.WATER['x2'],self.WATER['y2']), self.WATER['color']],
            [Map(0, 0, 1000, 1000), (0, 255, 0)],  # Green for grass
            [Map(1000, 0, 500, 1000), (139, 69, 19)], # Brown for dirt
            [self.enemy1mapped, (0,0,255)]  
        ]

        #creating randomly generated grass in the grass area.
        #currently between 0,0 and 1000, 1000
        GRASS_SIZE = 20
        GRASS_COLOR = (0, 200, 0)
        for _ in range(0, 100): #number of grass
          x = random.randint(0, 1000)
          y = random.randint(0, 1000)
          self.map_elements.append([Map(x, y, GRASS_SIZE, GRASS_SIZE), GRASS_COLOR])

        self.image = pygame.image.load('sand2.jpg')
        
        self.image_x = 0
        self.image_y = 1000
        original_width = original_height = 512 
        # Calculate the new width and height while maintaining the aspect ratio
        new_width = int(original_width * 0.25)
        new_height = int(original_height * 0.25)

        # Resize the image
        self.resized_image = pygame.transform.scale(self.image, (new_width, new_height))


        self.player = pygame.Rect(self.WIDTH / 2, self.HEIGHT / 2, self.PLAYER_SIZE, self.PLAYER_SIZE)
        self.offset_x = 0 #this is just default
        self.offset_y = -1300 #this is to make sure we spawn at the beach

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.PLAYER_SPEED = 5
        if(self.player.colliderect((0, 1800),(1000,2000))):
            self.PLAYER_SPEED = 3
        print(self.PLAYER_SPEED)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.offset_y += self.PLAYER_SPEED
        if keys[pygame.K_s]:
            self.offset_y -= self.PLAYER_SPEED
        if keys[pygame.K_a]:
            self.offset_x += self.PLAYER_SPEED
        if keys[pygame.K_d]:
            self.offset_x -= self.PLAYER_SPEED

    def draw(self):
        self.screen.fill((0, 0, 0))
        for element in self.map_elements:
            pygame.draw.rect(self.screen, element[1], element[0].rect.move(self.offset_x, self.offset_y))
        
        # Draw the image
        total_len = 1000
        total_height = 800
        temp_x = 0
        temp_y = 0

        while total_height > temp_y:
            while total_len > temp_x:
                self.screen.blit(self.resized_image, (self.image_x + temp_x + self.offset_x, self.image_y + temp_y + self.offset_y))
                temp_x += 128
            temp_y += 128
            temp_x = 0

        # Draw the enemy rectangle
        pygame.draw.rect(self.screen, (255,0,0), (self.enemy1.x, self.enemy1.y, self.enemy1.size, self.enemy1.size))



        pygame.draw.rect(self.screen, (255, 255, 255), self.player)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
