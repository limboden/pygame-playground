import pygame
import sys


# Initialize Pygame
pygame.init()

# Set the window size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the image
image = pygame.image.load('sand2.jpg')

# Set the image's position
image_x = 100
image_y = 100

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the image
    screen.blit(image, (image_x, image_y))

    # Update the display
    pygame.display.flip()
