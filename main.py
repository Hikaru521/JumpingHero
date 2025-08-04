import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 960))
clock = pygame.time.Clock()
running = True

#                X    Y   szél. mag.
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
jump_duration = 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

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
            dy = 0
            break

    if not collision:
        player = new_pos

    for border in borders:
        pygame.draw.rect(screen, (255, 255, 255), border)

    pygame.draw.rect(screen, (0, 255, 0), player)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()