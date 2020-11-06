from src.entity.block import Block

class Reward(Block):
    def __init__(self, x, y, width, height, block_type):
        super().__init__(x, y, width, height, block_type)
        self.is_valid = True
