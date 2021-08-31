from math import sqrt

class Entity:

    def takeDamage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
            self.diy()

    def diy(self):
        self.isAlive = False

    def checkCollision(self, position):
        return sqrt(abs(position[0] - self.x) ** 2 + abs(position[1] - self.y) ** 2) < self.radius