import configparser

from src.entity.character import Character
from src.entity.reward import Reward


class Player(Character):
    """
    player extended form entity contains all state variables required by the player.
    handels jumping and moving also.
    """

    def __init__(
        self, x, y, width, height, max_depth=float("inf"), update_per_frame=10
    ):
        cfg = configparser.ConfigParser()
        cfg.read("config.ini")

        frame_mapping_cfg = cfg["PLAYER_FRAME_MAPPING"]
        state_n_frames = {
            "ideal": int(frame_mapping_cfg["IDEAL"]),
            "running": int(frame_mapping_cfg["RUNNING"]),
            "jumping": int(frame_mapping_cfg["JUMPING"]),
        }

        super().__init__(x, y, width, height, state_n_frames, update_per_frame)
        self.max_depth = max_depth
        self.move_direction = {
            "left": False,
            "right": False,
            "up": False,
            "attack": False,
        }

        self.attack_arc_end_deg = 300

        self.VELOCITY_X_INC = float(cfg["PLAYER"]["ACCELERATION"])
        self.ground_friction = float(cfg["PLAYER"]["GROUND_FRICTION"])
        self.air_resistance = float(cfg["PLAYER"]["AIR_RESISTANCE"])

    def update_pos_from_collision(self, check_against, max_x=None, max_y=None):
        """
        function updates the position of primary entity based on collision detection.
        """

        score = 0
        move = self.velocity
        self.move_x(move[0])
        colliding_entities = filter(self.rect.colliderect, check_against)

        left = False
        right = False
        top = False
        bottom = False

        for i in colliding_entities:
            if isinstance(i, Reward):
                if i.is_valid:
                    score += i.score_gain
                    self.take_damage(i.health_gain)
                    if i.block_type == 3:
                        i.is_valid = False
                continue

            elif move[0] > 0:
                self.rect.right = i.rect.left
                right = True
            else:
                self.rect.left = i.rect.right
                left = True

        self.move_y(move[1])

        colliding_entities = filter(self.rect.colliderect, check_against)

        for i in colliding_entities:
            if isinstance(i, Reward):
                if i.is_valid:
                    score += i.score_gain
                    self.take_damage(i.health_gain)
                    if i.block_type == 3:
                        i.is_valid = False
                continue
            elif move[1] > 0:
                self.rect.bottom = i.rect.top
                bottom = True
            else:
                self.rect.top = i.rect.bottom
                top = True

        return left, right, top, bottom, score

    def move(self, blocks, enemies):
        """
        blocks = static blocks for collision detection and reward
        enemies = characters to process when attack is done.
        moves the player according to move_direction.
        """
        self.update()

        if self.frame_count % self.damage_cooldown == 0:
            self.read_to_take_damage = True

        # update velocity of player.
        self.velocity[1] += self.GRAVITY

        if self.move_direction["up"] and (
            not self.in_mid_air or self.jump_count < self.MAX_JUMP_COUNT
        ):
            self.jump()

        self.move_direction["up"] = False

        if self.move_direction["left"]:
            self.velocity[0] -= self.VELOCITY_X_INC
            self.direction = False
        if self.move_direction["right"]:
            self.velocity[0] += self.VELOCITY_X_INC
            self.direction = True

        if not self.move_direction["left"] and not self.move_direction["right"]:
            current_friction = (
                self.air_resistance if self.in_mid_air else self.ground_friction
            )

            if abs(self.velocity[0]) < 0.1:
                self.velocity[0] = 0
            elif self.velocity[0] > 0:
                self.velocity[0] -= current_friction
            else:
                self.velocity[0] += current_friction

        self.cap_velocity()

        if self.health == 0:
            # if player is dead make horizontal velocity zero.
            self.velocity[0] = 0

        left, right, top, bottom, score = self.update_pos_from_collision(blocks)
        # stop player from moving out of map.
        self.rect.x = max(0, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        if top:
            # stop jumping if player collides his head on another entity.
            self.velocity[1] = 0

        self.landed = False
        if self.in_mid_air and bottom:
            self.landed = True

        if self.in_mid_air and (right or left):
            self.velocity[0] = 0

        self.in_mid_air = not bottom
        if not self.in_mid_air:
            self.jump_count = 0

        if self.move_direction["attack"]:
            self.move_direction["attack"] = False
            self.attack(enemies)

        if self.rect.y > self.max_depth:
            # kill the player if he/she falls from the map. don't let them suffer for infinity.
            self.take_damage(-100, forced=True)

        self.update_state()
        return score

    def attack(self, enemies):
        self.attack_arc_end_deg += 15
        # make enemies suffer.
        damage_area = self.rect.copy()
        damage_area.width = damage_area.width + 20
        if not self.direction:
            # looking left
            damage_area.x -= 20

        for enemy in filter(lambda e: damage_area.colliderect(e), enemies):
            enemy.take_damage(-20)
