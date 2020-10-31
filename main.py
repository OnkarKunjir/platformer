from src.game import Game
import sys

# TODO:
# optimize collision detection by checking collision limiter blocks.
# create mapping for asset image and block type
# optimize the rendering method.

if __name__ == '__main__':
    level_name = 'dev_lvl'
    if len(sys.argv) > 1:
        level_name = sys.argv[1]
    game = Game(level_name)
    game.play()
