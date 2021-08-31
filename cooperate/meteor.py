import pygame
import Config
import random
import math
import entities
from entity import Entity

class Meteor(Entity):
    def __init__(self, img):
        self.x = random.randint(0, Config.WIDTH)
        self.y = 0
        self.size = random.randint(20, 65)
        self.speed = random.randint(3, 5)
        self.damage = self.size * self.speed / 10
        self.mass = self.size ** 2
        self.kineticStrong = self.mass * self.speed
        self.startPosition = (self.x, self.y)
        self.img = pygame.transform.rotate(pygame.transform.scale(img, (self.size, self.size)), random.randint(0, 360))
        self.direction = random.choice([random.randint(-180, -100), random.randint(100, 180)])
        self.isAlive = True
        self.radius = 47
        self.maxhealth = self.size * 3
        self.health = self.maxhealth
        self.baseRotation = random.randint(1, 10)
        self.contacts = []

    def render(self, window):
        self.move()
        self.draw(window)
        self.checkBorders()
        self.checkBeat()
        self.checkHealth()
        self.updateContacts()

    def updateContacts(self):
        clone = self.contacts.copy()
        for contact in clone:
            if contact[1] < 1000 / Config.FPS:
                self.contacts.remove(contact)
            else: contact[1] -= 1000 / Config.FPS

    def checkBeat(self):
        clone = entities.entities.copy()
        for entity in clone:
            if not isinstance(entity, Meteor) and entity.checkCollision((self.x, self.y)):
                entity.takeDamage(self.damage)
                self.diy()
            elif isinstance(entity, Meteor) and entity.checkCollisionWithAnotherMeteor(self) and entity != self:
                isContacted = False
                for contact in self.contacts:
                    if contact[0] == entity: isContacted = True
                if not isContacted:
                    entity.beat(self)
                    self.beat(entity)

    def beat(self, another):
        self.contacts.append([another, 500])
        def getDifferenceBetweenDegrees(deg1, deg2):
            if deg1 < 0: deg1 = 360 + deg1
            if deg2 < 0: deg2 = 360 + deg2
            return deg1 - deg2
        aks = another.kineticStrong
        self.direction += getDifferenceBetweenDegrees(self.direction, another.direction) * (self.kineticStrong + aks) / aks
        self.fixDirection()

    def checkCollisionWithAnotherMeteor(self, another):
        return math.sqrt(abs(another.x - self.x) ** 2 + abs(another.y - self.y) ** 2) <= self.radius + another.radius

    def fixDirection(self):
        while self.direction > 180:
            self.direction += -360
        while self.direction < -180:
            self.direction += 360

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def diy(self):
        self.addDeathParticles()
        self.isAlive = False

    def move(self):
        self.fixDirection()
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

    def checkBorders(self):
        if self.x > Config.WIDTH + self.size or self.x < -self.size:
            self.isAlive = False
        if self.y > Config.HEIGHT + self.size or self.y < -self.size:
            self.isAlive = False

    def checkHealth(self):
        if self.health <= 0:
            self.diy()

    def addDeathParticles(self):
        entities.effects.explosionEffect((self.x, self.y))
