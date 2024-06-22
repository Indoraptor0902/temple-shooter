#SOFT SCROLLING BACKGROUND WITH MARGIN OLD CODE

#best working code so far
'''if self.player.pos[0] + self.player.anim_offset[0] - int(self.scroll[0]) <= WIDTH / 3:
    self.scroll[0] += (self.player.rect().left - WIDTH / 3 - self.scroll[0]) / 10
elif self.player.pos[0] + self.player.anim_offset[0] - int(self.scroll[0]) >= WIDTH / 1.5:
    self.scroll[0] += (self.player.rect().centerx - WIDTH / 1.5 - self.scroll[0]) / 20'''

'''print("pos in world: ", self.player.pos)
print("pos on screen: ", self.player.pos[0] + self.player.anim_offset[0] - int(self.scroll[0]))'''

#self.scroll[0] += (self.player.rect().centerx - WIDTH / 2 - self.scroll[0]) / 10