import configparser

from pygame import Rect

"""
module contains Entity, Block and Player class and some important functions specific to entities.
"""


def check_collision(primary_entity, check_against, max_x=None, max_y=None):
    """
    function to check collision between primary entity and list of non primary entities
    primary_entity = Entity()
    check_against = [Entity(),...]
    returns list of Entity from check_against which collide with primary_entity
    """
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


class Entity:
    """
    basic component of game.
    each component derived from entity.
    """

    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)

    def set_pos(self, pos):
        """
        set x,y to new position pos = (x, y)
        """
        self.rect.x, self.rect.y = pos

    def move_x(self, dist):
        self.rect.x += dist

    def move_y(self, dist):
        self.rect.y += dist
