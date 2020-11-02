import pygame
import random
import configparser
from src.entity.player import Player
from src.utils import load_chunk_map
from src.camera import Camera

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
        self.move = [0, 0]
        self.camera = Camera(self.player, fx = self.RENDER_SURFACE_MIDPOINT[0], fy = self.RENDER_SURFACE_MIDPOINT[1], smooth = 20)

        self.chunks = load_chunk_map(level_name, (self.BLOCK_WIDTH, self.BLOCK_HEIGHT), (self.RENDER_SURFACE_WIDTH, self.RENDER_SURFACE_HEIGHT), self.CHUNK_SIZE)

        # assets
        self.dirt_img = pygame.image.load('assets/images/dirt.png')
        self.grass_img = pygame.image.load('assets/images/grass.png')

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
        #self.player.move(self.blocks)
        cx = self.player.rect.x//200
        cy = self.player.rect.y//200
        blocks = []
        for i in range(cx-1, cx+2):
            for j in range(cy-1, cy+2):
                for c in self.chunks.get((i,j), []):
                    blocks.append(c)
        self.player.move(blocks)


    def draw_frame(self):
        self.render_surface.fill((135, 206, 235))
        pygame.draw.rect(self.render_surface, self.player.color, self.camera.translate(self.player.rect))
        cx = self.player.rect.x//200
        cy = self.player.rect.y//200
        for i in range(cx-2, cx+3):
            for j in range(cy-2, cy+2):
                for tile in self.chunks.get((i,j), []):
                    if tile.block_type == 1:
                        self.render_surface.blit(self.dirt_img, self.camera.translate(tile.rect))
                    elif tile.block_type == 2:
                        self.render_surface.blit(self.grass_img, self.camera.translate(tile.rect))
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
            self.clock.tick(60)

    def __del__(self):
        pygame.quit()
        pygame.font.quit()
