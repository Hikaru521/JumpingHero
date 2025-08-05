import pygame
import sys
import random
import time

pygame.init()

WIDTH, HEIGHT = 1280, 960
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping Hero")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 48)

def draw_restart_screen(elapsed_time):
    screen.fill(BLACK)
    text = font.render(f"Túlélt idő: {elapsed_time} másodperc", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

    button_text = font.render("Újraindítás", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 80)
    pygame.draw.rect(screen, GREEN, button_rect)
    screen.blit(button_text, (button_rect.x + 60, button_rect.y + 20))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

def main():
    borders = [
        pygame.Rect(320, 240, 640, 20),
        pygame.Rect(320, 240, 20, 480),
        pygame.Rect(320, 720, 640, 20),
        pygame.Rect(960, 240, 20, 500),
    ]

    player = pygame.Rect(640, 480, 20, 20)
    jumping = False
    jump_count = 0
    jump_height = 50
    jump_duration = 20

    wall_width, wall_height = 20, 700
    wall_speed_range = (2, 7)
    wall_exists = [True, True, True, True]
    last_restart_time = [time.time() + 1] * 4
    walls = [
        {"x": WIDTH, "y": HEIGHT // 2 - wall_height // 2, "dx": -random.randint(*wall_speed_range), "dy": 0},
        {"x": 0 - wall_width, "y": HEIGHT // 2 - wall_height // 2, "dx": random.randint(*wall_speed_range), "dy": 0},
        {"x": WIDTH // 2 - wall_height // 2, "y": HEIGHT, "dx": 0, "dy": -random.randint(*wall_speed_range)},
        {"x": WIDTH // 2 - wall_height // 2, "y": 0 - wall_width, "dx": 0, "dy": random.randint(*wall_speed_range)},
    ]

    start_time = time.time()

    running = True
    while running:
        screen.fill(BLACK)

        elapsed_time_sec = int(time.time() - start_time)
        time_text = f"{elapsed_time_sec} mp"
        time_surface = font.render(time_text, True, WHITE)
        screen.blit(time_surface, (640, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -4
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 4
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -4
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 4
        if keys[pygame.K_SPACE] and not jumping:
            jumping = True
            jump_count = 0

        if jumping:
            if jump_count < jump_duration:
                dy -= jump_height / jump_duration
            elif jump_count < jump_duration * 2:
                dy += jump_height / jump_duration
            else:
                jumping = False
            jump_count += 1

        new_pos = player.move(dx, dy)

        collision = False
        for border in borders:
            if new_pos.colliderect(border):
                collision = True
                break

        for i, wall in enumerate(walls):
            if wall_exists[i]:
                if time.time() - start_time > 2:
                    wall["x"] += wall["dx"]
                    wall["y"] += wall["dy"]

                    wall_rect = pygame.Rect(
                        wall["x"], wall["y"],
                        wall_width if i in [0, 1] else wall_height,
                        wall_height if i in [0, 1] else wall_width,
                    )

                    if new_pos.colliderect(wall_rect):
                        if not jumping:
                            running = False
                            break

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

        if not collision:
            player = new_pos

        for border in borders:
            pygame.draw.rect(screen, WHITE, border)

        for i, wall in enumerate(walls):
            if wall_exists[i]:
                if i in [0, 1]:
                    pygame.draw.rect(screen, RED, (wall["x"], wall["y"], wall_width, wall_height))
                else:
                    pygame.draw.rect(screen, RED, (wall["x"], wall["y"], wall_height, wall_width))

        pygame.draw.rect(screen, GREEN, player)

        pygame.display.flip()
        clock.tick(60)

    draw_restart_screen(elapsed_time_sec)
    main()

main()
