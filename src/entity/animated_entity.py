from src.entity.entity import Entity

class AnimatedEntity(Entity):
    def __init__(self, x, y, width, height, n_frames, update_per_frame = 10):
        '''
        n_frames =          total number of frames included in animation.
        update_per_frame =  number of frames to wait to update the current frame.
        '''
        super().__init__(x, y, width, height)
        self.current_frame = 0
        self.n_frames = n_frames
        self.update_per_frame = update_per_frame
        self.frame_count = 0


    def update_frame(self):
        '''
        function updates the current frame number.
        '''
        self.frame_count += 1
        if self.frame_count < self.update_per_frame:
            return

        self.frame_count = 0
        self.current_frame += 1
        if self.current_frame >= self.n_frames:
            self.current_frame = 0
