from src.entity.entity import Entity

class AnimatedEntity(Entity):
    def __init__(self, x, y, width, height, n_frames):
        super().__init__(x, y, width, height)
        self.current_frame = 0
        self.n_frames = n_frames


    def update_frame(self):
        self.current_frame += 1
        if self.current_frame >= self.n_frames:
            self.current_frame = 0
