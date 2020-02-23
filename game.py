import pygame
import sys
import os


def load_image(name, color_key=None, transform=[]):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if color_key is None:
        image.set_colorkey(color_key)
    if transform != []:
        image = pygame.transform.scale(image, tuple(transform))
    return image


def count(now, fon, nyan):
    if now % 2 == 0:
        if fon < 3:
            fon += 1
        else:
            fon = 0
    if now % 1 == 0:
        if nyan < 2:
            nyan += 1
        else:
            nyan = 0
    if now < 59:
        now += 1
    else:
        now = 0
    return [now, fon, nyan]


def game():
    playing = True
    counter = 0
    fon_animation_counter = 0
    nyan_animation_counter = 0

    while playing:
        global SPEED, JUMP, SECOND_JUMP, FALL_SPEED

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not JUMP:
                        NYAN.rect.y -= 200
                        JUMP = True
                    elif JUMP and not SECOND_JUMP:
                        NYAN.rect.y -= 80
                        SECOND_JUMP = True
                elif event.key == pygame.K_LEFT:
                    SPEED -= 10
                elif event.key == pygame.K_RIGHT:
                    SPEED += 10
            elif event.type == pygame.QUIT:
                playing = False
        new_counters = count(counter, fon_animation_counter, nyan_animation_counter)
        counter, fon_animation_counter, nyan_animation_counter = new_counters
        fon_image = f'fon/fon_{fon_animation_counter}.jpg'
        fon = load_image(fon_image)
        screen.blit(fon, (0, 0))
        animate_nyan(nyan_animation_counter)
        for i in range(GROUNDS):
            move_ground(list(ground)[i], SPEED)
        move_nyan(FALL_SPEED)
        ground.draw(screen)
        cactuses.draw(screen)
        nyan_group.draw(screen)
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


def generate_nyan():
    global NYAN

    sprite = pygame.sprite.Sprite()
    sprite.image = load_image(f'nyan/nyan_0.png', transform=[NYAN_WIDTH, NYAN_HEIGHT])
    sprite.rect = pygame.Rect(0, 0, NYAN_WIDTH, NYAN_HEIGHT)
    sprite.rect.x = 80
    sprite.rect.y = HEIGHT - GROUND_HEIGHT - NYAN_HEIGHT
    nyan_group.add(sprite)
    NYAN = list(nyan_group)[0]


def move_nyan(i):
    global JUMP, SECOND_JUMP, NYAN

    if NYAN.rect.y + NYAN_HEIGHT < HEIGHT - GROUND_HEIGHT:
        NYAN.rect.y += i
    elif NYAN.rect.y + NYAN_HEIGHT > HEIGHT - GROUND_HEIGHT:
        NYAN.rect.y = HEIGHT - GROUND_HEIGHT - NYAN_HEIGHT
    else:
        JUMP = False
        SECOND_JUMP = False


def animate_nyan(nyan_count):
    nyan_image = f'nyan/nyan_{nyan_count}.png'
    NYAN.image = load_image(nyan_image, transform=[NYAN_WIDTH, NYAN_HEIGHT])


def generate_cactuses(n):
    for i in range(n):
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image(f'cactuses/cactus_{i}.png', color_key=(255, 255, 255))
        sprite.rect = sprite.image.get_rect()
        height = list(sprite.rect)[-1]
        sprite.rect.x = 200 + 100 * i
        sprite.rect.y = HEIGHT - GROUND_HEIGHT - height
        cactuses.add(sprite)


HEIGHT, WIDTH = 500, 1000
FPS = 60

GROUNDS = 3
GROUND_LEN = 975
GROUND_HEIGHT = 87

CACTUSES = 6

SPEED = 20

NYAN_HEIGHT = 105
NYAN_WIDTH = 165
NYAN = ''

FALL_SPEED = 13
LIFTING_SPEED = 13

JUMP = False
SECOND_JUMP = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

nyan_group = pygame.sprite.Group()
generate_nyan()

ground = pygame.sprite.Group()
generate_ground(GROUNDS)

cactuses = pygame.sprite.Group()
generate_cactuses(CACTUSES)

game()

pygame.quit()
sys.exit()
