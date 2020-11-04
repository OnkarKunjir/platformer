import configparser
import os
from src.entity.block import Block

class ChunkedMap:
    '''
    class to handle chunked map.
    '''
    def __init__(self, level_name, xlimit, ylimit):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')

        DISPLAY_WIDTH = int(cfg['DEFAULT']['DISPLAY_WIDTH'])
        DISPLAY_HEIGHT = int(cfg['DEFAULT']['DISPLAY_HEIGHT'])
        RENDER_SURFACE_WIDTH = int(cfg['DEFAULT']['RENDER_SURFACE_WIDTH'])
        RENDER_SURFACE_HEIGHT = int(cfg['DEFAULT']['RENDER_SURFACE_HEIGHT'])
        BLOCK_WIDTH = int(cfg['DEFAULT']['BLOCK_WIDTH'])
        BLOCK_HEIGHT = int(cfg['DEFAULT']['BLOCK_HEIGHT'])
        CHUNK_SIZE = int(cfg['DEFAULT']['CHUNK_SIZE'])

        self.level_name = level_name
        self.chunks = {}
        self.chunk_pixel_width = CHUNK_SIZE * BLOCK_WIDTH
        self.chunk_pixel_height = CHUNK_SIZE * BLOCK_HEIGHT
        self.chunk_x = 0
        self.chunk_y = 0
        self.blocks_on_screen = []

        self.xb, self.xf = xlimit
        self.yb, self.yf = ylimit


        self.load_chunk_map((BLOCK_WIDTH, BLOCK_HEIGHT), (RENDER_SURFACE_WIDTH, RENDER_SURFACE_HEIGHT), CHUNK_SIZE)

    def load_chunk_map(self, image_size, display_size, chunk_size):
        level_path = 'assets/levels/' + self.level_name + '.txt'
        self.chunks = {}

        if os.path.exists(level_path):
            with open(level_path, 'r') as lvl:
                lvl = lvl.read().split('\n')
                x = 0
                y = 0
                for row in lvl:
                    x = 0
                    if len(row.strip()) > 0:
                        for cell in row.strip().split(','):
                            cell = int(cell)
                            if cell > 0:
                                cx = x//self.chunk_pixel_width
                                cy = y//self.chunk_pixel_height
                                if (cx, cy) not in self.chunks.keys():
                                    self.chunks[(cx, cy)] = []
                                self.chunks[(cx, cy)].append(
                                    Block(x = x, y = y, width = image_size[0], height = image_size[1], block_type = cell),
                                )
                            x += image_size[0]
                        y += image_size[1]

    def update(self, px, py):
        '''
        update chunk index based on players position.
        px,py = x and y coordinate of player.
        '''
        self.chunk_x = px//self.chunk_pixel_width
        self.chunk_y = py//self.chunk_pixel_height
        self.blocks_on_screen = []


    def get_blocks(self):
        '''
        returns list of blocks visible on the screen.
        '''
        if len(self.blocks_on_screen) > 0:
            return self.blocks_on_screen
        cx = self.chunk_x
        cy = self.chunk_y
        #for i in range(cx-2, cx+3):
        #    for j in range(cy-2, cy+2):
        for i in range(cx-self.xb, cx+self.xf):
            for j in range(cy-self.yb, cy+self.yf):
                for c in self.chunks.get((i,j), []):
                    self.blocks_on_screen.append(c)

        return self.blocks_on_screen