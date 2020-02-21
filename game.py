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
    fon_image = "fon/fon_0.jpg"

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        counter, fon_animation_counter = fon_count(counter, fon_animation_counter)
        '''if fon_animation_counter < 3:
            fon_animation_counter += 1
        else:
            fon_animation_counter = 0'''
        fon_image = f'fon/fon_{fon_animation_counter}.jpg'
        fon = pygame.transform.scale(load_image(fon_image), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        ground.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def generate_ground(n):
    for i in range(n):
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image(f"ground/ground_{i}.jpg")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = i * 1000
        sprite.rect.y = 450
        ground.add(sprite)


def move_ground(ground):
    ground.rect.x += 10


HEIGHT, WIDTH = 500, 1000
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

ground = pygame.sprite.Group()
generate_ground(2)

game()

pygame.quit()
sys.exit()
