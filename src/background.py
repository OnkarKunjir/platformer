from src.entity.entity import Entity

class Background:
    def __init__(self):
        self.level_1 = [
            Entity(x = 100, y = 100, width = 100, height = 300),
            Entity(x = 300, y = 100, width = 100, height = 300),
            Entity(x = 500, y = 100, width = 100, height = 300),
        ]
        self.level_2 = [
            Entity(x = 200, y = 200, width = 100, height = 300),
            Entity(x = 400, y = 80, width = 100, height = 300),
            Entity(x = 700, y = 110, width = 100, height = 300),
        ]
        self.levle_1_distance = 0.5
        self.levle_2_distance = 0.25
