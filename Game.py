import pygame
from player import Player
from map import Map
import sys

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.map = Map()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.update()
            self.map.update(self.player.offset_x, self.player.offset_y)

            self.screen.fill((0, 0, 0))
            self.map.draw(self.screen)
            self.player.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
