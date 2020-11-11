from src.entity.entity import check_collision
from src.entity.character import Character
from src.entity.reward import Reward

class Enemy(Character):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.color = color

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
        pass
