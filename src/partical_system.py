import random
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
        self.gravity = 0.2
        self.shrink_rate = 0.2 + radius * 0.02

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

    def add(self, x, y, n = 1, velocity_x = 0, velocity_y = 0, min_size = 5, max_size = 8):
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

            # generating random velocity for particle.
            vx = 0
            if velocity_x != 0:
                vx = random.randint(velocity_x - 1, velocity_x + 1)

            vy = 0
            if velocity_y != 0:
                vy = random.randint(velocity_y - 1, velocity_y + 1)

            radius = random.randint(min_size, max_size)

            if len(self.particles) < self.max_particles:
                self.particles.append(Particle(x, y, radius, vx, vy))
            else:
                for i in range(len(self.particles)):
                    if self.particles[i].radius == 0:
                        index = i
                        break

                if index > -1:
                    self.particles[index] = Particle(x, y, radius, vx, vy)
