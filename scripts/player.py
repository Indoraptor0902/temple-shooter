import pygame
from scripts.utils import load_image, load_all_spritesheets

class Player:
    def __init__(self, game, pos):
        self.game = game
        
        self.pos = list(pos)

        self.sprites = load_all_spritesheets('entities/player')
        self.direction = 'right'
        self.action = 'idle'
        self.state = self.action + '_' + self.direction
        self.image = self.sprites[self.state][0]
        self.image = load_image('entities/player.png')
        self.size = [self.image.get_width(), self.image.get_height()]

        self.movement = [0, 0]
        self.velocity = [0, 0]
        self.speed = 5

        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.anim_offset = (-3, -3)
        self.animation_duration = 5
        self.frame = 0
        self.air_time = 0
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.frame = 0
    
    def handle_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.movement[0] += -1
            if event.key == pygame.K_RIGHT:
                self.movement[0] += 1
            if event.key == pygame.K_UP:
                self.velocity[1] = -8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.movement[0] -= -1
            if event.key == pygame.K_RIGHT:
                self.movement[0] -= 1
    
    def update(self, tilemap):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.velocity[0] = self.movement[0] * self.speed
        self.velocity[1] = min(10, self.velocity[1] + 0.3)

        self.pos[0] += self.velocity[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                if self.velocity[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += self.velocity[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                if self.velocity[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                self.pos[1] = entity_rect.y
        
        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0
    
    def update_sprite(self):
        self.air_time += 1

        self.frame = (self.frame + 1) % (self.animation_duration * len(self.sprites[self.state]))
        
        if self.collisions['down']:
            self.air_time = 0
        
        if self.air_time > 4:
            self.set_action('jump')
        elif self.movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
        
        if self.movement[0] > 0:
            self.direction = 'right'
        if self.movement[0] < 0:
            self.direction = 'left'

        self.state = self.action + '_' + self.direction
        
        self.image = self.sprites[self.state][int(self.frame / self.animation_duration)]
    
    def draw(self, win):
        win.blit(self.image, (self.pos[0] + self.anim_offset[0], self.pos[1] + self.anim_offset[1]))