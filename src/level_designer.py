import pygame
import os
import configparser


class LevelDesigner:
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')

        self.DISPLAY_WIDTH = int(cfg['DEFAULT']['DISPLAY_WIDTH'])
        self.DISPLAY_HEIGHT = int(cfg['DEFAULT']['DISPLAY_HEIGHT'])

        self.RENDER_SURFACE_WIDTH = int(cfg['DEFAULT']['RENDER_SURFACE_WIDTH'])
        self.RENDER_SURFACE_HEIGHT = int(cfg['DEFAULT']['RENDER_SURFACE_HEIGHT'])

        self.CHUNK_SIZE = int(cfg['DEFAULT']['CHUNK_SIZE'])

        self.BLOCK_WIDTH = int(cfg['DEFAULT']['BLOCK_WIDTH'])
        self.BLOCK_HEIGHT = int(cfg['DEFAULT']['BLOCK_HEIGHT'])

        pygame.init()
        pygame.display.set_caption('Blursed Ninja design stuff')

        # pygame objects
        self.display = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.render_surface = pygame.Surface((self.RENDER_SURFACE_WIDTH, self.RENDER_SURFACE_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font() , 10)

        # game state variables
        self.RENDER_FRAME = True


        self.run()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RENDER_FRAME = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.RENDER_FRAME = False
                    break

    def run(self):
        while self.RENDER_FRAME:
            self.render_surface.fill((135, 206, 235))

            self.event_handler()
            scaled_surface = pygame.transform.scale(self.render_surface, (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
            self.display.blit(scaled_surface, (0, 0))
            pygame.display.update()
            self.clock.tick()
