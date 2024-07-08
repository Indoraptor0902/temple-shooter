#SOFT SCROLLING BACKGROUND WITH MARGIN OLD CODE

#best working code so far
'''if self.player.pos[0] + self.player.anim_offset[0] - int(self.scroll[0]) <= WIDTH / 3:
    self.scroll[0] += (self.player.rect().left - WIDTH / 3 - self.scroll[0]) / 10
elif self.player.pos[0] + self.player.anim_offset[0] - int(self.scroll[0]) >= WIDTH / 1.5:
    self.scroll[0] += (self.player.rect().centerx - WIDTH / 1.5 - self.scroll[0]) / 20'''

'''print("pos in world: ", self.player.pos)
print("pos on screen: ", self.player.pos[0] + self.player.anim_offset[0] - int(self.scroll[0]))'''

#self.scroll[0] += (self.player.rect().centerx - WIDTH / 2 - self.scroll[0]) / 10



#DRAWING TILEMAP WITHOUT OPTIMIZATION OLD CODE

'''for loc in self.tilemap:
    tile = self.tilemap[loc]
    win.blit(self.sprites[tile['type']][tile['variant']], (tile['pos'][0] * TILE_SIZE - offset[0], tile['pos'][1] * TILE_SIZE - offset[1]))'''



#INITIAL TESTING CODE FOR TILEMAP

'''for i in range(50):
    self.tilemap[str(-5 + i) + ';8'] = {'type': 'grass', 'variant': 1, 'pos': [-5 + i, 8]}
    self.tilemap['9;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': [9, 5 + i]}'''