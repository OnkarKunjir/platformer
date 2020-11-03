import os
from pygame import image

class Assets:
    def __init__(self):
        self.available_assets = [
            '',
            'dirt',
            'grass',
            'player',
        ]

        self.asset_dir = 'assets/images/'
        self.asset_images = {
            'dirt'   : [],
            'grass'  : [],
            'player' : [],
        }

    def load(self):
        for asset_name in self.available_assets[1:]:
            current_path = self.asset_dir + asset_name
            if os.path.exists(current_path):
                for frame in os.listdir(current_path):
                    self.asset_images[asset_name].append(
                        image.load(os.path.join(current_path, frame))
                    )

    def get_mapped_image(self, index, frame = 0):
        return self.asset_images[self.available_assets[index]][frame]

    def get_image(self, image_name, frame = 0):
        return self.asset_images[image_name][frame]
