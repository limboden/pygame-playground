import pygame
from map import Map
import sys
import random




class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.PLAYER_SIZE = 50
        self.BORDER_SIZE = 10
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.map_elements = [
            [Map(0, 0, 1000, 1000), (0, 255, 0)],  # Green for grass
            [Map(1000, 0, 500, 1000), (139, 69, 19)],  # Brown for dirt
            [Map(1500, 0, 500, 1000), (0, 0, 255)],  # Blue for water
        ]

        #creating randomly generated grass in the grass area.
        #currently between 0,0 and 1000, 1000
        GRASS_SIZE = 20
        GRASS_COLOR = (0, 200, 0)
        for _ in range(0, 100): #number of grass
          x = random.randint(0, 1000)
          y = random.randint(0, 1000)
          self.map_elements.append([Map(x, y, GRASS_SIZE, GRASS_SIZE), GRASS_COLOR])



        self.player = pygame.Rect(self.WIDTH / 2, self.HEIGHT / 2, self.PLAYER_SIZE, self.PLAYER_SIZE)
        self.offset_x = 0
        self.offset_y = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.offset_y += 5
        if keys[pygame.K_s]:
            self.offset_y -= 5
        if keys[pygame.K_a]:
            self.offset_x += 5
        if keys[pygame.K_d]:
            self.offset_x -= 5

    def draw(self):
        self.screen.fill((0, 0, 0))
        for element in self.map_elements:
            pygame.draw.rect(self.screen, element[1], element[0].rect.move(self.offset_x, self.offset_y))
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
