import configparser
from pygame import Rect

'''
module contains Entity, Block and Player class and some important functions specific to entities.
'''

def check_collision(primary_entity, check_against, max_x = None, max_y = None):
    '''
    function to check collision between primary entity and list of non primary entities
    primary_entity = Entity()
    check_against = [Entity(),...]
    returns list of Entity from check_against which collide with primary_entity
    '''
    colliding_entities = []
    if max_x == None or max_y == None:
        for i in check_against:
            if primary_entity.rect.colliderect(i.rect):
                colliding_entities.append(i)
    else:
        for i in check_against:
            if i.rect.x < 0 or i.rect.y < 0 or i.rect.x > max_x or i.rect.y > max_y:
                continue
            if primary_entity.rect.colliderect(i.rect):
                colliding_entities.append(i)

    return colliding_entities

def update_pos_from_collision(primary_entity, check_against, move, max_x = None, max_y = None):
    '''
    function updates the position of primary entity based on collision detection.
    '''
    primary_entity.move_x(move[0])
    colliding_entities = check_collision(primary_entity, check_against, max_x, max_y)

    left = False
    right = False
    top = False
    bottom = False

    for i in colliding_entities:
        if move[0] > 0:
            primary_entity.rect.right = i.rect.left
            right = True
        else:
            primary_entity.rect.left = i.rect.right
            left = True

    primary_entity.move_y(move[1])
    colliding_entities = check_collision(primary_entity, check_against, max_x, max_y)

    for i in colliding_entities:
        if move[1] > 0:
            primary_entity.rect.bottom = i.rect.top
            bottom = True
        else:
            primary_entity.rect.top = i.rect.bottom
            top = True

    return left, right, top, bottom

class Entity:
    '''
    basic component of game.
    each component derived from entity.
    '''
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)

    def set_pos(self, pos):
        '''
        set x,y to new position pos = (x, y)
        '''
        self.rect.x, self.rect.y = pos

    def move_x(self, dist):
        self.rect.x += dist
    def move_y(self, dist):
        self.rect.y += dist

class Block(Entity):
    def __init__(self, x, y, width, height, block_type):
        super().__init__(x, y, width, height)
        self.block_type = block_type

