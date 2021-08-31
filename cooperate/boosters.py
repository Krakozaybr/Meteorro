import pygame
import entities
import Config
import random
import images
from spaceship import SpaceShip
from Particle import Effects


class Booster:
    def __init__(self):
        self.liveTime = 5000
        self.isAlive = True
        self.x = random.randint(0 + Config.booster_size[0], Config.WIDTH - Config.booster_size[0])
        self.y = random.randint(0 + Config.booster_size[1], Config.HEIGHT - Config.booster_size[1])

    def render(self, window):
        self.draw(window)
        self.checkCollision()
        self.tick()
        self.checkDeath()

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def checkCollision(self):
        for entity in entities.entities:
            if isinstance(entity, SpaceShip) and entity.checkCollision((self.x, self.y)):
                self.effect(entity)

    def diy(self):
        self.isAlive = False
        Config.effects.explosionEffect((self.x, self.y))

    def effect(self, entity):
        pass

    def tick(self):
        if self.liveTime < 1000 / Config.FPS:
            self.liveTime = 0
        else:
            self.liveTime -= 1000 / Config.FPS

    def checkDeath(self):
        if self.liveTime <= 0:
            self.diy()


class HealingBooster(Booster):
    def __init__(self):
        super().__init__()
        self.image = images.healingBooster
        self.healing = Config.healing_of_healing_booster

    def effect(self, entity):
        if entity.health + self.healing > entity.maxhealth:
            entity.health = entity.maxhealth
        else:
            entity.health += self.healing
        self.diy()

class AttackBooster(Booster):
    def __init__(self):
        super().__init__()
        self.image = images.attackBooster
        self.attack = Config.attack_boost_of_attack_booster
        self.isBoosting = False
        self.master = None
        self.explosions = 0

    def render(self, window):
        if not self.isBoosting:
            self.draw(window)
            self.checkCollision()
        self.tick()

    def checkCollision(self):
        for entity in entities.entities:
            if isinstance(entity, SpaceShip) and entity.checkCollision((self.x, self.y)):
                self.startBoosting(entity)
                Config.effects.explosionEffect((self.x, self.y))

    def diy(self):
        self.isAlive = False
        if not self.isBoosting:
            Config.effects.explosionEffect((self.x, self.y))
        else:
            self.master.attack = 0

    def tick(self):
        if self.liveTime < 1000 / Config.FPS:
            self.liveTime = 0
            self.diy()
        else:
            self.liveTime -= 1000 / Config.FPS

    def startBoosting(self, entity):
        self.master = entity
        self.liveTime = 10000
        self.isBoosting = True
        self.master.attack = 40

class ReloadBooster(Booster):
    def __init__(self):
        super().__init__()
        self.image = images.reloadBooster
        self.isBoosting = False
        self.master = None
        self.explosions = 0
        self.masterMaxReload = 0

    def render(self, window):
        if not self.isBoosting:
            self.draw(window)
            self.checkCollision()
        self.tick()

    def checkCollision(self):
        for entity in entities.entities:
            if isinstance(entity, SpaceShip) and entity.checkCollision((self.x, self.y)):
                self.startBoosting(entity)
                Config.effects.explosionEffect((self.x, self.y))

    def diy(self):
        self.isAlive = False
        if not self.isBoosting:
            Config.effects.explosionEffect((self.x, self.y))
        else:
            self.master.fullReload = self.masterMaxReload

    def tick(self):
        if self.liveTime < 1000 / Config.FPS:
            self.liveTime = 0
            self.diy()
        else:
            self.liveTime -= 1000 / Config.FPS

    def startBoosting(self, entity):
        self.master = entity
        self.liveTime = 10000
        self.isBoosting = True
        self.masterMaxReload = self.master.fullReload
        self.master.fullReload = self.masterMaxReload / 2