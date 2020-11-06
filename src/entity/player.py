import configparser
from pygame import image
import os
from src.entity.entity import Entity, check_collision
from src.entity.reward import Reward

class Player(Entity):
    '''
    player extended form entity contains all state variables required by the player.
    handels jumping and moving also.
    '''
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.color = color
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')

        # constants
        self.MAX_VELOCITY = ( float(cfg['DEFAULT']['MAX_VELOCITY_X']), float(cfg['DEFAULT']['MAX_VELOCITY_Y']) )
        self.GRAVITY = float(cfg['DEFAULT']['GRAVITY'])
        self.JUMP_SPEED = float(cfg['DEFAULT']['JUMP_SPEED'])
        self.MAX_JUMP_COUNT = int(cfg['DEFAULT']['MAX_JUMP_COUNT'])

        self.RENDER_SURFACE_WIDTH = int(cfg['DEFAULT']['RENDER_SURFACE_WIDTH'])
        self.RENDER_SURFACE_HEIGHT = int(cfg['DEFAULT']['RENDER_SURFACE_HEIGHT'])
        # player state.
        self.velocity = [0, 0]
        self.in_mid_air = False
        self.landed = False
        self.jump_count = 0
        self.move_direction = {
            'left' : False,
            'right' : False,
            'up' : False
        }

        self.direction = True # True / False = Right / Left


    def update_pos_from_collision(self, check_against, move, max_x = None, max_y = None):
        '''
        function updates the position of primary entity based on collision detection.
        '''

        self.move_x(move[0])
        colliding_entities = check_collision(self, check_against, max_x, max_y)

        left = False
        right = False
        top = False
        bottom = False

        for i in colliding_entities:
            if isinstance(i, Reward):
                i.is_valid = False
                continue

            elif move[0] > 0:
                self.rect.right = i.rect.left
                right = True
            else:
                self.rect.left = i.rect.right
                left = True

        self.move_y(move[1])
        colliding_entities = check_collision(self, check_against, max_x, max_y)

        for i in colliding_entities:
            if isinstance(i, Reward):
                i.is_valid = False
                continue
            elif move[1] > 0:
                self.rect.bottom = i.rect.top
                bottom = True
            else:
                self.rect.top = i.rect.bottom
                top = True

        return left, right, top, bottom

    def move(self, blocks):
        '''
        moves the player according to move_direction.
        '''
        self.velocity[1] += self.GRAVITY

        if self.move_direction['up'] and (not self.in_mid_air or self.jump_count < self.MAX_JUMP_COUNT):
            self.velocity[1] = -self.JUMP_SPEED
            self.jump_count += 1
        self.move_direction['up'] = False

        if self.move_direction['left']:
            self.velocity[0] -= 3
            self.direction = False
        if self.move_direction['right']:
            self.velocity[0] += 3
            self.direction = True

        if not self.move_direction['left'] and not self.move_direction['right']:
            self.velocity[0] = 0

        for i in range(2):
            if self.velocity[i] > self.MAX_VELOCITY[i]:
                self.velocity[i] = self.MAX_VELOCITY[i]
            elif self.velocity[i] < -self.MAX_VELOCITY[i]:
                self.velocity[i] = -self.MAX_VELOCITY[i]

        #left, right, top, bottom = update_pos_from_collision(self, blocks, self.velocity, self.RENDER_SURFACE_WIDTH, self.RENDER_SURFACE_HEIGHT)
        left, right, top, bottom = self.update_pos_from_collision(blocks, self.velocity)
        self.rect.x = max(0, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        if top:
            self.velocity[1] = 0
        self.landed = False
        if self.in_mid_air and bottom:
            self.landed = True

        self.in_mid_air = not bottom
        if not self.in_mid_air:
            self.jump_count = 0
