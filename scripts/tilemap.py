import pygame
from scripts.settings import *
from scripts.utils import load_images

NEIGHBOR_OFFSETS = [(0, 0), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=TILE_SIZE):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}

        self.sprites = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone')
        }

        for i in range(10):
            self.tilemap[str(3 + i) + ';8'] = {'type': 'grass', 'variant': 1, 'pos': [3 + i, 8]}
            self.tilemap['9;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': [9, 5 + i]}
    
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * TILE_SIZE, tile['pos'][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects
    
    def draw(self, win):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            win.blit(self.sprites[tile['type']][tile['variant']], (tile['pos'][0] * TILE_SIZE, tile['pos'][1] * TILE_SIZE))