from src.game import Game
import sys

# TODO: make enemies attack the player.


if __name__ == '__main__':
    level_name = 'dev_lvl'
    if len(sys.argv) > 1:
        level_name = sys.argv[1]
    game = Game(level_name)
    game.play()
