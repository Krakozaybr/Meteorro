import pygame

# Window
HEIGHT = 500
WIDTH = 900
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 60

# Spaceships
spaceship_width = 55
spaceship_height = 55
spaceship_health = 200
spaceship_size = (spaceship_width, spaceship_height)
bullet_size = (13, 20)

# Boosters
booster_size = (35, 35)
booster_live_time = 5000  # == 5s
allow_multiply_effect_of_one_booster = True
allow_multiply_effect_of_different_boosters = True

# Healing booster
healing_booster_size = booster_size
healing_booster_live_time = booster_live_time
healing_of_healing_booster = 40

# Attack booster
attack_booster_size = booster_size
attack_booster_live_time = booster_live_time
attack_boost_of_attack_booster = 50

# Reload booster
reload_booster_size = booster_size
reload_booster_live_time = booster_live_time
reload_boost_of_reload_booster = 2