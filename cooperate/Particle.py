import random
import Config
import images
import pygame
import entities


class Effects:
    def explosionEffect(self, pos, particlesCount=5):
        for i in range(0, particlesCount):
            entities.particles.append(Particle(random.randint(-180, 180), pos))

    def directedEffect(self, pos, direction, particlesCount=1):
        for i in range(0, particlesCount):
            particle = Particle(direction + random.randint(-30, 30), pos)
            particle.size = random.randint(2, 5)
            particle.liveTime = 300
            entities.particles.append(particle)


class Particle:
    def __init__(self, direction, startPosition):
        self.startPosition = startPosition
        self.x = startPosition[0]
        self.y = startPosition[1]
        self.speed = random.randint(1, 2)
        self.direction = direction
        self.size = random.randint(15, 35)
        self.image = pygame.transform.rotate(pygame.transform.scale(images.particle, (self.size, self.size)), random.randint(0, 360))
        self.liveTime = 1000
        self.isAlive = True

    def render(self, window):
        self.draw(window)
        self.move()
        self.checkTime()

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def checkTime(self):
        self.liveTime -= 1000 / Config.FPS
        if self.liveTime <= 0:
            self.isAlive = False

    def move(self):
        def reverse(deg):
            if deg > 90: return 180 - deg
            if deg < -90: return -180 - deg

        d = self.direction
        movementX = 0
        movementY = 0
        if d <= 90 and d >= -90:
            movementX = self.speed * -d / 90
        else:
            movementX = self.speed * -reverse(d) / 90
        if d >= 0:
            movementY = self.speed * (90 - d) / 90
        elif d < 0:
            movementY = self.speed * (90 + d) / 90
        self.x += movementX
        self.y -= movementY