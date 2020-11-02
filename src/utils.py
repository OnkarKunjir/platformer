import os
from pygame import Rect
import random
from src.entity.block import  Block

def load_level(level_name, image_size, display_size):
    '''
    function loads map from txt file from assets/levels and converts each cell into appropriate Entity element.
    returns list of Entity.
    '''
    level_path = 'assets/levels/' + level_name + '.txt'
    tiles = []
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
                            tiles.append(
                                Block(x = x, y = y, width = image_size[0], height = image_size[1], block_type = cell),
                            )
                        x += image_size[0]
                    y += image_size[1]
    return tiles


def load_chunk_map(level_name, image_size, display_size, chunk_size):
    level_path = 'assets/levels/' + level_name + '.txt'
    chunks = {}
    chunk_pixel_width = chunk_size * image_size[0]
    chunk_pixel_height = chunk_size * image_size[1]
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
                            cx = x//chunk_pixel_width
                            cy = y//chunk_pixel_height
                            if (cx, cy) not in chunks.keys():
                                chunks[(cx, cy)] = []
                            chunks[(cx, cy)].append(
                                Block(x = x, y = y, width = image_size[0], height = image_size[1], block_type = cell),
                            )
                        x += image_size[0]
                    y += image_size[1]
    return chunks
