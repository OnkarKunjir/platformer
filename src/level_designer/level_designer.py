import pygame
import os
import configparser

from src.assets import Assets
from src.entity.block import Block

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

        self.block_type_button = (
            Block(x = 6*self.BLOCK_WIDTH, y = self.RENDER_SURFACE_HEIGHT - 3*self.BLOCK_HEIGHT, width = self.BLOCK_WIDTH, height = self.BLOCK_HEIGHT, block_type = 1),
            Block(x = 7*self.BLOCK_WIDTH, y = self.RENDER_SURFACE_HEIGHT - 3*self.BLOCK_HEIGHT, width = self.BLOCK_WIDTH, height = self.BLOCK_HEIGHT, block_type = 2),
            Block(x = 8*self.BLOCK_WIDTH, y = self.RENDER_SURFACE_HEIGHT - 3*self.BLOCK_HEIGHT, width = self.BLOCK_WIDTH, height = self.BLOCK_HEIGHT, block_type = 3),
            Block(x = 9*self.BLOCK_WIDTH, y = self.RENDER_SURFACE_HEIGHT - 3*self.BLOCK_HEIGHT, width = self.BLOCK_WIDTH, height = self.BLOCK_HEIGHT, block_type = 4),
            Block(x = 10*self.BLOCK_WIDTH, y = self.RENDER_SURFACE_HEIGHT - 3*self.BLOCK_HEIGHT, width = self.BLOCK_WIDTH, height = self.BLOCK_HEIGHT, block_type = 5),
        )

        self.selected_type = 0

        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_bottom = False

        self.camera_x = 0
        self.camera_y = 0

        # assets
        self.assets = Assets()
        self.assets.load_assets()

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
                elif event.key == pygame.K_w:
                    self.move_up = True
                elif event.key == pygame.K_s:
                    self.move_bottom = True
                elif event.key == pygame.K_a:
                    self.move_left = True
                elif event.key == pygame.K_d:
                    self.move_right = True
                elif event.key == pygame.K_r:
                    self.camera_x = 0
                    self.camera_y = 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.move_up = False
                elif event.key == pygame.K_s:
                    self.move_bottom = False
                elif event.key == pygame.K_a:
                    self.move_left = False
                elif event.key == pygame.K_d:
                    self.move_right = False


            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.place_block = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.place_block = False

    def translate(self, block):
        '''
        function applies camera on the blocks
        NOTE: can be imporved.
        '''
        x = block.rect.x - self.camera_x
        y = block.rect.y - self.camera_y
        return Block(x = x, y = y, width = self.BLOCK_WIDTH, height = self.BLOCK_HEIGHT, block_type = block.block_type)

    def draw_blocks(self):
        translated_blocks = map(self.translate, self.blocks)
        translated_blocks = filter(lambda x : (0 <= x.rect.x <= self.RENDER_SURFACE_WIDTH and 0 <= x.rect.y <= self.RENDER_SURFACE_HEIGHT), translated_blocks)

        for i in translated_blocks:
            self.render_surface.blit(self.assets.get_block_image(i.block_type), i.rect)

    def draw_grid(self):
        for i in range(0, self.RENDER_SURFACE_WIDTH, self.BLOCK_WIDTH):
            pygame.draw.line(self.render_surface, (0, 0, 0), (i, 0), (i, self.RENDER_SURFACE_HEIGHT))
        for i in range(0, self.RENDER_SURFACE_HEIGHT, self.BLOCK_HEIGHT):
            pygame.draw.line(self.render_surface, (0, 0, 0), (0, i), (self.RENDER_SURFACE_WIDTH, i))

    def draw_block_type_button(self):
        # highlight selected block with white border.
        selection_rect = self.block_type_button[self.selected_type].rect.copy()
        selection_rect.y -= 3
        selection_rect.height += 6
        pygame.draw.rect(self.render_surface, (255, 255, 255), selection_rect)
        for button in self.block_type_button:
            self.render_surface.blit(self.assets.get_block_image(button.block_type), button.rect)

    def draw_frame(self):
        self.render_surface.fill((135, 206, 235))
        self.draw_blocks()
        self.draw_grid()
        self.draw_block_type_button()


    def update(self):
        if self.move_bottom:
            self.camera_y += self.BLOCK_HEIGHT
        if self.move_up:
            self.camera_y -= self.BLOCK_HEIGHT
        if self.move_right:
            self.camera_x += self.BLOCK_WIDTH
        if self.move_left:
            self.camera_x -= self.BLOCK_WIDTH

        # keeping the positivity... lol
        self.camera_x = max(0, self.camera_x)
        self.camera_y = max(0, self.camera_y)


        if self.place_block:
            pos = pygame.mouse.get_pos()
            # scaling the x, y coordinate back to the render surface coordinate I'm smort I know.
            x = int(( pos[0] / self.DISPLAY_WIDTH) * (self.RENDER_SURFACE_WIDTH))
            y = int(( pos[1] / self.DISPLAY_HEIGHT) * (self.RENDER_SURFACE_HEIGHT))

            clicked_button = tuple(filter(lambda block : block.rect.collidepoint(x, y), self.block_type_button))
            if len(clicked_button) > 0:
                self.place_block = False
                self.selected_type = clicked_button[0].block_type - 1
                return

            x = (self.BLOCK_WIDTH * (x // self.BLOCK_WIDTH)) + self.camera_x
            y = (self.BLOCK_HEIGHT * (y // self.BLOCK_HEIGHT)) + self.camera_y



            prev = list(filter(lambda block : (block.rect.x == x and block.rect.y == y) , self.blocks))
            if len(prev) == 0:
                self.blocks.append(
                    Block(x = x, y = y, width = self.BLOCK_WIDTH, height = self.BLOCK_HEIGHT, block_type = self.block_type_button[self.selected_type].block_type)
                )


    def run(self):
        while self.RENDER_FRAME:

            self.event_handler()
            self.update()
            self.draw_frame()

            scaled_surface = pygame.transform.scale(self.render_surface, (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
            self.display.blit(scaled_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
