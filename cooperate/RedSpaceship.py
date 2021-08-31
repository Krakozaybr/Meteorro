import pygame
import pygame.display
import Config

from spaceship import SpaceShip

class RedSpaceShip(SpaceShip):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.speed = 5
        self.particleDirection = 180
        self.startParticlePosition = (x + Config.spaceship_size[0] / 2, y + Config.spaceship_size[1])

    def move(self):
        def reverse(deg):
            if deg > 90: return 180 - deg
            if deg < -90: return -180 - deg
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotation += self.degreesOfRotation
            self.updateParticleStartPosition(self.degreesOfRotation)
        if keys[pygame.K_RIGHT]:
            self.rotation += -self.degreesOfRotation
            self.updateParticleStartPosition(-self.degreesOfRotation)
        if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            d = self.rotation
            if d <= 90 and d >= -90:
                self.movementX = self.speed * -d / 90
            else:
                self.movementX = self.speed * -reverse(d) / 90
            if d >= 0:
                self.movementY = self.speed * (90 - d) / 90
            elif d < 0:
                self.movementY = self.speed * (90 + d) / 90
            if keys[pygame.K_UP]:
                self.x += self.movementX
                self.y -= self.movementY
            if keys[pygame.K_DOWN]:
                self.x -= self.movementX
                self.y += self.movementY
        self.updateParticleStartPosition(0)
        self.checkBounds()
        self.refreshImage()
        self.refreshPosition()

    def checkShot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.reload == 0:
            return True
        else:
            return False
