from src.entity.animated_entity import AnimatedEntity


class AnimatedBlock(AnimatedEntity):
    def __init__(self, x, y, width, height, block_type, n_frames):
        super().__init__(x, y, width, height, n_frames)
        self.block_type = block_type
