import configparser
import pickle

import pygame
from src.assets import Assets
from src.entity.animated_block import AnimatedBlock
from src.entity.block import Block
from src.entity.reward import Reward


class LevelDesigner:
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read("config.ini")

        self.DISPLAY_WIDTH = int(cfg["DEFAULT"]["DISPLAY_WIDTH"])
        self.DISPLAY_HEIGHT = int(cfg["DEFAULT"]["DISPLAY_HEIGHT"])

        self.RENDER_SURFACE_WIDTH = int(cfg["DEFAULT"]["RENDER_SURFACE_WIDTH"])
        self.RENDER_SURFACE_HEIGHT = int(cfg["DEFAULT"]["RENDER_SURFACE_HEIGHT"])

        self.CHUNK_SIZE = int(cfg["DEFAULT"]["CHUNK_SIZE"])

        self.BLOCK_WIDTH = int(cfg["DEFAULT"]["BLOCK_WIDTH"])
        self.BLOCK_HEIGHT = int(cfg["DEFAULT"]["BLOCK_HEIGHT"])

        pygame.init()
        pygame.display.set_caption("Blursed Ninja design stuff")

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
        self.place_block = False
        self.remove_block = False
        self.poor_mans_snapping = False
        self.blocks = []

        self.block_type_button = (
            Block(
                x=6 * self.BLOCK_WIDTH,
                y=self.RENDER_SURFACE_HEIGHT - 3 * self.BLOCK_HEIGHT,
                width=26,
                height=26,
                block_type=1,
            ),
            Block(
                x=7 * self.BLOCK_WIDTH,
                y=self.RENDER_SURFACE_HEIGHT - 3 * self.BLOCK_HEIGHT,
                width=26,
                height=26,
                block_type=2,
            ),
            Block(
                x=9 * self.BLOCK_WIDTH,
                y=self.RENDER_SURFACE_HEIGHT - 3 * self.BLOCK_HEIGHT,
                width=16,
                height=16,
                block_type=3,
            ),
            Block(
                x=8 * self.BLOCK_WIDTH,
                y=self.RENDER_SURFACE_HEIGHT - 3 * self.BLOCK_HEIGHT,
                width=8,
                height=8,
                block_type=4,
            ),
            Block(
                x=10 * self.BLOCK_WIDTH,
                y=self.RENDER_SURFACE_HEIGHT - 3 * self.BLOCK_HEIGHT,
                width=self.BLOCK_WIDTH,
                height=self.BLOCK_HEIGHT,
                block_type=5,
            ),
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
        """
        W, A, S, D : Move camera
        R          : Reset camera
        E          : Export map
        <SPACE>    : toggle snapping
        """
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
                elif event.key == pygame.K_e:
                    self.export()
                elif event.key == pygame.K_SPACE:
                    self.poor_mans_snapping = not self.poor_mans_snapping

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
                    self.remove_block = False
                elif event.button == 3:
                    self.place_block = False
                    self.remove_block = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.place_block = False
                elif event.button == 3:
                    self.remove_block = False

    def translate(self, block):
        """
        function applies camera on the blocks
        NOTE: can be imporved.
        """
        x = block.rect.x - self.camera_x
        y = block.rect.y - self.camera_y
        return Block(
            x=x,
            y=y,
            width=block.rect.width,
            height=block.rect.height,
            block_type=block.block_type,
        )

    def draw_blocks(self):
        translated_blocks = map(self.translate, self.blocks)
        translated_blocks = filter(
            lambda x: (
                0 <= x.rect.x <= self.RENDER_SURFACE_WIDTH
                and 0 <= x.rect.y <= self.RENDER_SURFACE_HEIGHT
            ),
            translated_blocks,
        )

        for i in translated_blocks:
            self.render_surface.blit(self.assets.get_block_image(i.block_type), i.rect)

    def draw_grid(self):
        # NOTE: useless in non-legacy mode.
        # function draws grid on the screen accroding to the block width and block height.
        #
        # self.block_type_button[self.selected_type].rect.width
        for i in range(
            0,
            self.RENDER_SURFACE_WIDTH,
            self.block_type_button[self.selected_type].rect.width,
        ):
            pygame.draw.line(
                self.render_surface, (0, 0, 0), (i, 0), (i, self.RENDER_SURFACE_HEIGHT)
            )
        for i in range(
            0,
            self.RENDER_SURFACE_HEIGHT,
            self.block_type_button[self.selected_type].rect.width,
        ):
            pygame.draw.line(
                self.render_surface, (0, 0, 0), (0, i), (self.RENDER_SURFACE_WIDTH, i)
            )

    def draw_block_type_button(self):
        # highlight selected block with white border.
        selection_rect = self.block_type_button[self.selected_type].rect.copy()
        selection_rect.y -= 3
        selection_rect.height += 6
        pygame.draw.rect(self.render_surface, (255, 255, 255), selection_rect)
        for button in self.block_type_button:
            self.render_surface.blit(
                self.assets.get_block_image(button.block_type), button.rect
            )

    def draw_frame(self):
        self.render_surface.fill((135, 206, 235))
        self.draw_blocks()
        self.draw_grid()
        self.draw_block_type_button()

    def update(self):
        if self.move_bottom:
            self.camera_y += 26
        if self.move_up:
            self.camera_y -= 26
        if self.move_right:
            self.camera_x += 26
        if self.move_left:
            self.camera_x -= 26

        # keeping the positivity... lol
        self.camera_x = max(0, self.camera_x)
        self.camera_y = max(0, self.camera_y)

        if self.place_block or self.remove_block:
            pos = pygame.mouse.get_pos()
            # scaling the x, y coordinate back to the render surface coordinate I'm smort I know.
            x = int((pos[0] / self.DISPLAY_WIDTH) * (self.RENDER_SURFACE_WIDTH))
            y = int((pos[1] / self.DISPLAY_HEIGHT) * (self.RENDER_SURFACE_HEIGHT))

            clicked_button = tuple(
                filter(
                    lambda block: block.rect.collidepoint(x, y), self.block_type_button
                )
            )
            if len(clicked_button) > 0:
                if self.place_block:
                    # if user was pressing left click then and then only change the block type.
                    self.selected_type = clicked_button[0].block_type - 1
                    # TODO: fix this this very bad :(
                    self.camera_x = 0
                    self.camera_y = 0

                self.place_block = False
                self.remove_block = False
                return

            x = (
                self.block_type_button[self.selected_type].rect.width
                * (x // self.block_type_button[self.selected_type].rect.width)
            ) + self.camera_x
            y = (
                self.block_type_button[self.selected_type].rect.height
                * (y // self.block_type_button[self.selected_type].rect.height)
            ) + self.camera_y
            temp_block = Block(
                x=x,
                y=y,
                width=self.block_type_button[self.selected_type].rect.width,
                height=self.block_type_button[self.selected_type].rect.height,
                block_type=self.block_type_button[self.selected_type].block_type,
            )

            prev = list(
                filter(
                    lambda block: temp_block.rect.colliderect(block.rect), self.blocks
                )
            )
            if self.place_block:
                if len(prev) == 0:
                    self.blocks.append(temp_block)
                elif self.poor_mans_snapping:
                    # hack to align items when out of sync
                    temp_block.rect.bottom = prev[0].rect.top
                    prev = list(
                        filter(
                            lambda block: temp_block.rect.colliderect(block.rect),
                            self.blocks,
                        )
                    )
                    if len(prev) == 0:
                        self.blocks.append(temp_block)

            elif self.remove_block and len(prev) > 0:
                del self.blocks[self.blocks.index(prev[0])]

    def get_entity(self, x, y, image_size, block_type):
        """
        function return entity object of appropriate type according to block_type.
        """
        if block_type == 3:
            return Reward(
                x=x,
                y=y,
                width=image_size[0],
                height=image_size[1],
                block_type=block_type,
                health_gain=-20,
                score_gain=0,
            )
        elif block_type == 4:
            return Reward(
                x=x,
                y=y,
                width=image_size[0],
                height=image_size[1],
                block_type=block_type,
                health_gain=0,
                score_gain=10,
                n_frames=5,
            )
        elif block_type == 5:
            return AnimatedBlock(
                x=x,
                y=y,
                width=image_size[0],
                height=image_size[1],
                block_type=block_type,
                n_frames=2,
            )
        else:
            return Block(
                x=x,
                y=y,
                width=image_size[0],
                height=image_size[1],
                block_type=block_type,
            )

    def export(self, leagacy_mode=False):
        """
        TODO: Handle cases where user is trying to save map without player or saving empty map or something.
        function to export whole map in desired format.
        """

        if leagacy_mode:
            n_cols = (
                max(self.blocks, key=lambda block: block.rect.x).rect.x
                // self.BLOCK_WIDTH
            ) + 1
            n_rows = (
                max(self.blocks, key=lambda block: block.rect.y).rect.y
                // self.BLOCK_HEIGHT
            ) + 1

            map_list = [["0"] * n_cols for _ in range(n_rows)]

            for block in self.blocks:
                col = block.rect.x // self.BLOCK_WIDTH
                row = block.rect.y // self.BLOCK_HEIGHT

                map_list[row][col] = str(block.block_type)

            map_str = ""
            for row in map_list:
                map_str += ",".join(row) + "\n"

            # wtirte the map to file.
            with open("assets/levels/new_map.txt", "w") as export_file:
                export_file.write(map_str)
            self.RENDER_FRAME = False

        else:
            # export object directly which is more flexible.
            chunked_map = {}
            for block in self.blocks:
                rect = block.rect
                cx = rect.x // self.CHUNK_SIZE
                cy = rect.y // self.CHUNK_SIZE

                # convert each block into appropriate entity.
                converted_block = self.get_entity(
                    rect.x, rect.y, (rect.width, rect.height), block.block_type
                )

                if (cx, cy) in chunked_map.keys():
                    chunked_map[(cx, cy)].append(converted_block)
                else:
                    chunked_map[(cx, cy)] = [converted_block]

            # convert list into tuple cause it's not gonna change.
            for key in chunked_map.keys():
                chunked_map[key] = tuple(chunked_map[key])

            with open("assets/levels/new_map.map", "wb") as new_map:
                pickle.dump(chunked_map, new_map)

    def run(self):
        while self.RENDER_FRAME:

            self.event_handler()
            self.update()
            self.draw_frame()

            scaled_surface = pygame.transform.scale(
                self.render_surface, (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)
            )
            self.display.blit(scaled_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
