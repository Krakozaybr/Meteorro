import pygame
import pygame.display
import Config
import random
import images
import boosters
import entities
from spaceship import SpaceShip
from Particle import Effects
from meteor import Meteor
from YellowSpaceship import YellowSpaceShip
from RedSpaceship import RedSpaceShip

redSpaceship = RedSpaceShip(images.redSpaceship,
                            Config.WIDTH - Config.spaceship_width - 20, Config.spaceship_height + 20)
yellowSpaceship = YellowSpaceShip(images.yellowSpaceship,Config.spaceship_width + 20,
                                  Config.HEIGHT - Config.spaceship_height - 20)
entities.entities.append(redSpaceship)
entities.entities.append(yellowSpaceship)
window = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
pygame.display.set_caption('very good game')
Config.effects = Effects()
players = []

pygame.font.init()


def main():
    run = True
    clock = pygame.time.Clock()
    while(run):
        clock.tick(Config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        drawWindow()
        addMeteors()
        addBoosters()


def drawWindow():
    window.blit(images.spaceImg, (0, 0))
    drawParticles()
    drawBoosters()
    drawEntities()
    pygame.display.update()


def drawParticles():
    clone = entities.particles.copy()
    for particle in clone:
        if particle.isAlive:
            particle.render(window)
        else:
            entities.particles.remove(particle)
            del particle


def drawEntities():
    copy = entities.entities.copy()
    for i in range(0, len(entities.entities)):
        entity = copy[i]
        if entity.isAlive:
            entity.render(window)
        else:
            if not isinstance(entity, SpaceShip):
                entities.entities.remove(entity)
                del entity
            else:
                entity.render(window)


def drawBoosters():
    copy = entities.boosters.copy()
    for i in range(0, len(entities.boosters)):
        booster = copy[i]
        if booster.isAlive:
            booster.render(window)
        else:
            entities.boosters.remove(booster)
            del booster


def addMeteors():
    if random.randint(40, 80) == 42:
        entities.entities.append(Meteor(images.getMeteor(random.randint(0, 4))))


def addBoosters():
    if random.randint(0, 300) == 42:
        entities.boosters.append(boosters.HealingBooster())
    elif random.randint(0, 300) == 42:
        entities.boosters.append(boosters.AttackBooster())
    elif random.randint(0, 300) == 42:
        entities.boosters.append(boosters.ReloadBooster())


main()