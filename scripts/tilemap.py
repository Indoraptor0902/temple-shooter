import pygame
import json
from scripts.settings import *
from scripts.utils import *

NEIGHBOR_OFFSETS = [(0, 0), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
TEST_NEIGHBOR_OFFSETS = [(0, 0), (0, 2), (2, 2), (2, 0), (2, -2), (0, -2), (-2, -2), (-2, 0), (-2, 2)]
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=TILE_SIZE):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        self.sprites = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone')
        }
    
    def save(self, file_name):
        f = open(BASE_MAP_PATH + file_name, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': TILE_SIZE, 'offgrid': self.offgrid_tiles}, f)
        f.close()
    
    def load(self, file_name):
        f = open(BASE_MAP_PATH + file_name, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.offgrid_tiles = map_data['offgrid']
    
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
    
    def draw(self, win, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            win.blit(self.sprites[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // TILE_SIZE, (offset[0] + WIDTH) // TILE_SIZE + 1):
            for y in range(offset[1] // TILE_SIZE, (offset[1] + HEIGHT) // TILE_SIZE + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    win.blit(self.sprites[tile['type']][tile['variant']], (tile['pos'][0] * TILE_SIZE - offset[0], tile['pos'][1] * TILE_SIZE - offset[1]))