import pygame
from scripts.utils import *
from scripts.projectile import *

class Entity:
    def __init__(self, game, entity_type, pos):
        self.game = game
        
        self.pos = list(pos)

        self.entity_type = entity_type

        self.sprites = load_all_spritesheets('entities/' + self.entity_type)
        self.direction = 'right'
        self.action = 'idle'
        self.state = self.action + '_' + self.direction
        self.image = load_image('entities/player.png')
        self.size = [self.image.get_width(), self.image.get_height()]

        self.movement = [0, 0]
        self.velocity = [0, 0]
        self.speed = 5

        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.anim_offset = (-10, -10)
        self.animation_duration = 4
        self.frame = 0
        self.air_time = 0

        self.project_wpn_img = load_image('gun.png')
        self.projectiles = []
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.frame = 0
    
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
        self.frame = (self.frame + 1) % (self.animation_duration * len(self.sprites[self.state]))
        
        if self.movement[0] > 0:
            self.direction = 'right'
        if self.movement[0] < 0:
            self.direction = 'left'

        self.state = self.action + '_' + self.direction
        
        self.image = self.sprites[self.state][int(self.frame / self.animation_duration)]
    
    def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.move()
    
    def draw_projectiles(self, win):
        for projectile in self.projectiles:
            projectile.draw(win)
    
    def draw(self, win):
        win.blit(self.image, (self.pos[0] + self.anim_offset[0], self.pos[1] + self.anim_offset[1]))
        self.draw_projectiles(win)
    
    def shoot(self, entity):
        projectile = Projectile(self.game, self.pos, self.direction, entity)
        self.projectiles.append(projectile)

class Player(Entity):
    def __init__(self, game, pos):
        super().__init__(game, 'player', pos)

        self.air_time = 0
        self.jump_count = 0
    
    def handle_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.movement[0] += -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.movement[0] += 1
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.jump_count < 2:
                self.velocity[1] = -8
                self.jump_count += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.movement[0] -= -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.movement[0] -= 1
    
    def handle_controls(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pass
            if pygame.mouse.get_pressed()[2]:
                super().shoot(self)
    
    def update_sprite(self):
        super().update(self.game.tilemap)
        super().update_sprite()
        super().update_projectiles()

        self.air_time += 1
    
        if self.collisions['down']:
            self.air_time = 0
            self.jump_count = 0
        
        if self.air_time > 4:
            self.set_action('jump')
        elif self.movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')