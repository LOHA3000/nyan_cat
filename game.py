import pygame
import sys
import os
from random import choice, randint
import time


def terminate():  # отключение программы
    global playing, is_pause, HIGH_SCORE
    playing, is_pause = False, False  # отключение основных циклов
    pygame.quit()  # отключение pygame
    file = open('data/high_score.txt', 'w')
    file.write(str(HIGH_SCORE))
    file.close()
    sys.exit()  # выключение программы


def load_image(name, color_key=None, transform=None):  # загрузка картинки
    fullname = os.path.join('data', name)  # преобразование пути в data\\<изначальный путь>
    image = pygame.image.load(fullname)  # преобразование в объект Surfase pygame
    if color_key is None:
        image.set_colorkey(color_key)  # создание прозрачного фона (не работает)
    if not (transform is None):
        image = pygame.transform.scale(image, tuple(transform))  # изменение размера картинки
    return image


def count(now, fon, nyan):  # расчёт номера анимации
    if now % 2 == 0:  # цикл анимации фона (раз в 3 смены основного)
        if fon < 3:
            fon += 1
        else:
            fon = 0
    if now % 4 == 0:  # цикл анимации нян кэта (раз в 5 смен основного)
        if nyan < 2:
            nyan += 1
        else:
            nyan = 0
    if now < 59:  # цикл смены основного счётчика
        now += 1
    else:
        now = 0
    return [now, fon, nyan]


