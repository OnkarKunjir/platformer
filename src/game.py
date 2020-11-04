import pygame
import random
import configparser
from src.entity.player import Player
from src.camera import Camera
from src.chunked_map import ChunkedMap
from src.assets import Assets
from src.partical_system import ParticleSystem

class Game:
    def __init__(self, level_name):

        # game configurations
        # acpect ration = 5/4
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')
        self.DISPLAY_WIDTH = int(cfg['DEFAULT']['DISPLAY_WIDTH'])
        self.DISPLAY_HEIGHT = int(cfg['DEFAULT']['DISPLAY_HEIGHT'])
        self.RENDER_SURFACE_WIDTH = int(cfg['DEFAULT']['RENDER_SURFACE_WIDTH'])
        self.RENDER_SURFACE_HEIGHT = int(cfg['DEFAULT']['RENDER_SURFACE_HEIGHT'])
        self.BLOCK_WIDTH = int(cfg['DEFAULT']['BLOCK_WIDTH'])
        self.BLOCK_HEIGHT = int(cfg['DEFAULT']['BLOCK_HEIGHT'])
        self.CHUNK_SIZE = int(cfg['DEFAULT']['CHUNK_SIZE'])

        self.RENDER_SURFACE_MIDPOINT = (self.RENDER_SURFACE_WIDTH//2, 50 + self.RENDER_SURFACE_HEIGHT//2)
        self.GRAVITY = float(cfg['DEFAULT']['GRAVITY'])

        # pygame related initalization
        pygame.init()
        pygame.display.set_caption('Blursed Ninja')

        # pygame objects
        self.display = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.render_surface = pygame.Surface((self.RENDER_SURFACE_WIDTH, self.RENDER_SURFACE_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font() , 10)


        # game state variables
        self.RENDER_FRAME = True

        # game objects
        self.player = Player(x = 10, y = 20, width = 20, height = 40, color = (255,255,255))
        self.camera = Camera(self.player, fx = self.RENDER_SURFACE_MIDPOINT[0], fy = self.RENDER_SURFACE_MIDPOINT[1], smooth = 20)
        self.chunked_map = ChunkedMap(level_name, (2,3), (2,2))
        self.particle_system = ParticleSystem()

        # assets
        self.assets = Assets()
        self.assets.load_assets()
        self.dirt_img = pygame.image.load('assets/images/dirt/0.png')
        self.grass_img = pygame.image.load('assets/images/grass/0.png')
        self.player_img = pygame.image.load('assets/images/player/0.png')

    def show_fps(self):
        text = self.font.render(str(int(self.clock.get_fps())), True, (255, 255, 255), (0, 0, 0))
        self.render_surface.blit(text , (10 , 10))


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
        self.camera.follow()
        self.chunked_map.update(self.player.rect.x, self.player.rect.y)
        self.player.move(self.chunked_map.get_blocks())
        self.particle_system.add(self.player.rect.x, self.player.rect.y + self.player.rect.height)
        self.particle_system.update()


    def draw_frame(self):
        '''
        function to draw elements of render screen.
        '''
        self.render_surface.fill((135, 206, 235))
        self.render_surface.blit(self.assets.get_player_image(self.player.direction), self.camera.translate(self.player.rect))

        for tile in self.chunked_map.get_blocks():
            if tile.block_type > 0:
                self.render_surface.blit(self.assets.get_static_block_image(tile.block_type), self.camera.translate(tile.rect))

        # draw particles
        for particle in self.particle_system.particles:
            pygame.draw.circle(self.render_surface, particle.color, self.camera.translate_xy(particle.center), particle.radius)
        self.show_fps()


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
            self.clock.tick()

    def __del__(self):
        pygame.quit()
        pygame.font.quit()
