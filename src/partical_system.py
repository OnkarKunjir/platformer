import random
# TODO: make add particle function more flexible.
class Particle:
    def __init__(self, x, y, radius, vx, vy, color = (255, 255, 255)):
        '''
        particle is fundamental component of particle system.
        on screen particles are as cricle at x,y cooridate of radius 'radius'
        '''
        self.center = [x, y]
        self.radius = radius
        self.color = random.choice([(255, 255, 255), (200, 200, 200), (150, 150, 150)])

        self.vx = vx
        self.vy = vy
        self.gravity = 0.07 * abs(vy)
        self.shrink_rate = radius * 0.03

    def update(self):
        self.center[0] += self.vx
        self.center[1] += self.vy
        self.vy += self.gravity
        self.radius -= self.shrink_rate
        self.radius = max(0, self.radius)
        if self.vy > 5:
            self.vy = 5

class ParticleSystem:
    def __init__(self):
        self.max_particles = 20
        self.particles = [
        ]

    def update(self):
        for particle in self.particles:
            particle.update()

    def add(self, x, y, n = 1, direction = True):
        '''
        adds atmost n and at lest 1 particle(s) at x,y
        with random velocity. direction = True/False = Right/Left
        '''
        orignal_x = x
        orignal_y = y
        for i in range(n):
            x = orignal_x + random.randint(-5, 5)
            y = orignal_y + random.randint(-5, 5)
            index = -1
            if direction:
                vx = random.randint(1, 2)
            else:
                vx = random.randint(-2, -1)
            vy = random.randint(-2, -1)
            radius = random.randint(5, 8)
            if len(self.particles) < self.max_particles:
                self.particles.append(Particle(x, y, radius, vx, vy))
            else:
                for i in range(len(self.particles)):
                    if self.particles[i].radius == 0:
                        index = i
                        break

                if index > -1:
                    self.particles[index] = Particle(x, y, radius, vx, vy)