def game():
    global SPEED, JUMP, SECOND_JUMP, NYAN, NYAN_HEIGHT, HEIGHT, GROUND_HEIGHT, FPS
    global LIFTING, FALL, FALL_SPEED, LIFTING_SPEED, LIFTING_COUNTER, FLY
    global STATES, CACTUS, ID
    global CREEPER_STADIES
    global playing, counter, fon_animation_counter, nyan_animation_counter, creeper_animation_counter
    global score, fly_counter, pause_button_image, pause_button_pos, pause_button_size
    global is_pause, is_main_menu, score, HIGH_SCORE

    pos = pause_button_pos
    size = pause_button_size

    while playing:  # основной цикл игры
        for event in pygame.event.get():  # сбор и обработка событий в окне
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # прыжок
                    if not JUMP:
                        LIFTING = True
                        FALL = False
                        JUMP = True
                    elif JUMP and not SECOND_JUMP:  # второй прыжок
                        LIFTING = True
                        FALL = False
                        SECOND_JUMP = True
                        LIFTING_COUNTER = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:  # нажатие на кнопку паузы
                if pos[0] + size[0] > event.pos[0] > pos[0] and pos[1] + size[1] > event.pos[1] > pos[1]:
                    is_pause = True
                    playing = False
                    pause()
            elif event.type == pygame.QUIT:  # закрытие окна
                terminate()

        new_counters = count(counter, fon_animation_counter, nyan_animation_counter)
        counter, fon_animation_counter, nyan_animation_counter = new_counters

        fon_image = f'fon/fon_{fon_animation_counter}.jpg'  # перезапись картинки фона для анимации
        fon = load_image(fon_image)
        screen.blit(fon, (0, 0))  # отображение на экране

        screen.blit(pause_button_image, tuple(pause_button_pos))  # отображение кнопки "пауза"

        animate_nyan(nyan_animation_counter)  # выбор вида персонажа в анимации

        for i in range(GROUNDS):  # движение "земли"
            move_ground(list(ground)[i], SPEED)

        # проверка падения, прыжка и полёта после прыжка
        if FALL:
            move_nyan(FALL_SPEED)
        elif LIFTING:
            move_nyan(LIFTING_SPEED)
        elif FLY:
            move_nyan(0)
            fly_counter += 1
            if fly_counter > SPEED ** (1 / 3):
                FLY = False
                FALL = True
                fly_counter = 0

        if False not in STATES:  # проверкадоступности объектов кактусов
            CACTUS, ID = change_cactus()
        else:  # движение доступного кактуса
            move_cactus(CACTUS, ID, SPEED)

        # анимация крипера (похоже, что он там просто для красоты)
        if creeper_animation_counter < len(CREEPER_STADIES) - 1:
            creeper_animation_counter += 1
        else:
            creeper_animation_counter = 0
        creeper_animation(creeper_animation_counter)
        creeper_move(SPEED // 2)  # передвижение крипера

        ground.draw(screen)  # отрисовка "земли"
        cactuses.draw(screen)  # отрисовка кактусов
        creeper.draw(screen)  # отрисовка крипера
        nyan_group.draw(screen)  # отрисовка нян кэт
        pygame.display.update()  # обновление экрана

        score += int(SPEED / FPS) + 1  # увеличение счётчика
        if score % 100 == 0:  # увеличение скорости движения в игре
            if SPEED < 100:
                SPEED += 2
                FALL_SPEED += 1
                LIFTING_SPEED -= 1

        game_status()

        clock.tick(FPS)  # ограничение повторений цикла в секунду

    time.sleep(3)
    is_main_menu = True
    if score > HIGH_SCORE:
        HIGH_SCORE = score
    restart()
    main_menu()


def pause():  # меню паузы
    global is_pause, pause_fon_image, continue_button_image, continue_button_pos, continue_button_size, playing
    global FPS

    screen.blit(pause_fon_image, (0, 0))  # отрисовка экрана паузы
    screen.blit(continue_button_image, tuple(continue_button_pos))  # отрисовка кнопки "продолжить"
    pygame.display.update()  # обновление дисплея
    pos = continue_button_pos
    size = continue_button_size

    while is_pause:  # основной цикл паузы
        for event in pygame.event.get():  # сбор событий и их обработка
            if event.type == pygame.MOUSEBUTTONDOWN:  # нажатие на кнопку продолжение курсором мыши
                if pos[0] + size[0] > event.pos[0] > pos[0] and pos[1] + size[1] > event.pos[1] > pos[1]:
                    is_pause = False
                    playing = True
                    game()
            elif event.type == pygame.QUIT:  # выход из игры
                terminate()

        clock.tick(FPS)  # ограничение повторений цикла в секунду


def main_menu():  # меню начала игры
    global FPS, is_main_menu, playing
    global menu_fon_image, start_button_image, start_button_pos, start_button_size

    screen.blit(menu_fon_image, (0, 0))  # отрисовка экрана паузы
    screen.blit(start_button_image, tuple(start_button_pos))  # отрисовка кнопки "продолжить"
    pygame.display.update()  # обновление дисплея
    pos = start_button_pos
    size = start_button_size

    while is_main_menu:  # основной цикл окна меню
        for event in pygame.event.get():  # сбор событий и их обработка
            if event.type == pygame.MOUSEBUTTONDOWN:  # нажатие на кнопку старта курсором мыши
                if pos[0] + size[0] > event.pos[0] > pos[0] and pos[1] + size[1] > event.pos[1] > pos[1]:
                    playing = True
                    is_main_menu = False
                    game()
            elif event.type == pygame.QUIT:  # выход из игры
                terminate()

        clock.tick(FPS)  # ограничение повторений цикла в секунду


def generate_ground(n):  # создание объектов "земли" в необходимом кол-ве
    for i in range(n):
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image(f"ground/ground_{i}.jpg")
        sprite.rect = pygame.Rect(0, 0, GROUND_LEN, GROUND_HEIGHT)
        sprite.rect.x = i * GROUND_LEN
        sprite.rect.y = HEIGHT - GROUND_HEIGHT
        ground.add(sprite)


def move_ground(ground_part, speed):  # перемещение выбранного участка "земли" с заданной скоростью
    if ground_part.rect.x <= -1 * GROUND_LEN:
        n = ground_part.rect.x + GROUND_LEN
        ground_part.rect.x = (GROUNDS - 1) * GROUND_LEN + n
    ground_part.rect.x -= speed


def generate_nyan():  # создание объекта нян кэт
    global NYAN

    sprite = pygame.sprite.Sprite()
    sprite.image = load_image(f'nyan/nyan_0.png', transform=[NYAN_WIDTH, NYAN_HEIGHT])
    sprite.rect = pygame.Rect(0, 0, NYAN_WIDTH, NYAN_HEIGHT)
    sprite.rect.x = 80
    sprite.rect.y = HEIGHT - GROUND_HEIGHT - NYAN_HEIGHT
    nyan_group.add(sprite)
    NYAN = sprite  # запись в глобальную переменную для более удобного использования


def move_nyan(i):  # прыжки и падение нян кэт
    global JUMP, SECOND_JUMP, NYAN, NYAN_HEIGHT, HEIGHT, GROUND_HEIGHT, cactuses
    global LIFTING, FALL, LIFTING_COUNTER, FIRST_LIFTING, SECOND_LIFTING, FLY

    if i > 0:  # падение
        if NYAN.rect.y + NYAN_HEIGHT < HEIGHT - GROUND_HEIGHT:  # пока не коснётся "земли" падает с скоростью i
            NYAN.rect.y += i
        if NYAN.rect.y + NYAN_HEIGHT > HEIGHT - GROUND_HEIGHT:  # сразу устанавливается на "землю", если слишком низко
            NYAN.rect.y = HEIGHT - GROUND_HEIGHT - NYAN_HEIGHT
        elif NYAN.rect.y + NYAN_HEIGHT == HEIGHT - GROUND_HEIGHT:  # момент касания "земли"
            JUMP = False
            SECOND_JUMP = False
            LIFTING = False
            FALL = False
    if i < 0:  # прыжок
        if (JUMP and not SECOND_JUMP) and LIFTING_COUNTER < FIRST_LIFTING:  # первый прыжок
            NYAN.rect.y += i
            LIFTING_COUNTER -= i
        elif SECOND_JUMP and LIFTING_COUNTER < SECOND_LIFTING:  # второй прыжок
            NYAN.rect.y += i
            LIFTING_COUNTER -= i
        else:  # активация полёта
            LIFTING = False
            FALL = False
            FLY = True
            LIFTING_COUNTER = 0


def game_status():
    global NYAN, CACTUS, playing, is_pause

    if pygame.sprite.collide_mask(NYAN, CACTUS):
        playing = False


def animate_nyan(nyan_count):  # обработка анимации нян кэта
    nyan_image = f'nyan/nyan_{nyan_count}.png'
    NYAN.image = load_image(nyan_image, transform=[NYAN_WIDTH, NYAN_HEIGHT])


def generate_cactuses(n):  # создание заданного количества объектов кактусов
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


def move_cactus(cactus, _id, speed):  # движение кактусов с проверкой их доступности
    global WIDTHES, cactuses, STATES, CACTUS, ID

    if cactus.rect.x > -1 * WIDTHES[_id]:
        cactus.rect.x -= speed
    else:
        STATES[_id] = True
        cactus.rect.x = randint(1000, 1500)
        CACTUS, ID = change_cactus()


def change_cactus():  # выбор кактуса для движения из доступных
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


def generate_creeper():  # создание объекта крипера
    global HEIGHT, GROUND_HEIGHT, CREEPER, creeper

    sprite = pygame.sprite.Sprite()
    sprite.image = load_image('creeper/creeper_0.png')
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = 500
    sprite.rect.y = HEIGHT - GROUND_HEIGHT - list(sprite.rect)[-1]
    CREEPER = sprite
    creeper.add(CREEPER)


def creeper_animation(i):  # анимация крипера
    global CREEPER, CREEPER_STADIES

    CREEPER.image = load_image(f'creeper/creeper_{CREEPER_STADIES[i]}.png')


def creeper_move(speed):  # перемещение крипера с заданной скоростью
    global CREEPER
    if CREEPER.rect.x > -1 * list(CREEPER.rect)[-1]:
        CREEPER.rect.x -= speed
    else:
        CREEPER.rect.x = 1000


# основные переменные

HEIGHT, WIDTH = 500, 1000  # высота и ширина окна игры
FPS = 60  # количество кадров в секунду

GROUNDS = 3  # количество объектов "земли"
GROUND_LEN = 975  # длина "земли"
GROUND_HEIGHT = 87  # высота "земли"

CACTUSES = 6  # количество кактусов
WIDTHES = {}  # ширина кактусов
STATES = []  # доступность исползования кактусов
CACTUS = ''  # выбранный кактус
ID = -1  # id выбранного кактуса среди объектов

SPEED = 25  # скорость игры

NYAN_HEIGHT = 105  # высота нян кэт
NYAN_WIDTH = 165  # длина нян кэт
NYAN = ''  # в будущем спрайт нян кэт

FALL_SPEED = 25  # скорость падения
LIFTING_SPEED = -1 * FALL_SPEED  # ось y напрвлена вниз, движение вверх производится его вычитанием
FALL = False  # состояние падения
LIFTING = False  # состояние прыжка
LIFTING_COUNTER = 0  # проверка длительности подъёма
FIRST_LIFTING = 200  # предел подъёма первым прыжком
SECOND_LIFTING = 100  # предел подъёма вторым прыжком
FLY = False  # состояние полёта

JUMP = False  # совершение первого прыжка
SECOND_JUMP = False  # совершение второго прыжка

CREEPER = ''  # в будущем спрайт крипера
CREEPER_STADIES = [0, 1, 2, 1, 0, 1, 2, 1, 0, 1, 2, 1, 3, 3, 3, 3]  # порядок состояния крипера

GAME_COUNTER = 0  # счётчик игры

HIGH_SCORE = int(open('data/high_score.txt').read())  # наибольший счёт

pygame.init()  # инициализация pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создание игрового окна
clock = pygame.time.Clock()  # создание ограничителя времени

nyan_group = pygame.sprite.Group()  # группа спрайтов нян кэт
generate_nyan()

ground = pygame.sprite.Group()  # группа спрайтов "земли"
generate_ground(GROUNDS)

cactuses = pygame.sprite.Group()  # группа спрайтов кактусов
generate_cactuses(CACTUSES)

creeper = pygame.sprite.Group()  # группа спрайтов криппера
generate_creeper()


def restart():  # сброс настроек для перезапуска
    global playing, counter, fon_animation_counter, nyan_animation_counter, creeper_animation_counter
    global score, fly_counter
    global STATES, ID, SPEED, FALL_SPEED, LIFTING_SPEED, FALL, LIFTING, LIFTING_COUNTER, FLY, JUMP, SECOND_JUMP
    global GAME_COUNTER
    global nyan_group, creeper, ground, cactuses

    playing = True  # состояние игры
    counter = 0  # основной счётчик
    fon_animation_counter = 0  # счётчик анимации фона
    nyan_animation_counter = 0  # счётчик анимации нян кэт
    creeper_animation_counter = 0  # счётчик анимации крипера
    score = 0  # счёт игры
    fly_counter = 0
    STATES = []
    ID = -1
    SPEED = 25
    FALL_SPEED = 25
    LIFTING_SPEED = -1 * FALL_SPEED
    FALL = False
    LIFTING = False
    LIFTING_COUNTER = 0
    FLY = False
    JUMP = False
    SECOND_JUMP = False
    GAME_COUNTER = 0

    nyan_group = pygame.sprite.Group()  # группа спрайтов нян кэт
    generate_nyan()

    ground = pygame.sprite.Group()  # группа спрайтов "земли"
    generate_ground(GROUNDS)

    cactuses = pygame.sprite.Group()  # группа спрайтов кактусов
    generate_cactuses(CACTUSES)

    creeper = pygame.sprite.Group()  # группа спрайтов криппера
    generate_creeper()


playing = False  # состояние игры
counter = 0  # основной счётчик
fon_animation_counter = 0  # счётчик анимации фона
nyan_animation_counter = 0  # счётчик анимации нян кэт
creeper_animation_counter = 0  # счётчик анимации крипера
score = 0  # счёт игры
fly_counter = 0  # проверка длительности полёта

is_pause = False  # состояние паузы
pause_button_image = load_image('pause/pause_button.png')  # изображение кнопки паузы
pause_button_pos = [890, 10]  # расположение кнопки паузы
pause_button_size = [100, 100]  # размер кнопки паузы
pause_fon_image = load_image('pause/pause_fon.png')  # картинка фона паузы
continue_button_image = load_image('pause/continue_button.png')  # картинка кнопки продолжения игры
continue_button_size = [336, 234]  # размеры кнопки продолжения
continue_button_pos = [332, 250]  # положение кнопки продолжения

is_main_menu = True  # состояние начального меню игры
menu_fon_image = load_image('main_menu/menu_fon.png')  # картинка фона меню
start_button_image = load_image('main_menu/start_button.png')  # картинка кнопки старта
start_button_size = [300, 100]  # размеры кнопки
start_button_pos = [350, 350]  # положение кнопки

main_menu()  # запуск игры
