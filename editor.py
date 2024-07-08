import pygame
from scripts.settings import *
from scripts.utils import *
from scripts.tilemap import Tilemap
import math


class Editor:
    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption('Level Editor')

        self.tilemap = Tilemap(self)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.assets = {tile_type: self.tilemap.sprites[tile_type] for tile_type in self.tilemap.sprites}

        self.running = True

        self.movement = [False, False, False, False]

        self.clock = pygame.time.Clock()

        self.scroll = [0, 0]
        self.velocity = 5

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False

        self.ongrid = True
    
    def run(self):
        while self.running:
            self.clock.tick(FPS)

            self.win.fill(BLACK)

            self.scroll[0] += (self.movement[1] - self.movement[0]) * self.velocity
            self.scroll[1] += (self.movement[3] - self.movement[2]) * self.velocity

            self.tilemap.draw(self.win, self.scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            tile_pos = (int((mpos[0] + self.scroll[0]) // TILE_SIZE), int((mpos[1] + self.scroll[1]) // TILE_SIZE))

            if self.ongrid:
                self.win.blit(current_tile_img, (tile_pos[0] * TILE_SIZE - self.scroll[0], tile_pos[1] * TILE_SIZE - self.scroll[1]))
            else:
                self.win.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': list(tile_pos)}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_rect = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_height(), tile_img.get_height())
                    if tile_rect.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            
            pygame.display.flip()
        
        quit()

if __name__ == '__main__':
    editor = Editor()
    editor.run()