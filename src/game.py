import pygame
import random
from src.entity import Entity, Player
from src.utils import load_level

class Game:
    def __init__(self):

        # game configurations
        # acpect ration = 5/4
        self.DISPLAY_WIDTH = 1000
        self.DISPLAY_HEIGHT = 800

        self.RENDER_SURFACE_WIDTH = 500
        self.RENDER_SURFACE_HEIGHT = 400

        self.RENDER_SURFACE_MIDPOINT = (self.RENDER_SURFACE_WIDTH//2, 50 + self.RENDER_SURFACE_HEIGHT//2)
        self.GRAVITY = 0.2

        # pygame related initalization
        pygame.init()

        # pygame objects
        self.display = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.render_surface = pygame.Surface((self.RENDER_SURFACE_WIDTH, self.RENDER_SURFACE_HEIGHT))
        self.clock = pygame.time.Clock()

        # game state variables
        self.RENDER_FRAME = True

        # game objects
        self.player = Player(x = 10, y = 20, width = 15, height = 30, color = (255,255,255), gravity = self.GRAVITY)
        self.move = [0, 0]
        self.camera = [0, 0]

        self.blocks = load_level('dev_lvl', (20,20), (self.RENDER_SURFACE_WIDTH, self.RENDER_SURFACE_HEIGHT) )

        # assets
        self.dirt_img = pygame.image.load('assets/images/dirt.png')
        self.grass_img = pygame.image.load('assets/images/grass.png')

    def event_handler(self):
        '''
        function to handle events.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RENDER_FRAME = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # exit game on ESCAPE
                    self.RENDER_FRAME = False

                elif event.key == pygame.K_a:
                    self.player.move_direction['left'] = True

                elif event.key == pygame.K_d:
                    self.player.move_direction['right'] = True

                elif event.key == pygame.K_SPACE:
                    self.player.move_direction['up'] = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a :
                    self.player.move_direction['left'] = False
                elif event.key == pygame.K_d:
                    self.player.move_direction['right'] = False


    def update_entities(self):
        '''
        function to update position of all entities based.
        '''
        self.camera[0] = (self.player.rect.x - self.RENDER_SURFACE_MIDPOINT[0])//20
        self.camera[1] = (self.player.rect.y - self.RENDER_SURFACE_MIDPOINT[1])//20

        self.player.move(self.blocks)

        # recenter whole map including player
        for i in self.blocks:
            i.rect.x -= self.camera[0]
            i.rect.y -= self.camera[1]

        self.player.rect.x -= self.camera[0]
        self.player.rect.y -= self.camera[1]


    def draw_frame(self):
        '''
        draw all components visible in frame.
        '''
        self.render_surface.fill((135, 206, 235))
        pygame.draw.rect(self.render_surface, self.player.color, self.player.rect)

        for tile in self.blocks:
            #pygame.draw.rect(self.render_surface, tile.color, tile.rect)
            if tile.block_type == 1:
                self.render_surface.blit(self.dirt_img, tile.rect)
            elif tile.block_type == 2:
                self.render_surface.blit(self.grass_img, tile.rect)

    def play(self):
        '''
        run main game loop
        '''
        while self.RENDER_FRAME:
            self.event_handler()
            self.update_entities()
            self.draw_frame()

            scaled_surface = pygame.transform.scale(self.render_surface, (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
            self.display.blit(scaled_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def __del__(self):
        pygame.quit()
