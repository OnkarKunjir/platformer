import pygame
from src.entity import Entity
from src.utils import check_collision
from src.config import DISPLAY_WIDTH, DISPLAY_HEIGHT, GRAVITY

pygame.init()
RENDER_FRAME = True

MOVE_KEY_PRESSED = False
DIRECTION = False # True = Right False = Left
JUMP = False

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

clock = pygame.time.Clock()
player = Entity(x = 150, y = 20, width = 40, height = 60, color = (255,255,255))

tiles = [
    Entity(x = 0, y = DISPLAY_HEIGHT - 200, width = DISPLAY_WIDTH, height = 200, color = (255,255,123)),
    Entity(x = 100, y = DISPLAY_HEIGHT - 300, width = 100, height = 100, color = (255,111,123)),
    Entity(x = 500, y = DISPLAY_HEIGHT - 300, width = 100, height = 100, color = (255,111,123)),
    Entity(x = 300, y = 400, width = 500, height = 50, color = (255,111,123)),
]

move = [0, 0]

def event_handler(events):
    global RENDER_FRAME, MOVE_KEY_PRESSED, DIRECTION, JUMP
    for event in events:
        if event.type == pygame.QUIT:
            RENDER_FRAME = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RENDER_FRAME = False
            elif event.key == pygame.K_LEFT:
                MOVE_KEY_PRESSED = True
                DIRECTION = False
            elif event.key == pygame.K_RIGHT:
                MOVE_KEY_PRESSED = True
                DIRECTION = True
            elif event.key == pygame.K_SPACE:
                JUMP = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                MOVE_KEY_PRESSED = False


def update_entities():
    global GRAVITY, JUMP
    if JUMP:
        move[1] = -10
        JUMP = False

    move[1] += GRAVITY

    if MOVE_KEY_PRESSED:
        move[0] += 3 if DIRECTION else -3
    else:
        move[0] = 0

    for i in range(2):
        if move[i] > 12:
            move[i] = 12
        elif move[i] < -12:
            move[i] = -12

    player.move_x(move[0])
    colliding_entities = check_collision(primary_entity = player, check_against = tiles)

    for i in colliding_entities:
        if move[0] > 0:
            player.rect.right = i.rect.left
        else:
            player.rect.left = i.rect.right

    player.move_y(move[1])
    colliding_entities = check_collision(primary_entity = player, check_against = tiles)

    for i in colliding_entities:
        if move[1] > 0:
            player.rect.bottom = i.rect.top
        else:
            player.rect.top = i.rect.bottom
            move[1] = 0

def draw_frame():
    display.fill((0,0,0))
    pygame.draw.rect(display, player.color, player.rect)

    for tile in tiles:
        pygame.draw.rect(display, tile.color, tile.rect)



while RENDER_FRAME:
    event_handler(pygame.event.get())
    update_entities()
    draw_frame()
    pygame.display.update()
    clock.tick(60)
