from src.entity.entity import check_collision
from src.entity.character import Character
from src.entity.reward import Reward
import random

class Enemy(Character):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        # constants
        self.JUMP_COOLDOWN = 15

        self.color = color
        self.x_offset = 80
        self.first_jumped_ago = 0

    def update_pos_from_collision(self, check_against, max_x = None, max_y = None):
        '''
        function updates the position of primary entity based on collision detection.
        '''
        move = self.velocity
        self.move_x(move[0])
        colliding_entities = check_collision(self, check_against, max_x, max_y)

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
        colliding_entities = check_collision(self, check_against, max_x, max_y)

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
            elif enemy_x < player_x:
                self.velocity[0] += self.VELOCITY_X_INC
        else:
            self.velocity[0] = 0

        if (enemy_y > player_y) and (self.first_jumped_ago == 0):
            self.jump()

        self.cap_velocity()
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
