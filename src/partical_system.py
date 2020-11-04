import random
class Particle:
    def __init__(self, x, y, radius, vx, vy, color = (255, 255, 255)):
        '''
        particle is fundamental component of particle system.
        on screen particles are as cricle at x,y cooridate of radius 'radius'
        '''
        self.center = [x, y]
        self.radius = radius
        self.color = color

        self.vx = vx
        self.vy = vy
        self.gravity = 0.07 * abs(vy)
        self.shrink_rate = radius * 0.01

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
        self.max_particles = 100
        self.particles = [
            Particle(0, 0, 10, 1, -5),
        ]

    def update(self):
        for particle in self.particles:
            particle.update()

    def add(self, x,y):
        index = -1
        if len(self.particles) < self.max_particles:
            self.particles.append(Particle(x+random.randint(-5,5), y, 10, random.randint(1,5), -9))
        else:
            for i in range(len(self.particles)):
                if self.particles[i].radius == 0:
                    index = i
                    break

            if index > -1:
                self.particles[index] = Particle(x+random.randint(-5,5), y, 10, random.randint(1,5), -9)
