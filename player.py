import pygame

class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y