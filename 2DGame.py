import pygame
import sys
import math
import random

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 72)
    just_dodge_text = font.render('Just Dodge!', 1, (0, 0, 255))  # Blue color
    just_dodge_text_rect = just_dodge_text.get_rect(center=(400, 200))
    just_dodge_button_rect = just_dodge_text_rect.inflate(20, 20)
    shooting_range_text = font.render('Shooting Range', 1, (0, 0, 255))  # Blue color
    shooting_range_text_rect = shooting_range_text.get_rect(center=(400, 350))
    shooting_range_button_rect = shooting_range_text_rect.inflate(20, 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and just_dodge_button_rect.collidepoint(event.pos):
                just_dodge()
            elif event.type == pygame.MOUSEBUTTONDOWN and shooting_range_button_rect.collidepoint(event.pos):
                shooting_range()

        screen.fill((0, 100, 0))  # Darker green color
        pygame.draw.rect(screen, (200, 200, 200), just_dodge_button_rect)
        screen.blit(just_dodge_text, just_dodge_text_rect)
        pygame.draw.rect(screen, (200, 200, 200), shooting_range_button_rect)
        screen.blit(shooting_range_text, shooting_range_text_rect)
        pygame.display.flip()


def just_dodge():
    # Initialize Pygame
    pygame.init()

    # Set up some constants
    WIDTH, HEIGHT = 1280, 960
    SPEED = 1
    PROJECTILE_SIZE = 10

    # Set up the display
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set up the rectangle
    RECT = pygame.Rect(WIDTH / 2, HEIGHT / 2, 40, 40)

    # Set up the projectiles
    projectiles = []

    # Set up the health
    health = 25

    # Set up the timer
    timer = 60

    # Game loop
    level = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get a list of all keys currently being pressed down
        keys = pygame.key.get_pressed()

        # Move the rectangle based on the keys
        if keys[pygame.K_w]:
            RECT.y -= SPEED
            if RECT.y < 0:
                RECT.y = 0
        if keys[pygame.K_a]:
            RECT.x -= SPEED
            if RECT.x < 0:
                RECT.x = 0
        if keys[pygame.K_s]:
            RECT.y += SPEED
            if RECT.y > HEIGHT - RECT.height:
                RECT.y = HEIGHT - RECT.height
        if keys[pygame.K_d]:
            RECT.x += SPEED
            if RECT.x > WIDTH - RECT.width:
                RECT.x = WIDTH - RECT.width

        # Add a new projectile occasionally
        if random.random() < 0.05 * level:
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                x = random.randint(0, WIDTH)
                y = 0
                angle = random.uniform(-math.pi / 2, math.pi / 2)
            elif side == 'bottom':
                x = random.randint(0, WIDTH)
                y = HEIGHT
                angle = random.uniform(math.pi / 2, math.pi * 3 / 2)
            elif side == 'left':
                x = 0
                y = random.randint(0, HEIGHT)
                angle = random.uniform(math.pi, math.pi * 2)
            elif side == 'right':
                x = WIDTH
                y = random.randint(0, HEIGHT)
                angle = random.uniform(0, math.pi)
            speed = random.uniform(0.5 * level/3, 2 * level/3)  # Increase speed with level
            projectiles.append([x, y, math.cos(angle) * speed, math.sin(angle) * speed])

        # Move the projectiles
        for i, projectile in enumerate(projectiles):
            projectile[0] += projectile[2]
            projectile[1] += projectile[3]
            if projectile[0] < 0 or projectile[0] > WIDTH or projectile[1] < 0 or projectile[1] > HEIGHT:
                del projectiles[i]

        # Check for collisions with the rectangle
        for i, projectile in enumerate(projectiles):
            projectile_rect = pygame.Rect(projectile[0], projectile[1], PROJECTILE_SIZE, PROJECTILE_SIZE)
            if RECT.colliderect(projectile_rect):
                del projectiles[i]
                health -= 1

        # Check for game over
        if health <= 0 or timer <= 0:
            SCREEN.fill((0, 0, 0))
            font = pygame.font.Font(None, 72)
            if health > 0:
                text = font.render('YOU WIN', 1, (255, 255, 255))
            else:
                text = font.render('GAME OVER', 1, (255, 0, 0))
            SCREEN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

            # Add a "Try Again" or "Next Level" button
            font = pygame.font.Font(None, 36)
            if health > 0:
                text = font.render('Next Level', 1, (255, 255, 255))
            else:
                text = font.render('Try Again', 1, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
            pygame.draw.rect(SCREEN, (200, 200, 200), text_rect.inflate(20, 20))
            SCREEN.blit(text, text_rect)

            # Check for mouse click on the button
            if event.type == pygame.MOUSEBUTTONDOWN and text_rect.collidepoint(event.pos):
                if health > 0:
                    level += 1
                else:
                    level = 1
                health = 25
                projectiles = []
                timer = 60
        else:
            # Fill the screen with darker green
            SCREEN.fill((0, 100, 0))

            # Draw the health
            font = pygame.font.Font(None, 36)
            text = font.render(str(health), 1, (0, 0, 0))
            SCREEN.blit(text, (10, 10))

            # Draw the timer
            font = pygame.font.Font(None, 36)
            text = font.render(str(int(timer)), 1, (0, 0, 0))
            SCREEN.blit(text, (WIDTH - 40, 10))

            # Draw the rectangle (blue)
            pygame.draw.rect(SCREEN, (0, 0, 255), RECT)

            # Draw the projectiles (red)
            for projectile in projectiles:
                pygame.draw.rect(SCREEN, (255, 0, 0), pygame.Rect(projectile[0], projectile[1], PROJECTILE_SIZE, PROJECTILE_SIZE))

            # Decrement the timer
            timer -= 1 / 240

        # Flip the display
        pygame.display.flip()


def shooting_range():
    # Initialize Pygame
    pygame.init()

    # Set up some constants
    WIDTH, HEIGHT = 1280, 960
    SPEED = 1

    # Set up the display
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set up the rectangle
    RECT = pygame.Rect(WIDTH / 2, HEIGHT / 2, 40, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get a list of all keys currently being pressed down
        keys = pygame.key.get_pressed()

        # Move the rectangle based on the keys
        if keys[pygame.K_w]:
            RECT.y -= SPEED
            if RECT.y < 0:
                RECT.y = 0
        if keys[pygame.K_a]:
            RECT.x -= SPEED
            if RECT.x < 0:
                RECT.x = 0
        if keys[pygame.K_s]:
            RECT.y += SPEED
            if RECT.y > HEIGHT - RECT.height:
                RECT.y = HEIGHT - RECT.height
        if keys[pygame.K_d]:
            RECT.x += SPEED
            if RECT.x > WIDTH - RECT.width:
                RECT.x = WIDTH - RECT.width

        # Fill the screen with darker green
        SCREEN.fill((0, 100, 0))

        # Draw the rectangle (blue)
        pygame.draw.rect(SCREEN, (0, 0, 255), RECT)

        # Flip the display
        pygame.display.flip()

if __name__ == '__main__':
    main_menu()

