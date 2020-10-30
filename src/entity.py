from pygame import Rect

'''
module contains Entity, Block and Player class and some important functions specific to entities.
'''

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

class Entity:
    '''
    basic component of game.
    each component derived from entity.
    '''
    def __init__(self, x, y, width, height, color):
        self.color = color
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
    def __init__(self, x, y, width, height, color, block_type):
        super().__init__(x, y, width, height, color)
        self.block_type = block_type

class Player(Entity):
    '''
    player extended form entity contains all state variables required by the player.
    handels jumping and moving also.
    '''
    def __init__(self, x, y, width, height, color, gravity):
        super().__init__(x, y, width, height, color)

        # constants
        self.MAX_VELOCITY = (5, 5)
        self.GRAVITY = gravity
        self.JUMP_SPEED = 5

        # player state.
        self.velocity = [0, 0]
        self.move_direction = {
            'left' : False,
            'right' : False,
            'up' : False
        }


    def move(self, blocks):
        '''
        moves the player according to move_direction.
        '''
        self.velocity[1] += self.GRAVITY

        if self.move_direction['up']:
            self.move_direction['up'] = False
            self.velocity[1] = -self.JUMP_SPEED

        if self.move_direction['left']:
            self.velocity[0] -= 3
        if self.move_direction['right']:
            self.velocity[0] += 3

        if not self.move_direction['left'] and not self.move_direction['right']:
            self.velocity[0] = 0

        for i in range(2):
            if self.velocity[i] > self.MAX_VELOCITY[i]:
                self.velocity[i] = self.MAX_VELOCITY[i]
            elif self.velocity[i] < -self.MAX_VELOCITY[i]:
                self.velocity[i] = -self.MAX_VELOCITY[i]

        update_pos_from_collision(self, blocks, self.velocity)
