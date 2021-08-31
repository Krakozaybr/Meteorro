import pygame
import Config

def getMeteor(n):
    if n == 0: return meteor
    elif n == 1: return meteor2
    elif n == 2: return meteor3
    else: return meteor4


attackBooster = pygame.transform.scale(pygame.image.load(r'..\Assets\boosters\attack.png'), Config.booster_size)
healingBooster = pygame.transform.scale(pygame.image.load(r'..\Assets\boosters\healing.png'), Config.booster_size)
reloadBooster = pygame.transform.scale(pygame.image.load(r'..\Assets\boosters\reload.png'), Config.booster_size)
bullet = pygame.transform.scale(pygame.image.load(r'..\Assets\bullet.png'), Config.bullet_size)
yellowSpaceship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(r'..\Assets\spaceship_yellow.png'), Config.spaceship_size), 180)
redSpaceship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(r'..\Assets\spaceship_red.png'), Config.spaceship_size), 180)
particle = pygame.image.load(r'..\Assets\particle.png')
spaceImg = pygame.image.load(r'..\Assets\space.png')
meteor = pygame.image.load(r'..\Assets\meteor.png')
meteor2 = pygame.image.load(r'..\Assets\meteor2.png')
meteor3 = pygame.image.load(r'..\Assets\meteor3.png')
meteor4 = pygame.image.load(r'..\Assets\meteor4.png')