import pygame
import sys
import random
import time

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("fasz.oldalak")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()

wall_width, wall_height = 20, 480
wall_speed_range = (2, 7)
wall_exists = [True, True, True, True]

last_restart_time = [time.time() + 1 ] * 4

walls = [
    {"x": WIDTH, "y": HEIGHT//2 - wall_height//2, "dx": -random.randint(*wall_speed_range), "dy": 0},              # Jobb fal
    {"x": 0 - wall_width, "y": HEIGHT//2 - wall_height//2, "dx": random.randint(*wall_speed_range), "dy": 0},      # Bal fal
    {"x": WIDTH//2 - wall_height//2, "y": HEIGHT, "dx": 0, "dy": -random.randint(*wall_speed_range)},             # Alsó fal
    {"x": WIDTH//2 - wall_height//2, "y": 0 - wall_width, "dx": 0, "dy": random.randint(*wall_speed_range)},       # Felső fal
]

start_time = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    for i, wall in enumerate(walls):
        if wall_exists[i]:
            if time.time() - start_time > 2:
                wall["x"] += wall["dx"]
                wall["y"] += wall["dy"]
                if i in [0, 1]:
                    if wall["x"] + wall_width < 0 or wall["x"] > WIDTH:
                        wall_exists[i] = False
                        last_restart_time[i] = time.time()
                else:
                    if wall["y"] + wall_width < 0 or wall["y"] > HEIGHT:
                        wall_exists[i] = False
                        last_restart_time[i] = time.time()
        else:
            if time.time() - last_restart_time[i] > random.randint(3, 8):
                wall_exists[i] = True
                last_restart_time[i] = time.time()

                if i == 0:
                    wall["x"] = WIDTH
                    wall["y"] = HEIGHT // 2 - wall_height // 2
                    wall["dx"] = -random.randint(*wall_speed_range)
                    wall["dy"] = 0
                elif i == 1:
                    wall["x"] = 0 - wall_width
                    wall["y"] = HEIGHT // 2 - wall_height // 2
                    wall["dx"] = random.randint(*wall_speed_range)
                    wall["dy"] = 0
                elif i == 2:
                    wall["x"] = WIDTH // 2 - wall_height // 2
                    wall["y"] = HEIGHT
                    wall["dx"] = 0
                    wall["dy"] = -random.randint(*wall_speed_range)
                elif i == 3:
                    wall["x"] = WIDTH // 2 - wall_height // 2
                    wall["y"] = 0 - wall_width
                    wall["dx"] = 0
                    wall["dy"] = random.randint(*wall_speed_range)      
        if wall_exists[i]:
            if i in [0, 1]:
                pygame.draw.rect(screen, RED, (wall["x"], wall["y"], wall_width, wall_height))
            else:
                pygame.draw.rect(screen, RED, (wall["x"], wall["y"], wall_height, wall_width))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()