from src.entity.entity import check_collision
from src.entity.character import Character
from src.entity.reward import Reward

class Player(Character):
    '''
    player extended form entity contains all state variables required by the player.
    handels jumping and moving also.
    '''
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.move_direction = {
            'left' : False,
            'right' : False,
            'up' : False
        }


    def update_pos_from_collision(self, check_against, max_x = None, max_y = None):
        '''
        function updates the position of primary entity based on collision detection.
        '''

        score = 0
        move = self.velocity
        self.move_x(move[0])
        colliding_entities = check_collision(self, check_against, max_x, max_y)

        left = False
        right = False
        top = False
        bottom = False

        for i in colliding_entities:
            if isinstance(i, Reward):
                if i.is_valid:
                    score += i.score_gain
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
        colliding_entities = check_collision(self, check_against, max_x, max_y)

        for i in colliding_entities:
            if isinstance(i, Reward):
                if i.is_valid:
                    score += i.score_gain
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

    def move(self, blocks):
        '''
        moves the player according to move_direction.
        '''
        self.velocity[1] += self.GRAVITY

        if self.move_direction['up'] and (not self.in_mid_air or self.jump_count < self.MAX_JUMP_COUNT):
            self.jump()
        self.move_direction['up'] = False

        if self.move_direction['left']:
            self.velocity[0] -= self.VELOCITY_X_INC
            self.direction = False
        if self.move_direction['right']:
            self.velocity[0] += self.VELOCITY_X_INC
            self.direction = True

        if not self.move_direction['left'] and not self.move_direction['right']:
            self.velocity[0] = 0

        for i in range(2):
            if self.velocity[i] > self.MAX_VELOCITY[i]:
                self.velocity[i] = self.MAX_VELOCITY[i]
            elif self.velocity[i] < -self.MAX_VELOCITY[i]:
                self.velocity[i] = -self.MAX_VELOCITY[i]

        left, right, top, bottom, score= self.update_pos_from_collision(blocks)
        # stop player from moving out of map.
        self.rect.x = max(0, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        if top:
            # stop jumping if player collides his head on another entity.
            self.velocity[1] = 0

        self.landed = False
        if self.in_mid_air and bottom:
            self.landed = True

        self.in_mid_air = not bottom
        if not self.in_mid_air:
            self.jump_count = 0

        return score
