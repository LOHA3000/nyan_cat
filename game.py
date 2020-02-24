import pygame
import sys
import os
from random import choice


def load_image(name, color_key=None, transform=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if color_key is None:
        image.set_colorkey(color_key)
    if not (transform is None):
        image = pygame.transform.scale(image, tuple(transform))
    return image


def count(now, fon, nyan):
    if now % 2 == 0:
        if fon < 3:
            fon += 1
        else:
            fon = 0
    if now % 4 == 0:
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
    score = 0

    while playing:
        global SPEED, JUMP, SECOND_JUMP, NYAN, NYAN_HEIGHT, HEIGHT, GROUND_HEIGHT
        global LIFTING, FALL, FALL_SPEED, LIFTING_SPEED, LIFTING_COUNTER
        global STATES, CACTUS, ID

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not JUMP:
                        LIFTING = True
                        FALL = False
                        JUMP = True
                    elif JUMP and not SECOND_JUMP:
                        LIFTING = True
                        FALL = False
                        SECOND_JUMP = True
                        LIFTING_COUNTER = 0
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
        if FALL:
            move_nyan(FALL_SPEED)
        elif LIFTING:
            move_nyan(LIFTING_SPEED)
        if False not in STATES:
            CACTUS, ID = change_cactus()
        else:
            move_cactus(CACTUS, ID, SPEED)
        ground.draw(screen)
        cactuses.draw(screen)
        creeper.draw(screen)
        nyan_group.draw(screen)
        pygame.display.update()
        score += int(SPEED / FPS) + 1
        if score % 100 == 0:
            if SPEED < 350:
                SPEED += 5
                FALL_SPEED += 3
                LIFTING_SPEED -= 3
            print(score)
        clock.tick(FPS)


def generate_ground(n):
    for i in range(n):
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image(f"ground/ground_{i}.jpg")
        sprite.rect = pygame.Rect(0, 0, GROUND_LEN, GROUND_HEIGHT)
        sprite.rect.x = i * GROUND_LEN
        sprite.rect.y = HEIGHT - GROUND_HEIGHT
        ground.add(sprite)


def move_ground(ground_part, speed):
    if ground_part.rect.x <= -1 * GROUND_LEN:
        n = ground_part.rect.x + GROUND_LEN
        ground_part.rect.x = (GROUNDS - 1) * GROUND_LEN + n
    ground_part.rect.x -= speed


def generate_nyan():
    global NYAN
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image(f'nyan/nyan_0.png', transform=[NYAN_WIDTH, NYAN_HEIGHT])
    sprite.rect = pygame.Rect(0, 0, NYAN_WIDTH, NYAN_HEIGHT)
    sprite.rect.x = 80
    sprite.rect.y = HEIGHT - GROUND_HEIGHT - NYAN_HEIGHT
    nyan_group.add(sprite)
    NYAN = sprite


def move_nyan(i):
    global JUMP, SECOND_JUMP, NYAN, NYAN_HEIGHT, HEIGHT, GROUND_HEIGHT
    global LIFTING, FALL, LIFTING_COUNTER, FIRST_LIFTING, SECOND_LIFTING
    if i > 0:
        if NYAN.rect.y + NYAN_HEIGHT < HEIGHT - GROUND_HEIGHT:
            NYAN.rect.y += i
        if NYAN.rect.y + NYAN_HEIGHT > HEIGHT - GROUND_HEIGHT:
            NYAN.rect.y = HEIGHT - GROUND_HEIGHT - NYAN_HEIGHT
        elif NYAN.rect.y + NYAN_HEIGHT == HEIGHT - GROUND_HEIGHT:
            JUMP = False
            SECOND_JUMP = False
            LIFTING = False
            FALL = False
    if i < 0:
        if (JUMP and not SECOND_JUMP) and LIFTING_COUNTER < FIRST_LIFTING:
            NYAN.rect.y += i
            LIFTING_COUNTER -= i
        elif SECOND_JUMP and LIFTING_COUNTER < SECOND_LIFTING:
            NYAN.rect.y += i
            LIFTING_COUNTER -= i
        else:
            LIFTING = False
            FALL = True
            LIFTING_COUNTER = 0


def animate_nyan(nyan_count):
    nyan_image = f'nyan/nyan_{nyan_count}.png'
    NYAN.image = load_image(nyan_image, transform=[NYAN_WIDTH, NYAN_HEIGHT])


def generate_cactuses(n):
    global WIDTHES, STATES
    for i in range(n):
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image(f'cactuses/cactus_{i}.png')
        rect = sprite.image.get_rect()
        height = int(rect[-1] * 1.5)
        width = int(rect[-2] * 1.5)
        WIDTHES[i] = width
        STATES.append(True)
        sprite.rect = pygame.Rect(0, 0, width, height)
        sprite.image = load_image(f'cactuses/cactus_{i}.png', transform=[width, height])
        sprite.rect.x = 1000  # пока невидимые
        sprite.rect.y = HEIGHT - GROUND_HEIGHT - height
        cactuses.add(sprite)


def move_cactus(cactus, _id, speed):
    global WIDTHES, cactuses, STATES, CACTUS, ID
    if cactus.rect.x > -1 * WIDTHES[_id]:
        cactus.rect.x -= speed
    else:
        STATES[_id] = True
        cactus.rect.x = 1000
        CACTUS, ID = change_cactus()


def change_cactus():
    global cactuses, STATES
    _cactuses = list(cactuses)
    available = []
    for i in range(len(STATES)):
        if STATES[i]:
            available.append(_cactuses[i])
    cactus = choice(available)
    _id = 0
    for _id in range(CACTUSES):
        if _cactuses[_id] == cactus:
            STATES[_id] = False
            break
    return [cactus, _id]


def generate_creeper():
    global HEIGHT, GROUND_HEIGHT, CREEPER, creeper
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image('creeper/creeper_0.png')
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = 500
    sprite.rect.y = HEIGHT - GROUND_HEIGHT - list(sprite.rect)[-1]
    CREEPER = sprite
    creeper.add(CREEPER)


HEIGHT, WIDTH = 500, 1000
FPS = 60

GROUNDS = 3
GROUND_LEN = 975
GROUND_HEIGHT = 87

CACTUSES = 6
WIDTHES = {}  # ширина кактусов
STATES = []  # доступность исползования кактусов
CACTUS = ''  # выбранный кактус
ID = -1  # id выбранного кактуса среди объектов

SPEED = 40

NYAN_HEIGHT = 105
NYAN_WIDTH = 165
NYAN = ''

FALL_SPEED = 30
LIFTING_SPEED = -1 * FALL_SPEED  # ось y напрвлена вниз, движение вверх производится его вычитанием
FALL = False
LIFTING = False
LIFTING_COUNTER = 0
FIRST_LIFTING = 200
SECOND_LIFTING = 100

JUMP = False
SECOND_JUMP = False

CREEPER = ''
CREEPER_STADIES = [0, 1, 0, 1, 0, 1, 0, 1, 2, 3]

GAME_COUNTER = 0
HIGH_SCORE = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

nyan_group = pygame.sprite.Group()
generate_nyan()

ground = pygame.sprite.Group()
generate_ground(GROUNDS)

cactuses = pygame.sprite.Group()
generate_cactuses(CACTUSES)

creeper = pygame.sprite.Group()
generate_creeper()

game()  # пока без стартоваго окна и окна паузы, только игровая часть

pygame.quit()
sys.exit()
