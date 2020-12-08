import os

from pygame import image, transform


class Assets:
    def __init__(self):
        self.static_block_assets_class = [
            "dirt",
            "grass",
            "coin",
            "spike",
        ]
        self.animated_block_assets_class = [
            "stick",
        ]

        self.static_blocks = {}
        self.animated_blocks = {}

        self.image_asset_base_dir = "assets/images/"

    def load_assets(self):
        # load the static blocks images
        for i, asset_name in enumerate(self.static_block_assets_class):
            current_asset_dir = os.path.join(self.image_asset_base_dir, asset_name)
            if os.path.exists(current_asset_dir):
                image_name = os.path.join(
                    current_asset_dir, os.listdir(current_asset_dir)[0]
                )
                self.static_blocks[i + 1] = image.load(image_name)

        # laod animated block assets
        animation_id_start = len(self.static_block_assets_class)

        for i, asset_name in enumerate(self.animated_block_assets_class):
            current_asset_dir = os.path.join(self.image_asset_base_dir, asset_name)
            if os.path.exists(current_asset_dir):
                current_id = i + animation_id_start + 1
                self.animated_blocks[current_id] = []
                for frame_name in os.listdir(current_asset_dir):
                    frame_path = os.path.join(current_asset_dir, frame_name)
                    self.animated_blocks[current_id].append(image.load(frame_path))

        self.load_player_assets()

    def load_player_assets(self, default_player_direction=True):
        # player direction True/False = Right/Left
        self.player = self.load_character_assets(
            os.path.join(self.image_asset_base_dir, "player")
        )

    def load_character_assets(self, base_path):
        """
        function loads asset for character.
        returns asset dict.
        """
        asset_dict = {"left": {}, "right": {}}

        if os.path.exists(base_path):
            character_states = os.listdir(base_path)
            for state in character_states:
                state_path = os.path.join(base_path, state)

                asset_dict["left"][state] = []
                asset_dict["right"][state] = []

                # loading frames for each state
                for frame_name in sorted(os.listdir(state_path)):
                    frame_path = os.path.join(state_path, frame_name)

                    frame = image.load(frame_path)
                    asset_dict["right"][state].append(frame)
                    asset_dict["left"][state].append(transform.flip(frame, True, False))

                # converting list into tuple.
                asset_dict["left"][state] = tuple(asset_dict["left"][state])
                asset_dict["right"][state] = tuple(asset_dict["right"][state])
        return asset_dict

    def get_static_block_image(self, block_type):
        return self.static_blocks[block_type]

    def get_animated_block_image(self, block_type, frame):
        return self.animated_blocks[block_type][frame]

    def get_block_image(self, block_type, frame=0):
        if block_type <= len(self.static_block_assets_class):
            return self.get_static_block_image(block_type)
        return self.get_animated_block_image(block_type, frame)

    def get_character_image(self, character):
        direction = "right" if character.direction else "left"
        return self.player[direction][character.current_state][character.current_frame]
