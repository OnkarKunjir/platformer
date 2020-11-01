class Camera:
    def __init__(self, player, x = 0, y = 0, fx = 0, fy = 0, smooth = 1):
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
