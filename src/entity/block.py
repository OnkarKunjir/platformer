from src.entity.entity import Entity


class Block(Entity):
    def __init__(self, x, y, width, height, block_type):
        super().__init__(x, y, width, height)
        self.block_type = block_type
