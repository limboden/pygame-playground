import pygame
import sys
import math
import random
import rpg



def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((1280, 960))
    font = pygame.font.Font(None, 72)
    just_dodge_text = font.render('Just Dodge!', 1, (0, 0, 255))  # Blue color
    just_dodge_text_rect = just_dodge_text.get_rect(center=(400, 200))
    just_dodge_button_rect = just_dodge_text_rect.inflate(20, 20)

    shooting_range_text = font.render('Shooting Range', 1, (0, 0, 255))  # Blue color
    shooting_range_text_rect = shooting_range_text.get_rect(center=(400, 350))
    shooting_range_button_rect = shooting_range_text_rect.inflate(20, 20)

    
    platformer_text = font.render('Platformer', 1, (0, 0, 255))  # Blue
    platformer_text_rect = platformer_text.get_rect(center=(400, 500))
    platformer_button_rect = platformer_text_rect.inflate(20, 20)

    rpg_text = font.render('RPG', 1, (0, 0, 255))  # Blue
    rpg_text_rect = rpg_text.get_rect(center=(400, 650))
    rpg_button_rect = rpg_text_rect.inflate(20, 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and just_dodge_button_rect.collidepoint(event.pos):
                just_dodge()
            elif event.type == pygame.MOUSEBUTTONDOWN and shooting_range_button_rect.collidepoint(event.pos):
                shooting_range()
            elif event.type == pygame.MOUSEBUTTONDOWN and platformer_button_rect.collidepoint(event.pos):
                platformer()
            elif event.type == pygame.MOUSEBUTTONDOWN and rpg_button_rect.collidepoint(event.pos):
                rpg()


        screen.fill((0, 100, 0))  # Darker green color
        pygame.draw.rect(screen, (200, 200, 200), just_dodge_button_rect)
        screen.blit(just_dodge_text, just_dodge_text_rect)
        pygame.draw.rect(screen, (200, 200, 200), shooting_range_button_rect)
        screen.blit(shooting_range_text, shooting_range_text_rect)
        pygame.draw.rect(screen, (200, 200, 200), platformer_button_rect)
        screen.blit(platformer_text, platformer_text_rect)#for platformer
        pygame.draw.rect(screen, (200, 200, 200), rpg_button_rect)
        screen.blit(rpg_text, rpg_text_rect)#for platformer
        pygame.display.flip()


def just_dodge():
    # Initialize Pygame
    pygame.init()

    # Set up some constants
    WIDTH, HEIGHT = 1280, 960
    SPEED = 1
    PROJECTILE_SIZE = 10
    HEALTH_PACK_SIZE = 20

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

    # Set up the health packs
    health_packs = []
    health_pack_timer = 0

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
        if random.random() < 0.08 + 0.04 * level:
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
            speed = random.uniform(0.5 * (level/10), 1.5 * (level/10))  # Increase speed with level
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

        # Add health packs
        if health_pack_timer <= 0:
            health_pack_x = random.randint(0, WIDTH)
            health_pack_y = random.randint(0, HEIGHT)
            health_packs.append([health_pack_x, health_pack_y])
            health_pack_timer = 100  # Reset the timer

        # Check for health pack pickup
        for i, health_pack in enumerate(health_packs):
            health_pack_rect = pygame.Rect(health_pack[0], health_pack[1], PROJECTILE_SIZE, PROJECTILE_SIZE)
            if RECT.colliderect(health_pack_rect):
                del health_packs[i]
                health += 10
                if health > 25:
                    health = 25

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

            # Draw the health packs
            for health_pack in health_packs:
                pygame.draw.rect(SCREEN, (0, 255, 0), pygame.Rect(health_pack[0], health_pack[1], HEALTH_PACK_SIZE, HEALTH_PACK_SIZE))

            # Decrement the timer
            timer -= 1 / 240
            health_pack_timer -= 1 / 240

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
    MIN_WEAPON_DMG = 10
    MAX_WEAPON_DMG = 20

    # Set up the display
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set up the rectangle
    RECT = pygame.Rect(WIDTH / 2, HEIGHT / 2, 40, 40)

    # Set up the circle
    circle_x = random.randint(WIDTH // 10, WIDTH - WIDTH // 10)
    circle_y = random.randint(HEIGHT // 10, HEIGHT - HEIGHT // 10)
    circle_health = random.randint(100, 500)

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

    # Set up the targets' projectiles
    target_projectiles = []

    # Set up the player health
    player_health = 100

    # Set up the score
    score = 0

        # Set up the weapons
    weapons = {
        'SMG': {'fire_rate': 2, 'damage': 0.5},
        'Rifle': {'fire_rate': 0.5, 'damage': 2}
    }

    # Set up the current weapon
    current_weapon = 'SMG'

    # Set up the weapon buttons
    weapon_buttons = {
        'SMG': {'rect': pygame.Rect(10, 10, 100, 50), 'text': font.render('SMG', 1, (255, 255, 255))},
        'Rifle': {'rect': pygame.Rect(120, 10, 100, 50), 'text': font.render('Rifle', 1, (255, 255, 255))}
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for weapon, button in weapon_buttons.items():
                    if button['rect'].collidepoint(event.pos):
                        current_weapon = weapon
                        fire_rate = weapons[weapon]['fire_rate']
                        damage = weapons[weapon]['damage']


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
            else:
                projectile_rect = pygame.Rect(projectile[0], projectile[1], PROJECTILE_SIZE, PROJECTILE_SIZE)
                if projectile_rect.colliderect(pygame.Rect(circle_x, circle_y, CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2)):
                    damage = random.randint(MIN_WEAPON_DMG, MAX_WEAPON_DMG)
                    circle_health -= damage
                    del projectiles[i]
                    score += 1

        # Move the targets' projectiles
        for i, projectile in enumerate(target_projectiles):
            projectile[0] += projectile[2]
            projectile[1] += projectile[3]
            if projectile[0] < 0 or projectile[0] > WIDTH or projectile[1] < 0 or projectile[1] > HEIGHT:
                del target_projectiles[i]
            else:
                projectile_rect = pygame.Rect(projectile[0], projectile[1], PROJECTILE_SIZE, PROJECTILE_SIZE)
                if projectile_rect.colliderect(RECT):
                    # Handle collision with the player
                    player_health -= 10
                    del target_projectiles[i]

        # Make the targets shoot back
        if random.random() < 0.01:  # 1% chance to shoot each game loop
            angle = math.atan2(RECT.centery - circle_y, RECT.centerx - circle_x)
            target_projectiles.append([circle_x, circle_y, math.cos(angle) * PROJECTILE_SPEED, math.sin(angle) * PROJECTILE_SPEED])

        # Respawn the circle if its health is 0
        if circle_health <= 0:
            circle_x = random.randint(WIDTH // 10, WIDTH - WIDTH // 10)
            circle_y = random.randint(HEIGHT // 10, HEIGHT - HEIGHT // 10)
            circle_health = random.randint(100, 500)

            # Draw the weapon buttons
        for weapon, button in weapon_buttons.items():
            pygame.draw.rect(SCREEN, (200, 200, 200), button['rect'])
            SCREEN.blit(button['text'], button['rect'].move(10, 10))

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
            else:
                projectile_rect = pygame.Rect(projectile[0], projectile[1], PROJECTILE_SIZE, PROJECTILE_SIZE)
                if projectile_rect.colliderect(pygame.Rect(circle_x, circle_y, CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2)):
                    damage = random.randint(MIN_WEAPON_DMG, MAX_WEAPON_DMG) * damage
                    circle_health -= damage
                    del projectiles[i]
                    score += 1

            # Check for game over
            if player_health <= 0:
                # Game over screen
                SCREEN.fill((0, 0, 0))
                font = pygame.font.Font(None, 72)
                text = font.render('GAME OVER', 1, (255, 0, 0))
                SCREEN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
                font = pygame.font.Font(None, 36)
                text = font.render(f'Score: {score}', 1, (255, 255, 255))
                SCREEN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 + 50))
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds
                main_menu()

        # Fill the screen with darker green
        SCREEN.fill((0, 100, 0))

        # Draw the rectangle (blue)
        pygame.draw.rect(SCREEN, (0, 0, 255), RECT)

        # Draw the circle (red)
        pygame.draw.circle(SCREEN, (255, 0, 0), (circle_x, circle_y), CIRCLE_RADIUS)

        # Draw the circle's health
        font = pygame.font.Font(None, 36)
        health_text = font.render(f'Health: {circle_health}', 1, (255, 255, 255))
        SCREEN.blit(health_text, (circle_x, circle_y + CIRCLE_RADIUS + 10))

        # Draw the player's health
        font = pygame.font.Font(None, 36)
        health_text = font.render(f'Health: {player_health}', 1, (255, 255, 255))
        SCREEN.blit(health_text, (10, 10))

        # Draw the cross hair (white)
        pygame.draw.line(SCREEN, (255, 255, 255), (mouse_x - CROSS_HAIR_SIZE, mouse_y), (mouse_x + CROSS_HAIR_SIZE, mouse_y))
        pygame.draw.line(SCREEN, (255, 255, 255), (mouse_x, mouse_y - CROSS_HAIR_SIZE), (mouse_x, mouse_y + CROSS_HAIR_SIZE))

        # Draw the projectiles (blue)
        for projectile in projectiles:
            pygame.draw.rect(SCREEN, (0, 0, 255), pygame.Rect(projectile[0], projectile[1], PROJECTILE_SIZE, PROJECTILE_SIZE))

        # Draw the targets' projectiles
        for projectile in target_projectiles:
            pygame.draw.rect(SCREEN, (255, 0, 0), pygame.Rect(projectile[0], projectile[1], PROJECTILE_SIZE, PROJECTILE_SIZE))

        # Draw the exit button
        pygame.draw.rect(SCREEN, (200, 200, 200), exit_button_rect)
        SCREEN.blit(exit_text, exit_text_rect)

        # Flip the display
        pygame.display.flip()





def platformer():




    gravity = 0.75
    jump_height = 20

    # Player Properties
    player_size = 50
    player_pos = [50, 1050]  # Start at the bottom of the screen
    player_vel = [0, 0]
    is_jumping = False

    # Platform Properties
    platforms = [

    
    
    [
    {"x": 0, "y": 1100, "w": 800, "h": 20},
    {"x": 100, "y": 900, "w": 200, "h": 20},
    {"x": 400, "y": 900, "w": 200, "h": 20},
    {"x": 200, "y": 700, "w": 200, "h": 20},
    {"x": 600, "y": 700, "w": 200, "h": 20},
    {"x": 300, "y": 500, "w": 200, "h": 20},
    {"x": 700, "y": 500, "w": 200, "h": 20},
    {"x": 400, "y": 300, "w": 200, "h": 20},
    {"x": 600, "y": 100, "w": 200, "h": 20},
],
    
    [
    {"x": 200, "y": 1000, "w": 200, "h": 20},
    {"x": 400, "y": 700, "w": 200, "h": 20},
    {"x": 600, "y": 500, "w": 200, "h": 20},
    {"x": 200, "y": 300, "w": 200, "h": 20},
    {"x": 400, "y": 100, "w": 200, "h": 20},
], 

[ 
    {"x": 200, "y": 1000, "w": 200, "h": 20},
    {"x": 500, "y": 700, "w": 200, "h": 20},
    {"x": 100, "y": 500, "w": 200, "h": 20},
    {"x": 300, "y": 300, "w": 200, "h": 20},
    {"x": 600, "y": 100, "w": 200, "h": 20},
], 

[
    {"x": 150, "y": 1000, "w": 200, "h": 20},
    {"x": 0, "y": 700, "w": 200, "h": 20},
    {"x": 0, "y": 500, "w": 200, "h": 20},
    {"x": 0, "y": 400, "w": 300, "h": 20},
    {"x": 680, "y": 700, "w": 120, "h": 20},
    {"x": 650, "y": 500, "w": 150, "h": 20},
    {"x": 600, "y": 300, "w": 200, "h": 20},
    {"x": 600, "y": 100, "w": 200, "h": 20},
]
    
    ]
    
    level = 0
    # Pygame Initialization
    pygame.init()
    screen = pygame.display.set_mode((800, 1200))  # Make the window taller
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    player_vel[1] -= jump_height
                    is_jumping = True

        # Move Player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_pos[0] -= 5
        if keys[pygame.K_d]:
            player_pos[0] += 5

        player_pos[1] += player_vel[1]

        # Apply Gravity
        player_vel[1] += gravity

        # Collision with Platforms
        for platform in platforms[level]:
            if (player_pos[1] + player_size > platform["y"] and
                player_pos[1] < platform["y"] + platform["h"] and
                player_pos[0] + player_size > platform["x"] and
                player_pos[0] < platform["x"] + platform["w"]):
                player_pos[1] = platform["y"] - player_size
                player_vel[1] = 0
                is_jumping = False

        # Keep Player on Screen    
        if player_pos[1] < 1:
            player_pos[1] = screen.get_height() - player_size
            level += 1

        if player_pos[1] > 1200:
            player_pos[1] = 1
            level -= 1

        # Draw Everything
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (player_pos[0], player_pos[1], player_size, player_size))

        for platform in platforms[level]:
            pygame.draw.rect(screen, (255, 255, 255), (platform["x"], platform["y"], platform["w"], platform["h"]))

            

        pygame.display.flip()

        # Cap at 60 FPS
        clock.tick(60)


def rpg():
    # Initialize Pygame
    pygame.init()

    # Set up some constants
    WIDTH, HEIGHT = 800, 600
    PLAYER_SIZE = 50
    BORDER_SIZE = 10  # Thickness of the border

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set up the clock
    clock = pygame.time.Clock()

    # Set up the map
    map = pygame.Rect(0, 0, 2000, 2000)
    grass = pygame.Rect(0, 0, 1000, 1000)
    dirt = pygame.Rect(1000, 0, 500, 1000)
    water = pygame.Rect(1500, 0, 500, 1000)

    # Set up the player
    player = pygame.Rect(WIDTH / 2, HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE)

    # Set up the offset
    offset_x = 0
    offset_y = 0

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get a list of all keys currently being pressed down
        keys = pygame.key.get_pressed()

        # Player movement
        if keys[pygame.K_w]:
            offset_y += 5
        if keys[pygame.K_s]:
            offset_y -= 5
        if keys[pygame.K_a]:
            offset_x += 5
        if keys[pygame.K_d]:
            offset_x -= 5

        # Check for collision with the border
        if player.x - BORDER_SIZE <= 0:
            if keys[pygame.K_a]:
                offset_x = 0
        if player.x + player.width + BORDER_SIZE >= WIDTH:
            if keys[pygame.K_d]:
                offset_x = 0
        if player.y - BORDER_SIZE <= 0:
            if keys[pygame.K_w]:
                offset_y = 0
        if player.y + player.height + BORDER_SIZE >= HEIGHT:
            if keys[pygame.K_s]:
                offset_y = 0

        # Calculate camera position
        player.x = WIDTH // 2
        player.y = HEIGHT // 2

        # Move the map in the opposite direction to simulate player movement

        # Draw everything
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (200, 200, 200), map)  # Gray border
        pygame.draw.rect(screen, (0, 255, 0), grass.move(offset_x, offset_y))  # Green for grass
        pygame.draw.rect(screen, (139, 69, 19), dirt.move(offset_x, offset_y))  # Brown for dirt
        pygame.draw.rect(screen, (0, 0, 255), water.move(offset_x, offset_y))  # Blue for water
        pygame.draw.rect(screen, (255, 255, 255), player)

        # Flip the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)








if __name__ == '__main__':
    main_menu()
