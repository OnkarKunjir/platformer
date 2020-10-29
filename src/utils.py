from pygame import Rect
import os
import random
from src.entity import Entity

def check_collision(primary_entity, check_against):
    '''
    function to check collision between primary entity and list of non primary entities
    primary_entity = Entity()
    check_against = [Entity(),...]
    returns list of Entity from check_against which collide with primary_entity
    '''
    colliding_entities = []
    for i in check_against:
        if primary_entity.rect.colliderect(i.rect):
            colliding_entities.append(i)

    return colliding_entities

def update_pos_from_collision(primary_entity, check_against, move):
    '''
    function updates the position of primary entity based on collision detection.
    '''
    primary_entity.move_x(move[0])
    colliding_entities = check_collision(primary_entity, check_against)

    for i in colliding_entities:
        if move[0] > 0:
            primary_entity.rect.right = i.rect.left
        else:
            primary_entity.rect.left = i.rect.right

    primary_entity.move_y(move[1])
    colliding_entities = check_collision(primary_entity, check_against)

    for i in colliding_entities:
        if move[1] > 0:
            primary_entity.rect.bottom = i.rect.top
        else:
            primary_entity.rect.top = i.rect.bottom
            move[1] = 0

def load_level(level_name, image_size, display_size):
    '''
    function loads map from txt file from assets/levels and converts each cell into appropriate Entity element.
    returns list of Entity.
    '''
    level_path = 'assets/levels/' + level_name + '.txt'
    tiles = []

    if os.path.exists(level_path):
        with open(level_path, 'r') as lvl:
            lvl = lvl.read().split('\n')
            x = 0
            y = 0
            for row in lvl:
                x = 0
                if len(row.strip()) > 0:
                    for cell in row.strip().split(','):
                        cell = int(cell)
                        if cell == 1:
                            tiles.append(
                                Entity(x = x, y = y, width = image_size[0], height = image_size[1], color = (random.randint(1,255),random.randint(1,255),random.randint(1,255))),
                            )
                        x += image_size[0]
                    y += image_size[1]
    return tiles
