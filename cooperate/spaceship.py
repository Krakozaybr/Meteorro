import math
import images
import pygame
import pygame.display
import entities
import Config
from general import getNextCoordsByDirection
from meteor import Meteor
from entity import Entity

def abs(value):
    if (value < 0):
        return -value
    else: return value

class SpaceShip(Entity):
    def __init__(self, sourceImage, x, y):
        self.sourceImage = sourceImage
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        self.attack = 0
        self.position = (x, y)
        self.currentImage = sourceImage
        self.radius = 95 / 2
        self.bullets = []
        self.reload = 0
        self.fullReload = 300
        self.maxhealth = 200
        self.health = self.maxhealth
        self.isAlive = True
        self.createHealthBar()
        self.startParticlePosition = (0, 0)
        self.particleDirection = 0
        self.particleFullReload = 50
        self.particleReload = self.particleFullReload
        self.rotation = 0
        self.movementX = 0
        self.movementY = 0
        self.degreesOfRotation = 135 / Config.FPS
        self.center = (self.x + Config.spaceship_size[0] / 2, self.y + Config.spaceship_size[1] / 2)
        self.startBulletPosition = (self.center[0], self.y)

    def getImage(self):
        return self.currentImage

    def getPosition(self):
        return self.position

    def createHealthBar(self):
        healthBarPosition = (self.x, self.y + Config.spaceship_height + 10)
        self.healthBar = pygame.Rect(healthBarPosition, (Config.spaceship_width, 10))

    def translate(self, x, y):
        self.position = (self.x + x, self.y + y)

    def draw(self, window):
        window.blit(self.currentImage, self.position)

    def drawHealth(self, window):
        pygame.draw.rect(window, (0, 255, 0), self.healthBar)

    def refreshPosition(self):
        self.position = (self.x, self.y)

    def refreshImage(self):
        if self.rotation > 180:
            self.rotation += -360
        elif self.rotation < -180:
            self.rotation += 360
        self.currentImage = pygame.transform.rotate(self.sourceImage, self.rotation)

    def checkBounds(self):
        if self.x < 0: self.x = 0
        if self.x > Config.WIDTH - Config.spaceship_width: self.x = Config.WIDTH - Config.spaceship_width
        if self.y < 0: self.y = 0
        if self.y > Config.HEIGHT - Config.spaceship_height: self.y = Config.HEIGHT - Config.spaceship_height
        self.refreshPosition()

    def render(self, window):
        if self.isAlive:
            self.move()
            self.draw(window)
            self.checkReload()
            self.drawHealth(window)
            self.addParticles()
            if self.checkShot():
                self.shot()
            bulletsClone = self.bullets.copy()
            for bullet in bulletsClone:
                if bullet.isAlive:
                    bullet.render(window)
                else:
                    self.bullets.remove(bullet)
                    del bullet
            self.update()
        else:
            self.isAlive = True
            self.x = self.startX
            self.y = self.startY
            self.refreshPosition()
            self.health = self.maxhealth

    def update(self):
        self.healthBar.x = self.x
        self.healthBar.y = self.y
        self.healthBar.width = Config.spaceship_width * self.health / self.maxhealth

    def addParticles(self):
        def toRadians(deg):
            return deg / math.pi
        def toDeg(rad):
            return rad * 180 / math.pi
        def reverse(deg):
            if deg >= 0: return deg - 180
            else: return deg + 180
        if self.particleReload <= 0:
            entities.effects.directedEffect(self.startParticlePosition, self.particleDirection)
            self.particleReload = self.particleFullReload
        else:
            self.particleReload -= 1000 / Config.FPS
    def move(self):
        pass

    def checkReload(self):
        if self.reload > 0:
            self.reload -= 1000 / 60
        if self.reload < 0:
            self.reload = 0

    def checkShot(self):
        pass

    def shot(self):
        self.reload = self.fullReload
        self.bullets.append(Bullet((255, 0, 0), self, self.rotation))

    def updateParticleStartPosition(self, rotation):
        self.updateCenter()
        self.startBulletPosition = getNextCoordsByDirection(rotation, self.center[0])
        self.startParticlePosition = (self.center[0], self.center[1])
        self.updateParticleDirection(rotation)

    def updateParticleDirection(self, rotation):
        self.particleDirection += rotation
        if self.particleDirection > 180:
            self.particleDirection += -360
        elif self.particleDirection < -180:
            self.particleDirection += 360

    def updateCenter(self):
        self.center = (self.x + Config.spaceship_size[0] / 2, self.y + Config.spaceship_size[1] / 2)


class Bullet:
    def __init__(self, color, master, direction):
        self.color = color
        self.master = master
        self.direction = direction
        self.x = master.x + Config.spaceship_size[0] / 2 - Config.bullet_size[0]
        self.y = master.y + Config.spaceship_size[1] / 2 - Config.bullet_size[1]
        self.position = master.getPosition()
        self.speed = 20
        self.createImg()
        self.isAlive = True
        self.damage = 45 + master.attack

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def render(self, window):
        if self.x > Config.WIDTH or self.x < 0: self.isAlive = False
        if self.y > Config.HEIGHT or self.y < 0: self.isAlive = False
        if self.isAlive:
            self.move()
            self.draw(window)
            self.checkCollision()

    def checkCollision(self):
        for entity in entities.entities:
            if isinstance(entity, SpaceShip) and entity.checkCollision(self.position) and entity != self.master:
                entity.takeDamage(self.damage)
                self.isAlive = False
            elif isinstance(entity, Meteor) and entity.checkCollision(self.position):
                entity.takeDamage(self.damage)
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
        self.refreshPosition()

    def refreshPosition(self):
        self.position = (self.x, self.y)

    def createImg(self):
        self.img = pygame.transform.rotate(images.bullet, self.direction)