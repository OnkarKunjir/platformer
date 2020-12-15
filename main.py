import sys

from src.game import Game
from src.level_designer.level_designer import LevelDesigner

# TODO:
# Scale the render surface more.
# build a level designer
# make bot more smort.


if __name__ == "__main__":
    level_name = "dev_lvl"
    if len(sys.argv) > 1:
        if sys.argv[1] == "design":
            # launch level designer instead of the game.
            LevelDesigner()
        else:
            level_name = sys.argv[1]
            game = Game(level_name)
            game.play()
