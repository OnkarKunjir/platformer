from src.entity.block import Block


class Reward(Block):
    def __init__(self, x, y, width, height, block_type, health_gain, score_gain):
        super().__init__(x, y, width, height, block_type)
        self.is_valid = True
        self.health_gain = health_gain
        self.score_gain = score_gain
