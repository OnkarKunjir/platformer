import configparser
import random
import threading

import pygame

from src.assets import Assets
from src.background import Background
from src.camera import Camera
from src.chunked_map import ChunkedMap
from src.entity.animated_entity import AnimatedEntity
from src.entity.reward import Reward
from src.partical_system import ParticleSystem


class Game:
    def __init__(self, level_name):

        # game configurations
        # acpect ration = 5/4
        cfg = configparser.ConfigParser()
        cfg.read("config.ini")
        self.DISPLAY_WIDTH = int(cfg["DEFAULT"]["DISPLAY_WIDTH"])
        self.DISPLAY_HEIGHT = int(cfg["DEFAULT"]["DISPLAY_HEIGHT"])
        self.RENDER_SURFACE_WIDTH = int(cfg["DEFAULT"]["RENDER_SURFACE_WIDTH"])
        self.RENDER_SURFACE_HEIGHT = int(cfg["DEFAULT"]["RENDER_SURFACE_HEIGHT"])
        self.BLOCK_WIDTH = int(cfg["DEFAULT"]["BLOCK_WIDTH"])
        self.BLOCK_HEIGHT = int(cfg["DEFAULT"]["BLOCK_HEIGHT"])
        self.CHUNK_SIZE = int(cfg["DEFAULT"]["CHUNK_SIZE"])

        self.RENDER_SURFACE_MIDPOINT = (
            self.RENDER_SURFACE_WIDTH // 2,
            50 + self.RENDER_SURFACE_HEIGHT // 2,
        )
        self.GRAVITY = float(cfg["DEFAULT"]["GRAVITY"])

        # pygame related initalization
        pygame.init()
        pygame.display.set_caption("Blursed Ninja")

        # pygame objects
        self.display = pygame.display.set_mode(
            (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)
        )
        self.render_surface = pygame.Surface(
            (self.RENDER_SURFACE_WIDTH, self.RENDER_SURFACE_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 10)

        # game state variables
        self.RENDER_FRAME = True
        self.frames = 0
        self.score = 0

        # game objects
        # self.player = Player(x = 10, y = 20, width = 20, height = 40)

        self.chunked_map = ChunkedMap(level_name, (2, 3), (2, 2))
        self.player = self.chunked_map.player

        self.camera = Camera(
            self.player,
            fx=self.RENDER_SURFACE_MIDPOINT[0],
            fy=self.RENDER_SURFACE_MIDPOINT[1],
            smooth=20,
        )
        self.particle_system = ParticleSystem()
        self.background = Background()

        self.enemies = None

        # assets
        self.assets = Assets()
        self.assets.load_assets()

        self.moon = pygame.Surface((80, 80))
        self.moon.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.moon, (50, 50, 50), (40, 40), 40)

    def event_handler(self):
        """
        function to handle events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RENDER_FRAME = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # exit game on ESCAPE
                    self.RENDER_FRAME = False

                elif event.key == pygame.K_a:
                    self.player.move_direction["left"] = True

                elif event.key == pygame.K_d:
                    self.player.move_direction["right"] = True

                elif event.key == pygame.K_SPACE:
                    self.player.move_direction["up"] = True

                elif event.key == pygame.K_h:
                    self.player.move_direction["attack"] = True

                elif event.key == pygame.K_k:
                    # NOTE: testing purpose only
                    self.player.health = 0

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.move_direction["left"] = False
                elif event.key == pygame.K_d:
                    self.player.move_direction["right"] = False

    def update_entities(self):
        """
        function to update position of all entities based.
        """
        self.camera.follow()
        self.chunked_map.update(self.player.rect.x, self.player.rect.y)
        self.enemies = tuple(self.chunked_map.get_special_entities_on_screen())

        # update animation of tiles.
        tiles = self.chunked_map.get_blocks()
        for tile in tiles:
            if isinstance(tile, AnimatedEntity):
                tile.update_frame()

        if self.player.move_direction["attack"]:
            x = (
                self.player.rect.x + self.player.rect.width
                if self.player.direction
                else self.player.rect.x
            )
            y = (self.player.rect.y + self.player.rect.height // 2) - 5

        self.score += self.player.move(tiles, self.enemies)
        # update enemies postion.
        for enemy in self.enemies:
            enemy.move(
                tiles, self.enemies, self.player, self.camera.translate(enemy.rect)
            )

        # adding particles when player moves on the ground.
        if self.player.landed:
            x = self.player.rect.x + self.player.rect.width // 2
            y = self.player.rect.y + self.player.rect.height
            self.particle_system.add(x, y, n=3, velocity_x=2, velocity_y=-2)
            self.particle_system.add(x, y, n=3, velocity_x=-2, velocity_y=-2)

        self.particle_system.update()

    # helper function to draw frame.
    def draw_fps(self):
        text = self.font.render(
            str(int(self.clock.get_fps())), True, (255, 255, 255), (0, 0, 0)
        )
        self.render_surface.blit(text, (470, 10))

    def draw_score(self):
        text = self.font.render(str(self.score), True, (255, 255, 255), (0, 0, 0))
        self.render_surface.blit(text, (50, 10))

    def draw_health_bar(
        self, health, x, y, max_health=100, thickness=5, translate=False
    ):
        if translate:
            pygame.draw.rect(
                self.render_surface,
                (0, 0, 0),
                self.camera.translate(
                    pygame.Rect(x - 1, y - 1, max_health + 2, thickness + 2)
                ),
            )
        else:
            pygame.draw.rect(
                self.render_surface,
                (0, 0, 0),
                (x - 1, y - 1, max_health + 2, thickness + 2),
            )

        color = None
        rect = pygame.Rect(x, y, health, thickness)
        if health > max_health * 0.6:
            color = (0, 255, 0)
        elif health > max_health * 0.4:
            color = (200, 255, 0)
        else:
            color = (200, 100, 0)

        if translate:
            pygame.draw.rect(self.render_surface, color, self.camera.translate(rect))
        else:
            pygame.draw.rect(self.render_surface, color, rect)

    def draw_player_health(self):
        self.draw_health_bar(self.player.health, 20, 12)

    def draw_enemy_health(self, enemy):
        x = enemy.rect.x
        y = enemy.rect.y
        y -= 15
        x -= 12
        self.draw_health_bar(
            enemy.health // 2, x, y, max_health=50, thickness=2, translate=True
        )

    def draw_attack_arc(self, character):
        # NOTE: figure out better way to do this.
        x = character.rect.x
        y = character.rect.y + 15
        width = character.rect.width
        height = character.rect.height

        arc_surface = pygame.Surface((40, 10))
        r = pygame.Rect(x, y, 40, 10)

        pygame.draw.arc(
            arc_surface,
            (255, 255, 255),
            (0, 0, 40, 10),
            0.0174533 * 300,
            0.0174533 * character.attack_arc_end_deg,
            5,
        )
        character.attack_arc_end_deg += 15
        if character.attack_arc_end_deg > 460:
            character.attack_arc_end_deg = 300
        arc_surface.set_colorkey((0, 0, 0))
        if not character.direction:
            arc_surface = pygame.transform.flip(arc_surface, True, False)
            r.x -= character.rect.width

        self.render_surface.blit(arc_surface, self.camera.translate(r))

    def draw_background(self):
        for i in self.background.level_2:
            pygame.draw.rect(
                self.render_surface,
                (0, 220, 0),
                self.camera.translate_distance(
                    i.rect, self.background.levle_2_distance
                ),
            )
        for i in self.background.level_1:
            pygame.draw.rect(
                self.render_surface,
                (0, 160, 0),
                self.camera.translate_distance(
                    i.rect, self.background.levle_1_distance
                ),
            )

    def get_tile_blit_seq(self, tile):
        if isinstance(tile, AnimatedEntity):
            return (
                self.assets.get_block_image(tile.block_type, tile.current_frame),
                self.camera.translate(tile.rect),
            )

        elif tile.block_type > 0:
            return (
                self.assets.get_block_image(tile.block_type),
                self.camera.translate(tile.rect),
            )

    def draw_frame(self):
        """
        function to draw elements of render screen.
        """
        self.render_surface.fill((135, 206, 235))
        # self.render_surface.fill((33, 38, 63))
        self.render_surface.blit(
            self.moon,
            (self.RENDER_SURFACE_WIDTH - 150, 80),
            special_flags=pygame.BLEND_ADD,
        )

        # draw background
        self.draw_background()

        self.render_surface.blit(
            self.assets.get_character_image(self.player),
            self.camera.translate(self.player.rect),
        )

        for enemy in self.enemies:
            pygame.draw.rect(
                self.render_surface, enemy.color, self.camera.translate(enemy.rect)
            )
            self.draw_enemy_health(enemy)

        # code to mask perticular block type.
        # for i in self.chunked_map.get_blocks():
        #     if i.block_type == 4:
        #         pygame.draw.rect(
        #             self.render_surface, (255, 255, 255), self.camera.translate(i.rect)
        #         )

        # draw tiles
        tiles = filter(
            lambda tile: not isinstance(tile, Reward) or tile.is_valid,
            self.chunked_map.get_blocks(),
        )
        tiles = map(self.get_tile_blit_seq, tiles)
        self.render_surface.blits(tiles)

        # draw particles
        for particle in self.particle_system.get_active_particles():
            pygame.draw.circle(
                self.render_surface,
                particle.color,
                self.camera.translate_xy(particle.center),
                particle.radius,
            )

        # self.draw_fps()
        # self.draw_score()
        self.draw_player_health()
        if self.player.attack_arc_end_deg != 300:
            self.draw_attack_arc(self.player)

        for enemy in filter(lambda e: e.attack_arc_end_deg != 300, self.enemies):
            self.draw_attack_arc(enemy)

        if not self.player.read_to_take_damage:
            red_s = pygame.Surface(
                (self.RENDER_SURFACE_WIDTH, self.RENDER_SURFACE_HEIGHT)
            )
            red_s.fill((100, 0, 0))
            self.render_surface.blit(red_s, (0, 0), special_flags=pygame.BLEND_ADD)

    def play(self):
        """
        run main game loop
        """
        frame_time = 0
        last_angle = 5
        while self.RENDER_FRAME:
            frame_time += self.clock.get_time()
            if frame_time > 15:
                frame_time = 0
                self.event_handler()
                self.update_entities()
                self.draw_frame()

                scaled_surface = pygame.transform.scale(
                    self.render_surface, (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)
                )
                self.display.blit(scaled_surface, (0, 0))

            pygame.display.update()
            self.clock.tick()

    def __del__(self):
        pygame.quit()
        pygame.font.quit()
