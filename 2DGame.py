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

            # Add an "Exit" button
            exit_text = font.render('Exit', 1, (255, 255, 255))
            exit_text_rect = exit_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
            exit_button_rect = exit_text_rect.inflate(20, 20)

            # Check for mouse click on the buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    if health > 0:
                        level += 1
                    else:
                        level = 1
                    health = 25
                    projectiles = []
                    timer = 60
                elif exit_button_rect.collidepoint(event.pos):
                    main_menu()

            # Draw the buttons
            pygame.draw.rect(SCREEN, (200, 200, 200), text_rect.inflate(20, 20))
            SCREEN.blit(text, text_rect)
            pygame.draw.rect(SCREEN, (200, 200, 200), exit_button_rect)
            SCREEN.blit(exit_text, exit_text_rect)
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
    CIRCLE_RADIUS = 20
    CROSS_HAIR_SIZE = 20
    PROJECTILE_SIZE = 15
    PROJECTILE_SPEED = 2

    # Set up the display
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set up the rectangle
    RECT = pygame.Rect(WIDTH / 2, HEIGHT / 2, 40, 40)

    # Set up the circle
    circle_x = random.randint(0, WIDTH)
    circle_y = random.randint(0, HEIGHT)

    # Set up the exit button
    font = pygame.font.Font(None, 36)
    exit_text = font.render('Exit', 1, (255, 255, 255))
    exit_text_rect = exit_text.get_rect(topright=(WIDTH - 10, 10))
    exit_button_rect = exit_text_rect.inflate(20, 20)

    # Set up the projectiles
    projectiles = []

    # Set up the firing rate
    fire_rate = 100  # 10 game loops
    last_fire = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and exit_button_rect.collidepoint(event.pos):
                main_menu()

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

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

        # Fire projectiles
        if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - last_fire >= fire_rate:
            last_fire = pygame.time.get_ticks()
            angle = math.atan2(mouse_y - RECT.centery, mouse_x - RECT.centerx)
            projectiles.append([RECT.centerx, RECT.centery, math.cos(angle) * PROJECTILE_SPEED, math.sin(angle) * PROJECTILE_SPEED])

        # Move the projectiles
        for i, projectile in enumerate(projectiles):
            projectile[0] += projectile[2]
            projectile[1] += projectile[3]
            if projectile[0] < 0 or projectile[0] > WIDTH or projectile[1] < 0 or projectile[1] > HEIGHT:
                del projectiles[i]

        # Fill the screen with darker green
        SCREEN.fill((0, 100, 0))

        # Draw the rectangle (blue)
        pygame.draw.rect(SCREEN, (0, 0, 255), RECT)

        # Draw the circle (red)
        pygame.draw.circle(SCREEN, (255, 0, 0), (circle_x, circle_y), CIRCLE_RADIUS)

        # Draw the cross hair (white)
        pygame.draw.line(SCREEN, (255, 255, 255), (mouse_x - CROSS_HAIR_SIZE, mouse_y), (mouse_x + CROSS_HAIR_SIZE, mouse_y))
        pygame.draw.line(SCREEN, (255, 255, 255), (mouse_x, mouse_y - CROSS_HAIR_SIZE), (mouse_x, mouse_y + CROSS_HAIR_SIZE))

        # Draw the projectiles (blue)
        for projectile in projectiles:
            pygame.draw.rect(SCREEN, (0, 0, 255), pygame.Rect(projectile[0], projectile[1], PROJECTILE_SIZE, PROJECTILE_SIZE))

        # Draw the exit button
        pygame.draw.rect(SCREEN, (200, 200, 200), exit_button_rect)
        SCREEN.blit(exit_text, exit_text_rect)

        # Flip the display
        pygame.display.flip()



if __name__ == '__main__':
    main_menu()

