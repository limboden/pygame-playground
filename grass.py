import pygame
import random
import sys
from map import Map



WIDTH, HEIGHT = 640, 480
OBJECT_SIZE = 20
OBJECT_COLOR = (50, 255, 50)  # Red
objects = []



class Grass:
    def __init__(self, x1, y1, x2, y2, count):
      self.x1 = x1
      self.y1 = y1
      self.x2 = x2
      self.y2 = y2
      self.count = count


    def produce_random_grass(self):
      for _ in range(0, self.count):
          x = random.randint(self.x1, self.x2)
          y = random.randint(self.y1, self.y2)
          objects.append([Map(x, y, x + OBJECT_SIZE, y + OBJECT_SIZE), OBJECT_COLOR])
      return objects