import configparser
from src.entity.entity import Entity

class Character(Entity):
    '''
    character extended form entity contains all state variables required by
    any movable or controlleable entity in gmae (player/enemy).
    '''
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')

        # constants
        self.MAX_VELOCITY = ( float(cfg['DEFAULT']['MAX_VELOCITY_X']), float(cfg['DEFAULT']['MAX_VELOCITY_Y']) )
        self.GRAVITY = float(cfg['DEFAULT']['GRAVITY'])
        self.JUMP_SPEED = float(cfg['DEFAULT']['JUMP_SPEED'])
        self.MAX_JUMP_COUNT = int(cfg['DEFAULT']['MAX_JUMP_COUNT'])

        self.RENDER_SURFACE_WIDTH = int(cfg['DEFAULT']['RENDER_SURFACE_WIDTH'])
        self.RENDER_SURFACE_HEIGHT = int(cfg['DEFAULT']['RENDER_SURFACE_HEIGHT'])

        # character state.
        self.velocity = [0, 0]
        self.in_mid_air = False
        self.landed = False
        self.jump_count = 0
        self.health = 100

        self.direction = True # True / False = Right / Left

        # following parameters can be changed by the derived classes
        self.VELOCITY_X_INC = 3
        self.damage_cooldown = 40
        self.read_to_take_damage = True
        self.frame_count = 0
        self.frame_count_cap = 100

    def jump(self):
        '''
        make character jump.
        class expects children classes to handel the state of in_mid_air and jump_count.
        '''
        if (self.jump_count < self.MAX_JUMP_COUNT) or not self.in_mid_air:
            self.velocity[1] = -self.JUMP_SPEED
            self.jump_count += 1

    def cap_velocity(self):
        '''
        function to cap the velocity of character.
        '''
        if self.velocity[0] > self.MAX_VELOCITY[0]:
            self.velocity[0] = self.MAX_VELOCITY[0]
        elif self.velocity[0] < -self.MAX_VELOCITY[0]:
            self.velocity[0] = -self.MAX_VELOCITY[0]

        if self.velocity[1] > self.MAX_VELOCITY[1]:
            self.velocity[1] = self.MAX_VELOCITY[1]
        elif self.velocity[1] < -self.MAX_VELOCITY[1]:
            self.velocity[1] = -self.MAX_VELOCITY[1]

    def take_damage(self, damage):
        '''
        !IMPORTANT: function expects parameters to be handled by the derived classes.
        function to receive damage from outside entity.
        damage is added hence it can process reward too.
        if +ve damage is provided it is added to health wihtout any restriction.
        '''
        if damage < 0:
            if self.read_to_take_damage:
                self.read_to_take_damage = False
                self.health += damage
                self.health = max(0, self.health)
        else:
            self.health += damage
            self.health = min(100, self.health)

    def update_pos_from_collision(self):
        '''
        function updates the position of primary entity based on collision detection.
        '''
        pass

    def move(self):
        '''
        moves the character according to move_direction.
        '''
        pass


    def attack(self):
        '''
        characters offensive move.
        '''
        pass
