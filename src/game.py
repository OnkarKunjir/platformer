import pygame
import random
from src.entity import Entity
from src.utils import check_collision, update_pos_from_collision, load_level

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
        self.MOVE_KEY_PRESSED = False
        self.DIRECTION = False # True = Right False = Left
        self.JUMP = False

        # game objects
        self.player = Entity(x = 10, y = 20, width = 15, height = 30, color = (255,255,255))
        self.tiles = []
        self.move = [0, 0]
        self.camera = [0, 0]

        self.tiles = load_level('dev_lvl', (20,20), (self.RENDER_SURFACE_WIDTH, self.RENDER_SURFACE_HEIGHT) )


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
                    self.MOVE_KEY_PRESSED = True
                    self.DIRECTION = False

                elif event.key == pygame.K_d:
                    self.MOVE_KEY_PRESSED = True
                    self.DIRECTION = True

                elif event.key == pygame.K_SPACE:
                    self.JUMP = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.MOVE_KEY_PRESSED = False


    def update_entities(self):
        '''
        function to update position of all entities based.
        '''
        self.camera[0] = (self.player.rect.x - self.RENDER_SURFACE_MIDPOINT[0])//20
        self.camera[1] = (self.player.rect.y - self.RENDER_SURFACE_MIDPOINT[1])//20

        if self.JUMP:
            self.move[1] = -5
            self.JUMP = False

        self.move[1] += self.GRAVITY

        if self.MOVE_KEY_PRESSED:
            self.move[0] += 3 if self.DIRECTION else -3
        else:
            self.move[0] = 0

        for i in range(2):
            if self.move[i] > 5:
                self.move[i] = 5
            elif self.move[i] < -5:
                self.move[i] = -5

        update_pos_from_collision(self.player, self.tiles, self.move)
        for i in self.tiles:
            i.rect.x -= self.camera[0]
            i.rect.y -= self.camera[1]

        self.player.rect.x -= self.camera[0]
        self.player.rect.y -= self.camera[1]


    def draw_frame(self):
        '''
        draw all components visible in frame.
        '''
        self.render_surface.fill((0,0,0))
        pygame.draw.rect(self.render_surface, self.player.color, self.player.rect)

        for tile in self.tiles:
            pygame.draw.rect(self.render_surface, tile.color, tile.rect)

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
