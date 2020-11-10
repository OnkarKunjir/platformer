import configparser
from src.entity.entity import Entity, check_collision
from src.entity.reward import Reward

class Enemy(Entity):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.velocity = [0, 0]
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

        score = 0
        self.move_x(move[0])
        colliding_entities = check_collision(self, check_against, max_x, max_y)

        left = False
        right = False
        top = False
        bottom = False

        for i in colliding_entities:
            if isinstance(i, Reward):
                continue
            if move[0] > 0:
                self.rect.right = i.rect.left
                right = True
            else:
                self.rect.left = i.rect.right
                left = True

        self.move_y(move[1])
        colliding_entities = check_collision(self, check_against, max_x, max_y)

        for i in colliding_entities:
            if isinstance(i, Reward):
                continue
            if move[1] > 0:
                self.rect.bottom = i.rect.top
                bottom = True
            else:
                self.rect.top = i.rect.bottom
                top = True

        return left, right, top, bottom, score

    def move(self, blocks, player):
        self.velocity[1] += self.GRAVITY

        if abs(self.rect.x - player.rect.x) > 60:
            if self.rect.x > player.rect.x:
                self.velocity[0] -= 3
            else:
                self.velocity[0] += 3
        else:
            self.velocity[0] = 0
        if (self.rect.y > player.rect.y) and (not self.in_mid_air or self.jump_count < 2):
            self.jump_count += 1
            self.velocity[1] -= 2*self.JUMP_SPEED

        if self.velocity[0] > self.MAX_VELOCITY[0]:
            self.velocity[0] = self.MAX_VELOCITY[0]
        elif self.velocity[0] < -self.MAX_VELOCITY[0]:
            self.velocity[0] = -self.MAX_VELOCITY[0]

        if self.velocity[1] > self.MAX_VELOCITY[1]:
            self.velocity[1] = self.MAX_VELOCITY[1]
        elif self.velocity[1] < -self.MAX_VELOCITY[1]:
            self.velocity[1] = -self.MAX_VELOCITY[1]

        left, right, top, bottom, score= self.update_pos_from_collision(blocks, self.velocity)

        self.in_mid_air = not bottom
        if not self.in_mid_air:
            self.jump_count = 0

        if (left or right) and self.jump_count < self.MAX_JUMP_COUNT:
            self.velocity[1] -= 2*self.JUMP_SPEED
