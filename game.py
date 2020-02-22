import pygame
import sys
import os


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if color_key is None:
        image.set_colorkey(color_key)
    return image


def fon_count(now, fon):
    if now == 2:
        if fon < 3:
            fon += 1
        else:
            fon = 0
    if now < 2:
        now += 1
    else:
        now = 0
    return [now, fon]


def game():
    playing = True
    counter = 0
    fon_animation_counter = 0

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        counter, fon_animation_counter = fon_count(counter, fon_animation_counter)
        fon_image = f'fon/fon_{fon_animation_counter}.jpg'
        fon = pygame.transform.scale(load_image(fon_image), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        for i in range(GROUNDS):
            move_ground(list(ground)[i], SPEED)
        ground.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def generate_ground(n):
    for i in range(n):
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image(f"ground/ground_{i}.jpg")
        sprite.rect = pygame.Rect(0, 0, GROUND_LEN, GROUND_HEIGHT)
        sprite.rect.x = i * GROUND_LEN
        sprite.rect.y = HEIGHT - GROUND_HEIGHT
        ground.add(sprite)


def move_ground(ground, speed):
    if ground.rect.x <= -1 * GROUND_LEN:
        n = ground.rect.x + GROUND_LEN
        ground.rect.x = (GROUNDS - 1) * GROUND_LEN + n
    ground.rect.x -= speed


HEIGHT, WIDTH = 500, 1000
FPS = 60
GROUNDS = 3
GROUND_LEN = 975
GROUND_HEIGHT = 87
SPEED = 34

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

ground = pygame.sprite.Group()
generate_ground(GROUNDS)

game()

pygame.quit()
sys.exit()
