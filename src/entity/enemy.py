from src.entity.character import Character
from src.entity.reward import Reward

class Enemy(Character):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        # constants
        self.JUMP_COOLDOWN = 15
        self.ATTACK_COOLDOWN = 100

        self.color = color
        self.x_offset = 20
        self.first_jumped_ago = 0
        self.attacked_ago = 0
        self.attack_arc_end_deg = 0

        self.VELOCITY_X_INC = 0.1

    def update_pos_from_collision(self, check_against, max_x = None, max_y = None):
        '''
        function updates the position of primary entity based on collision detection.
        '''
        move = self.velocity
        self.move_x(move[0])
        colliding_entities = filter(self.rect.colliderect, check_against)

        left = False
        right = False
        top = False
        bottom = False

        for i in colliding_entities:
            if isinstance(i, Reward):
                continue

            if isinstance(i, Enemy):
                if i == self:
                    continue
                if move[0] > 0:
                    self.rect.right = i.rect.left - 10
                    right = True
                else:
                    self.rect.left = i.rect.right + 10
                    left = True
                continue

            if move[0] > 0:
                self.rect.right = i.rect.left
                right = True
            else:
                self.rect.left = i.rect.right
                left = True

        self.move_y(move[1])
        colliding_entities = filter(self.rect.colliderect, check_against)

        for i in colliding_entities:
            if isinstance(i, Reward):
                continue

            if isinstance(i, Enemy):
                if i == self:
                    continue
                if move[1] > 0:
                    self.rect.bottom = i.rect.top - 10
                    bottom = True
                else:
                    self.rect.top = i.rect.bottom + 10
                    top = True
                continue

            if move[1] > 0:
                self.rect.bottom = i.rect.top
                bottom = True
            else:
                self.rect.top = i.rect.bottom
                top = True

        return left, right, top, bottom

    def move(self, blocks, comrades, player, translated_location):
        self.read_to_take_damage = True
        self.attacked_ago += 1

        tx, ty, _, _ = translated_location
        if tx < 0 or tx > self.RENDER_SURFACE_WIDTH or ty < 0 or ty > self.RENDER_SURFACE_HEIGHT:
            # update postion if and only if enemy is within frame.
            return

        player_x = player.rect.x
        player_y = player.rect.y
        enemy_x = self.rect.x
        enemy_y = self.rect.y

        self.velocity[1] += self.GRAVITY

        if abs(enemy_x - player_x) > self.x_offset:
            if enemy_x > player_x:
                self.velocity[0] -= self.VELOCITY_X_INC
                self.direction = False
            elif enemy_x < player_x:
                self.velocity[0] += self.VELOCITY_X_INC
                self.direction = True
        else:
            self.velocity[0] = 0
            self.attack(player)

        if (enemy_y > player_y) and (self.first_jumped_ago == 0):
            self.jump()

        self.cap_velocity()
        if self.health == 0:
            # if i'm ded I ain't movin bro
            self.velocity[0] = 0

        blocks = blocks + comrades
        left, right, top, bottom = self.update_pos_from_collision(blocks)
        self.in_mid_air = not bottom

        if not self.in_mid_air:
            self.jump_count = 0
            self.first_jumped_ago = 0
        else:
            self.first_jumped_ago += 1
            if self.first_jumped_ago > self.JUMP_COOLDOWN:
                self.first_jumped_ago = 0

        if top:
            self.velocity[1] = 0
        if left or right:
            self.velocity[0] = 0


    def attack(self, player):
        return
        if self.health == 0:
            self.attacked_ago = 0
            return
        if self.attacked_ago < self.ATTACK_COOLDOWN:
            return

        self.attacked_ago = 0
        self.attack_arc_end_deg += 15
        x_start = None
        x_end = None
        y_start = y_end  = self.rect.y + 15


        if self.direction:
            # looking right
            x_start = self.rect.x + self.rect.width
            x_end = x_start + 40
        else:
            # looking left
            x_start = self.rect.x
            x_end = x_start - 20

        if len(player.rect.clipline(x_start, y_start, x_end, y_end)) > 0:
            player.take_damage(-10)
