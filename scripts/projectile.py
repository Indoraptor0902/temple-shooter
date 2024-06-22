import pygame
from scripts.utils import *


class Projectile:
    def __init__(self, game, pos, direction, entity):
        self.game = game
        
        self.pos = list(pos)

        self.direction = direction
        self.movement = [0, 0]

        self.sprites = {'left': flip_img(load_image('projectile.png')), 'right': load_image('projectile.png')}
        self.sprite = self.sprites[self.direction]

        self.offset = entity.image.get_height() / 2 - self.sprite.get_height() / 2
        self.pos[1] += self.offset

        if self.direction == 'left':
            self.movement[0] = -1
        elif self.direction == 'right':
            self.movement[0] = 1

        self.speed = 15 * self.movement[0]
    
    def move(self):
        self.pos[0] += self.speed
    
    def draw(self, win, offset=(0, 0)):
        win.blit(self.sprite, (self.pos[0] - offset[0], self.pos[1] - offset[1]))