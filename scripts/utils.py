import pygame
import os
from scripts.settings import *
from scripts.colors import *

pygame.init()

BASE_IMG_PATH = 'data/images/'
BASE_MAP_PATH = 'data/maps/'

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
    def __init__(self, sprites, img_dur=5):
        self.sprites = sprites
        self.img_dur = img_dur
        self.frame = 0
    
    def copy(self):
        return Animation(self.sprites, self.img_dur)
    
    def update(self):
        self.frame = (self.frame + 1) % (self.img_dur * len(self.sprites))
    
    def img(self):
        return self.sprites[int(self.frame / self.img_dur)]