from src.entity.animated_block import AnimatedBlock


class Reward(AnimatedBlock):
    def __init__(
        self, x, y, width, height, block_type, health_gain, score_gain, n_frames=1
    ):

        super().__init__(x, y, width, height, block_type, n_frames)
        self.is_valid = True
        self.health_gain = health_gain
        self.score_gain = score_gain
