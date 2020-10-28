from pygame import Rect


class Entity:
    def __init__(self, x, y, width, height, color):
        self.color = color
        self.rect = Rect(x, y, width, height)

    def set_pos(self, pos):
        '''
        set x,y to new position pos = (x, y)
        '''
        self.rect.x, self.rect.y = pos

    def move_x(self, dist):
        self.rect.x += dist
    def move_y(self, dist):
        self.rect.y += dist
