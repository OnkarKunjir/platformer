import configparser

from src.entity.entity import Entity


class Character(Entity):
    """
    character extended form entity contains all state variables required by
    any movable or controlleable entity in gmae (player/enemy).
    """

    def __init__(self, x, y, width, height, state_n_frames=None, update_per_frame=10):
        """
        x, y = initaial postion
        height, width you know this boi.

        pass this if the character is to be animated.
        state_n_frames = dict('state_name' : (int) n_frames)
        update_per_frame = (int) when to update the frame.
        """
        super().__init__(x, y, width, height)
        cfg = configparser.ConfigParser()
        cfg.read("config.ini")

        # constants
        self.MAX_VELOCITY = (
            float(cfg["DEFAULT"]["MAX_VELOCITY_X"]),
            float(cfg["DEFAULT"]["MAX_VELOCITY_Y"]),
        )
        self.GRAVITY = float(cfg["DEFAULT"]["GRAVITY"])
        self.JUMP_SPEED = float(cfg["DEFAULT"]["JUMP_SPEED"])
        self.MAX_JUMP_COUNT = int(cfg["DEFAULT"]["MAX_JUMP_COUNT"])

        self.RENDER_SURFACE_WIDTH = int(cfg["DEFAULT"]["RENDER_SURFACE_WIDTH"])
        self.RENDER_SURFACE_HEIGHT = int(cfg["DEFAULT"]["RENDER_SURFACE_HEIGHT"])

        # character state.
        self.velocity = [0, 0]
        self.in_mid_air = False
        self.landed = False
        self.jump_count = 0
        self.health = 100

        self.direction = True  # True / False = Right / Left

        # following parameters can be changed by the derived classes
        self.VELOCITY_X_INC = 3
        self.damage_cooldown = 30
        self.read_to_take_damage = True
        self.frame_count = 0
        self.frame_count_cap = 100

        # animation variables
        # NOTE: character animation is different form entity animation
        # character has state hance create new thing..
        self.state_n_frames = state_n_frames
        self.current_state = "ideal"
        self.current_frame = 0
        self.update_per_frame = update_per_frame

    def jump(self):
        """
        make character jump.
        class expects children classes to handel the state of in_mid_air and jump_count.
        """
        if self.health == 0:
            return

        if (self.jump_count < self.MAX_JUMP_COUNT) or not self.in_mid_air:
            self.velocity[1] = -self.JUMP_SPEED
            self.jump_count += 1

    def cap_velocity(self):
        """
        function to cap the velocity of character.
        """
        if self.velocity[0] > self.MAX_VELOCITY[0]:
            self.velocity[0] = self.MAX_VELOCITY[0]
        elif self.velocity[0] < -self.MAX_VELOCITY[0]:
            self.velocity[0] = -self.MAX_VELOCITY[0]

        if self.velocity[1] > self.MAX_VELOCITY[1]:
            self.velocity[1] = self.MAX_VELOCITY[1]
        elif self.velocity[1] < -self.MAX_VELOCITY[1]:
            self.velocity[1] = -self.MAX_VELOCITY[1]

    def take_damage(self, damage, forced=False):
        """
        NOTE: function expects parameters to be handled by the derived classes.
        function to receive damage from outside entity.
        damage is added hence it can process reward too.
        if +ve damage is provided it is added to health wihtout any restriction.
        """
        if damage < 0:
            if self.read_to_take_damage or forced:
                self.read_to_take_damage = False
                self.health += damage
                self.health = max(0, self.health)
        else:
            self.health += damage
            self.health = min(100, self.health)

    def update(self):
        """
        function to update frame counter to keep track of animation frame.
        """
        self.frame_count += 1
        if self.frame_count > self.frame_count_cap:
            self.frame_count = 0

    def update_state(self):
        """
        function to update animation state of the character based on state variables.
        """
        new_state = None
        if self.in_mid_air:
            new_state = "jumping"
        elif self.velocity[0] == 0:
            new_state = "ideal"
        else:
            new_state = "running"

        if new_state == self.current_state:
            if self.frame_count % self.update_per_frame != 0:
                return
            # if state is same then move to next frame in same state.
            self.current_frame += 1
            if self.current_frame == self.state_n_frames[new_state]:
                self.current_frame = 0
        else:
            # if state is changed then swithch to new states first frame.
            self.current_state = new_state
            self.current_frame = 0

    def update_pos_from_collision(self):
        """
        function updates the position of primary entity based on collision detection.
        """
        pass

    def move(self):
        """
        moves the character according to move_direction.
        """
        pass

    def attack(self):
        """
        characters offensive move.
        """
        pass
