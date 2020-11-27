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
        self.place_block = False
        self.blocks = []

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.place_block = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.place_block = False

    def draw_blocks(self):
        for i in self.blocks:
            pygame.draw.rect(self.render_surface, (255, 255, 255), (i, (self.BLOCK_WIDTH, self.BLOCK_HEIGHT)))

    def draw_grid(self):
        for i in range(0, self.RENDER_SURFACE_WIDTH, self.BLOCK_WIDTH):
            pygame.draw.line(self.render_surface, (0, 0, 0), (i, 0), (i, self.RENDER_SURFACE_HEIGHT))
        for i in range(0, self.RENDER_SURFACE_HEIGHT, self.BLOCK_HEIGHT):
            pygame.draw.line(self.render_surface, (0, 0, 0), (0, i), (self.RENDER_SURFACE_WIDTH, i))

    def draw_frame(self):
        self.render_surface.fill((135, 206, 235))
        self.draw_blocks()
        self.draw_grid()


    def update(self):
        if self.place_block:
            pos = pygame.mouse.get_pos()
            # scaling the x, y coordinate back to the render surface coordinate I'm smort I know.
            x = int(( pos[0] / self.DISPLAY_WIDTH) * (self.RENDER_SURFACE_WIDTH))
            y = int(( pos[1] / self.DISPLAY_HEIGHT) * (self.RENDER_SURFACE_HEIGHT))
            x = self.BLOCK_WIDTH * (x // self.BLOCK_WIDTH)
            y = self.BLOCK_HEIGHT * (y // self.BLOCK_HEIGHT)
            self.blocks.append((x, y))

    def run(self):
        while self.RENDER_FRAME:

            self.event_handler()
            self.update()
            self.draw_frame()

            scaled_surface = pygame.transform.scale(self.render_surface, (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
            self.display.blit(scaled_surface, (0, 0))
            pygame.display.update()
            self.clock.tick()
