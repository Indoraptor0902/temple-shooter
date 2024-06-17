import pygame
import os
from scripts.settings import *
from scripts.colors import *

pygame.init()

BASE_IMG_PATH = 'data/images/'

def flip_img(sprite):
    return pygame.transform.flip(sprite, True, False)

def flip_images(sprites):
    return [flip_img(sprite) for sprite in sprites]

def load_image(path):
    unscaled_img = pygame.image.load(BASE_IMG_PATH + path)
    img = pygame.transform.scale(unscaled_img, (unscaled_img.get_width() * IMG_SCALE, unscaled_img.get_height() * IMG_SCALE))
    img.set_colorkey(BLACK)
    return img

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images

def load_all_spritesheets(path):
    new_path = BASE_IMG_PATH + path

    all_sprites = {}

    anim_states = [folder for folder in os.listdir(new_path) if os.path.isdir(os.path.join(new_path, folder))]

    for anim_state in anim_states:
        images = load_images(os.path.join(path, anim_state).replace('\\', '/'))
        
        all_sprites[anim_state + '_right'] = images
        all_sprites[anim_state + '_left'] = flip_images(images)
    
    return all_sprites

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]