import random
class Camera:
    def __init__(self, player, x = 0, y = 0, fx = 0, fy = 0, smooth = 1):
        '''
        player = Entity to be tracked with camera.
        x,y = initial camera coordinates.
        fx, fy = coordinates of point to focus on.
        smooth = factor used to smoothout camera movement.
        '''
        self.player = player
        self.x = x
        self.y = y
        self.fx = fx
        self.fy = fy
        self.smooth = smooth

    def follow(self):
        self.x += (self.player.rect.x - self.x - self.fx)//self.smooth
        self.y += (self.player.rect.y - self.y - self.fy)//self.smooth

    def translate(self, rect):
        return (rect.x - self.x, rect.y - self.y, rect.width, rect.height)

    def translate_xy(self, location):
        return (location[0]-self.x, location[1]-self.y)
