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

        self.clock = pygame.time.Clock()
    
    def run(self):
        while self.running:
            self.clock.tick(FPS)

            self.win.blit(self.assets['background'], (0, 0))

            self.tilemap.draw(self.win)

            #self.player.update(self.tilemap)
            self.player.update_sprite()
            self.player.draw(self.win)

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