import pygame
from scripts.settings import *
from scripts.utils import *
from scripts.entities import Player
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption('Temple Shooter')

        self.assets = {
            'background': load_image('background.png')
        }

        self.running = True

        self.player = Player(self, (50, 50))

        self.tilemap = Tilemap(self)

        self.scroll = [0, 0]

        self.clock = pygame.time.Clock()
    
    def run(self):
        while self.running:
            self.clock.tick(FPS)

            #Define margins
            margin_x = 100  # Horizontal margin

            #Update scroll in x direction
            if self.player.rect().centerx < self.scroll[0] + WIDTH / 2 - margin_x:
                self.scroll[0] += (self.player.rect().centerx - (self.scroll[0] + WIDTH / 2 - margin_x)) / 10
            elif self.player.rect().centerx > self.scroll[0] + WIDTH / 2 + margin_x:
                self.scroll[0] += (self.player.rect().centerx - (self.scroll[0] + WIDTH / 2 + margin_x)) / 10
            
            #Update scroll in y direction
            self.scroll[1] += (self.player.rect().centery - HEIGHT / 2 - self.scroll[1]) / 10

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.win.blit(self.assets['background'], (0, 0))

            self.tilemap.draw(self.win, offset=render_scroll)

            #self.player.update(self.tilemap)
            self.player.update_sprite()
            self.player.draw(self.win, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                self.player.handle_movement(event)
                self.player.handle_controls(event)
            
            pygame.display.flip()
        
        quit()

if __name__ == '__main__':
    game = Game()
    game.run()