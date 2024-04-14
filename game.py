import pygame
import random
import os
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SKY ESCAPE")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load balloon image
balloon_img = pygame.image.load("balloon.png").convert_alpha()
balloon_img = pygame.transform.scale(balloon_img, (50, 50))

# Load background image
background_img = pygame.image.load("background.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = balloon_img
        self.rect = self.image.get_rect()
        self.reset_position()
        self.score = 0

    def reset_position(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Wrap around the screen
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    MAX_OBSTACLES = 100

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH)
        self.rect.y = random.randrange(-HEIGHT, 0)  # Start off-screen
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.x = random.randrange(WIDTH)
        self.rect.y = random.randrange(-HEIGHT, 0)
        self.speed = random.randint(1, 3)

    def create_new_obstacle(self):
        if len(obstacles) < Obstacle.MAX_OBSTACLES:
            new_obstacle = Obstacle()
            obstacles.add(new_obstacle)
            all_sprites.add(new_obstacle)
            new_obstacle.create_new_obstacle()  # Recursively create more obstacles

# Sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Create initial obstacles
for _ in range(10):
    obstacle = Obstacle()
    obstacles.add(obstacle)
    all_sprites.add(obstacle)

# Create balloon
balloon = Balloon()
all_sprites.add(balloon)

# Game fonts
score_font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 48)

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Restart the program
                python = sys.executable
                os.execl(python, python, *sys.argv)

    if not game_over:
        # Update
        all_sprites.update()

        # Check for collisions
        hits = pygame.sprite.spritecollide(balloon, obstacles, False)
        if hits:
            game_over = True

        # Increase score for each frame
        balloon.score += 1

        # Draw
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        score_text = score_font.render(f"Score: {balloon.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        if game_over:
            game_over_text = game_over_font.render("Game Over! Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()

        clock.tick(60)  # Limit to 60 frames per second

pygame.quit()
