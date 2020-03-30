from collections import OrderedDict

import numpy as np
from pygame.sprite import Group, RenderUpdates
from pygame.transform import scale

from src.animated_sprite import AnimatedSprite
from src.base_sprite import BaseSprite
from src.common import Direction, tantegel_castle_throne_room_music, play_music, KING_LORIK_PATH, get_image, \
    ROAMING_GUARD_PATH, MAN_PATH, village_music, tantegel_castle_courtyard_music, WOMAN_PATH, WISE_MAN_PATH, \
    SOLDIER_PATH, MERCHANT_PATH, PRINCESS_GWAELIN_PATH, DRAGONLORD_PATH
from src.config import TILE_SIZE, SCALE, COLOR_KEY
# Tile Key:
# Index values for the map tiles corresponding to location on tilesheet.
from src.player import Player

all_impassable_tiles = (
    'ROOF', 'WALL', 'WOOD', 'DOOR', 'BARRIER', 'WEAPON_SIGN', 'INN_SIGN', 'MOUNTAINS', 'WATER', 'BOTTOM_COAST',
    'BOTTOM_LEFT_COAST', 'LEFT_COAST', 'TOP_LEFT_COAST', 'TOP_COAST', 'TOP_RIGHT_COAST', 'RIGHT_COAST',
    'BOTTOM_RIGHT_COAST', 'BOTTOM_TOP_LEFT_COAST', 'BOTTOM_TOP_COAST', 'BOTTOM_TOP_RIGHT_COAST', 'KING_LORIK',
    'DOWN_FACE_GUARD', 'LEFT_FACE_GUARD', 'UP_FACE_GUARD', 'RIGHT_FACE_GUARD', 'MAN', 'WOMAN', 'WISE_MAN', 'SOLDIER',
    'MERCHANT')

brick_line = [3] * 16
test_map = [
    brick_line,
    [3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3],
    [3, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 3],
    [3, 4, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 4, 3],
    [3, 4, 6, 7, 4, 4, 4, 4, 4, 4, 4, 4, 7, 6, 4, 3],
    [3, 4, 6, 7, 4, 3, 3, 3, 3, 3, 3, 4, 7, 6, 4, 3],
    [3, 4, 6, 7, 4, 3, 4, 4, 4, 4, 3, 4, 7, 6, 4, 3],
    [3, 4, 6, 7, 4, 3, 4, 3, 34, 4, 3, 4, 7, 6, 4, 3],
    [3, 4, 6, 7, 4, 3, 4, 4, 4, 4, 3, 4, 7, 6, 4, 3],
    [3, 4, 6, 7, 4, 3, 3, 3, 3, 3, 3, 4, 7, 6, 4, 3],
    [3, 4, 6, 7, 4, 4, 4, 4, 4, 4, 4, 4, 7, 6, 4, 3],
    [3, 4, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 4, 3],
    [3, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 3],
    [3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3],
    brick_line
]

roof_line = [0] * 27

tantegel_throne_room = [
    # Using the following dims: coord maps will be 0,0 top left and positive axes towards
    # bottom right.

    # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26
    roof_line,  # 0
    roof_line,  # 1
    roof_line,  # 2
    roof_line,  # 3
    roof_line,  # 4
    roof_line,  # 5
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 4, 3, 1, 0, 0, 0, 0, 0, 0, 0],  # 7
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 2, 2, 2, 2, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0],  # 8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 35, 2, 2, 3, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0],  # 9
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 34, 4, 4, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],  # 10
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 40, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],  # 11
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 39, 3, 37, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],  # 12
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 13
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 6, 1, 0, 0, 0, 0, 0, 0, 0],  # 14
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 15
    roof_line,  # 16
    roof_line,  # 17
    roof_line,  # 18
    roof_line,  # 19
    roof_line,  # 20
    roof_line,  # 21
    roof_line,  # 22
]

grass_line = [13] * 34

tantegel_courtyard = [
    grass_line,
    grass_line,
    grass_line,
    grass_line,
    grass_line,
    grass_line,
    grass_line,
    grass_line,
    [13, 13, 13, 1, 1, 1, 1, 1, 1, 1, 13, 13, 13, 13, 13, 13, 13, 13, 1, 1, 1, 1, 1, 1, 1, 13, 1, 1, 1, 13, 14, 13, 13,
     13],
    [13, 13, 13, 1, 3, 3, 3, 3, 3, 1, 13, 14, 13, 14, 14, 13, 14, 13, 1, 3, 3, 3, 3, 3, 1, 13, 1, 3, 1, 13, 13, 13, 13,
     13],
    [13, 13, 13, 1, 3, 3, 3, 3, 3, 1, 13, 13, 13, 13, 13, 13, 13, 13, 1, 3, 3, 3, 3, 3, 1, 13, 1, 2, 1, 13, 13, 13, 13,
     13],
    [13, 13, 13, 1, 3, 3, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 3, 3, 1, 13, 13, 13, 14, 14, 13, 13, 13, 13],
    [13, 13, 13, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 13, 14, 14, 14, 13, 13, 13, 13, 13],
    [13, 13, 13, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 1, 13, 13, 13, 13, 13, 13, 13, 13, 13],
    [13, 13, 13, 1, 1, 1, 1, 1, 3, 1, 3, 36, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 13, 13, 13],
    [13, 13, 13, 1, 3, 3, 3, 1, 3, 1, 7, 34, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 13, 13, 13],
    [13, 13, 13, 1, 3, 41, 3, 3, 3, 1, 3, 38, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 13, 13, 13],
    [13, 13, 13, 1, 3, 3, 3, 1, 3, 1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 13, 13, 13],
    [13, 13, 13, 1, 1, 1, 1, 1, 3, 1, 14, 14, 3, 3, 3, 3, 14, 14, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 13, 13, 13],
    [13, 13, 13, 1, 3, 3, 3, 1, 3, 1, 14, 14, 3, 3, 41, 3, 14, 14, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 13, 13, 13],
    [13, 13, 13, 1, 3, 40, 3, 1, 3, 1, 14, 13, 3, 3, 3, 3, 13, 14, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 13, 13, 13],
    [13, 13, 13, 1, 4, 3, 4, 5, 3, 1, 13, 42, 3, 3, 3, 3, 13, 13, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 13, 13, 13],
    [13, 13, 13, 1, 3, 4, 3, 1, 3, 1, 13, 13, 3, 3, 3, 3, 13, 13, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 13, 13, 13],
    [13, 13, 13, 1, 4, 3, 4, 1, 3, 1, 13, 3, 3, 3, 3, 3, 3, 13, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 13, 13, 13],
    [13, 13, 13, 1, 1, 1, 1, 1, 3, 1, 13, 3, 22, 22, 22, 22, 3, 13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 13, 13, 13],
    [13, 13, 13, 1, 3, 3, 3, 3, 3, 3, 3, 3, 22, 8, 8, 22, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 13, 13, 13],
    [13, 13, 13, 1, 3, 3, 3, 3, 3, 3, 3, 3, 22, 8, 8, 22, 3, 3, 3, 3, 3, 3, 3, 3, 1, 8, 8, 8, 8, 8, 1, 13, 13, 13],
    [13, 13, 13, 1, 1, 1, 3, 3, 1, 1, 1, 3, 22, 22, 22, 22, 3, 1, 1, 3, 3, 3, 3, 3, 1, 8, 8, 8, 8, 8, 1, 13, 13, 13],
    [13, 13, 13, 1, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 1, 39, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 22, 13, 13],
    [13, 13, 13, 1, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 3, 3, 3, 3, 1, 22, 13, 13],
    [13, 13, 13, 1, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 22, 13, 13],
    [13, 13, 13, 1, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 22, 22, 22, 22, 22, 22, 22, 13, 13],
    [13, 13, 13, 1, 3, 22, 22, 3, 3, 1, 3, 1, 3, 3, 3, 3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 22, 22, 22, 22, 22, 22, 22, 13,
     13],
    [13, 13, 13, 1, 22, 22, 22, 22, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 1, 22, 22, 22, 22, 22, 22, 22, 13,
     13],
    [13, 13, 13, 1, 22, 22, 22, 22, 3, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3, 3, 2, 3, 1, 22, 22, 22, 22, 22, 22, 22, 13,
     13],
    [13, 13, 13, 1, 22, 22, 22, 22, 22, 3, 3, 1, 39, 3, 3, 37, 1, 3, 3, 1, 3, 3, 1, 3, 1, 22, 22, 22, 22, 22, 22, 22,
     13, 13],
    [13, 13, 13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 22, 22, 22, 22, 22, 22, 22, 13, 13],
    [13, 13, 13, 22, 22, 13, 13, 13, 13, 13, 13, 13, 13, 3, 3, 13, 13, 13, 13, 13, 13, 13, 13, 22, 22, 22, 22, 22, 22,
     22, 22, 22,
     6, 13],
    grass_line,
    grass_line,
    grass_line,
    grass_line,
    grass_line,
    grass_line,
    grass_line,
    grass_line,
]

current_map = None


def parse_animated_spritesheet(sheet, is_roaming=False):
    """
    Parses spritesheets and creates image lists. If is_roaming is True
    the sprite will have four lists of images, one for each direction. If
    is_roaming is False then there will be one list of 2 images.
    """
    sheet.set_colorkey(COLOR_KEY)
    sheet.convert_alpha()
    # width, height = sheet.get_size()

    facing_down = []
    facing_left = []
    facing_up = []
    facing_right = []

    for i in range(0, 2):

        rect = (i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
        facing_down.append(sheet.subsurface(rect))

        if is_roaming:
            rect = ((i + 2) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
            facing_left.append(sheet.subsurface(rect))

            rect = ((i + 4) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
            facing_up.append(sheet.subsurface(rect))

            rect = ((i + 6) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
            facing_right.append(sheet.subsurface(rect))

    return facing_down, facing_left, facing_up, facing_right


class DragonWarriorMap:
    def __init__(self, map_tiles, hero_images):

        self.player = None
        self.player_sprites = None
        self.characters = []
        self.tiles_in_current_loaded_map = None
        self.layout = [[]]
        self.map_tiles = map_tiles
        self.roaming_characters = []

        self.hero_images = hero_images

        self.down_face_guard = None
        self.down_face_guard_sprites = RenderUpdates()

        self.up_face_guard = None
        self.up_face_guard_sprites = RenderUpdates()
        self.right_face_guard = None
        self.right_face_guard_sprites = RenderUpdates()

        self.man = None
        self.man_sprites = RenderUpdates()
        self.character_sprites = []

        self.impassable_tiles = all_impassable_tiles

        self.tile_group_dict = {}

        self.roof_group = Group()  # 0/
        self.wall_group = Group()  # 1
        self.wood_group = Group()  # 2
        self.brick_group = Group()  # 3
        self.chest_group = Group()  # 4
        self.door_group = Group()  # 5
        self.brick_stairdn_group = Group()  # 6
        self.brick_stairup_group = Group()  # 7
        self.barrier_group = Group()  # 8
        self.weapon_sign_group = Group()  # 9
        self.inn_sign_group = Group()  # 10
        self.castle_group = Group()  # 11
        self.town_group = Group()  # 12
        self.grass_group = Group()  # 13
        self.trees_group = Group()  # 14
        self.hills_group = Group()  # 15
        self.mountains_group = Group()  # 16
        self.cave_group = Group()  # 17
        self.grass_stairdn_group = Group()  # 18
        self.sand_group = Group()  # 19
        self.marsh_group = Group()  # 20
        self.bridge_group = Group()  # 21
        self.water_group = Group()  # 22
        self.bottom_coast_group = Group()  # 23
        self.bottom_left_coast_group = Group()  # 24
        self.left_coast_group = Group()  # 25
        self.top_left_coast_group = Group()  # 26
        self.top_coast_group = Group()  # 27
        self.top_right_coast_group = Group()  # 28
        self.right_coast_group = Group()  # 29
        self.bottom_right_coast_group = Group()  # 30
        self.bottom_top_left_coast_group = Group()  # 31
        self.bottom_top_coast_group = Group()  # 32
        self.bottom_top_right_coast_group = Group()  # 33

        self.tile_key = OrderedDict([
            ('ROOF', {'val': 0, 'group': self.roof_group}),
            ('WALL', {'val': 1, 'group': self.wall_group}),
            ('WOOD', {'val': 2, 'group': self.wood_group}),
            ('BRICK', {'val': 3, 'group': self.brick_group}),
            ('CHEST', {'val': 4, 'group': self.chest_group}),
            ('DOOR', {'val': 5, 'group': self.door_group}),
            ('BRICK_STAIRDN', {'val': 6, 'group': self.brick_stairdn_group}),
            ('BRICK_STAIRUP', {'val': 7, 'group': self.brick_stairup_group}),
            ('BARRIER', {'val': 8, 'group': self.barrier_group}),
            ('WEAPON_SIGN', {'val': 9, 'group': self.weapon_sign_group}),
            ('INN_SIGN', {'val': 10, 'group': self.inn_sign_group}),
            ('CASTLE', {'val': 11, 'group': self.castle_group}),
            ('TOWN', {'val': 12, 'group': self.town_group}),
            ('GRASS', {'val': 13, 'group': self.grass_group}),
            ('TREES', {'val': 14, 'group': self.trees_group}),
            ('HILLS', {'val': 15, 'group': self.hills_group}),
            ('MOUNTAINS', {'val': 16, 'group': self.mountains_group}),
            ('CAVE', {'val': 17, 'group': self.cave_group}),
            ('GRASS_STAIRDN', {'val': 18, 'group': self.grass_stairdn_group}),
            ('SAND', {'val': 19, 'group': self.sand_group}),
            ('MARSH', {'val': 20, 'group': self.marsh_group}),
            ('BRIDGE', {'val': 21, 'group': self.bridge_group}),
            ('WATER', {'val': 22, 'group': self.water_group}),
            ('BOTTOM_COAST', {'val': 23, 'group': self.bottom_coast_group}),
            ('BOTTOM_LEFT_COAST', {'val': 24, 'group': self.bottom_left_coast_group}),
            ('LEFT_COAST', {'val': 25, 'group': self.left_coast_group}),
            ('TOP_LEFT_COAST', {'val': 26, 'group': self.top_left_coast_group}),
            ('TOP_COAST', {'val': 27, 'group': self.top_coast_group}),
            ('TOP_RIGHT_COAST', {'val': 28, 'group': self.top_right_coast_group}),
            ('RIGHT_COAST', {'val': 29, 'group': self.right_coast_group}),
            ('BOTTOM_RIGHT_COAST', {'val': 30, 'group': self.bottom_right_coast_group}),
            ('BOTTOM_TOP_LEFT_COAST', {'val': 31, 'group': self.bottom_top_left_coast_group}),
            ('BOTTOM_TOP_COAST', {'val': 32, 'group': self.bottom_top_coast_group}),
            ('BOTTOM_TOP_RIGHT_COAST', {'val': 33, 'group': self.bottom_top_right_coast_group}),
        ])

        self.character_key = OrderedDict([
            ('HERO', {'val': 34}),
            ('KING_LORIK', {'val': 35}),
            ('DOWN_FACE_GUARD', {'val': 36}),
            ('LEFT_FACE_GUARD', {'val': 37}),
            ('UP_FACE_GUARD', {'val': 38}),
            ('RIGHT_FACE_GUARD', {'val': 39}),
            ('ROAMING_GUARD', {'val': 40}),
            ('MAN', {'val': 41}),
            ('WOMAN', {'val': 42}),
            ('WISE_MAN', {'val': 43}),
            ('SOLDIER', {'val': 44}),
            ('MERCHANT', {'val': 45}),
            ('PRINCESS_GWAELIN', {'val': 46}),
            ('DRAGONLORD', {'val': 47}),
        ])
        self.tile_character_key = self.tile_key.update(self.character_key)

    def get_tile_by_value(self, position):
        return list(self.tile_key.keys())[position]

    def get_initial_character_location(self, character_name):
        layout_numpy_array = np.array(self.layout)
        hero_layout_position = np.asarray(np.where(layout_numpy_array == self.tile_key[character_name]['val'])).T
        return hero_layout_position

    def draw_map(self, surface):
        """
        Draw static sprites on the big map.
        """
        for col_dict in self.tile_key.values():
            group = col_dict.get('group')
            if group is not None:
                group.draw(surface)

    def load_map(self):
        current_loaded_map = self

        x_offset = TILE_SIZE / 2
        y_offset = TILE_SIZE / 2

        layout_values = [self.get_tile_by_value(tile) for row in self.layout for tile in row]
        tiles_in_current_loaded_map = list(filter(lambda n: n in layout_values, list(self.tile_key.keys())))
        self.impassable_tiles = tuple(set(tiles_in_current_loaded_map) & set(all_impassable_tiles))
        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                self.center_pt = [(x * TILE_SIZE) + x_offset,
                                  (y * TILE_SIZE) + y_offset]
                self.map_floor_tiles(x, y)
                self.map_character_tiles(current_loaded_map, x, y)

        self.add_tile(tile_value=self.tile_key['BRICK']['val'], tile_group=self.brick_group)

    def map_character_tiles(self, current_loaded_map, x, y):
        if self.layout[y][x] == self.character_key['HERO']['val']:
            self.map_player(current_loaded_map)
        elif self.layout[y][x] == self.character_key['KING_LORIK']['val']:
            self.map_two_sided_npc(path=KING_LORIK_PATH, name='KING_LORIK', underlying_tile='BRICK')
        elif self.layout[y][x] == self.character_key['DOWN_FACE_GUARD']['val']:
            self.map_four_sided_npc(direction=Direction.DOWN.value, name='DOWN_FACE_GUARD',
                                    underlying_tile='BRICK',
                                    image_path=ROAMING_GUARD_PATH)
        elif self.layout[y][x] == self.character_key['LEFT_FACE_GUARD']['val']:
            self.map_four_sided_npc(direction=Direction.LEFT.value, name='LEFT_FACE_GUARD',
                                    underlying_tile='BRICK',
                                    image_path=ROAMING_GUARD_PATH)
        elif self.layout[y][x] == self.character_key['UP_FACE_GUARD']['val']:
            self.map_four_sided_npc(direction=Direction.UP.value, name='UP_FACE_GUARD',
                                    underlying_tile='BRICK',
                                    image_path=ROAMING_GUARD_PATH)
        elif self.layout[y][x] == self.character_key['RIGHT_FACE_GUARD']['val']:
            self.map_four_sided_npc(direction=Direction.RIGHT.value, name='RIGHT_FACE_GUARD',
                                    underlying_tile='BRICK',
                                    image_path=ROAMING_GUARD_PATH)
        elif self.layout[y][x] == self.character_key['ROAMING_GUARD']['val']:
            self.map_four_sided_npc(direction=Direction.DOWN.value, name='ROAMING_GUARD',
                                    underlying_tile='BRICK',
                                    image_path=ROAMING_GUARD_PATH, is_roaming=True)
        elif self.layout[y][x] == self.character_key['MAN']['val']:
            self.map_four_sided_npc(direction=Direction.DOWN.value, name='MAN',
                                    underlying_tile='BRICK',
                                    image_path=MAN_PATH)
        elif self.layout[y][x] == self.character_key['WOMAN']['val']:
            self.map_four_sided_npc(direction=Direction.DOWN.value, name='WOMAN',
                                    underlying_tile='GRASS',
                                    image_path=WOMAN_PATH)
        elif self.layout[y][x] == self.character_key['WISE_MAN']['val']:
            self.map_four_sided_npc(direction=Direction.DOWN.value, name='WISE_MAN',
                                    underlying_tile='BRICK',
                                    image_path=WISE_MAN_PATH, is_roaming=True)
        elif self.layout[y][x] == self.character_key['SOLDIER']['val']:
            self.map_four_sided_npc(direction=Direction.DOWN.value, name='SOLDIER',
                                    underlying_tile='BRICK',
                                    image_path=SOLDIER_PATH, is_roaming=True)
        elif self.layout[y][x] == self.character_key['MERCHANT']['val']:
            self.map_four_sided_npc(direction=Direction.DOWN.value, name='MERCHANT',
                                    underlying_tile='BRICK',
                                    image_path=MERCHANT_PATH, is_roaming=True)
        elif self.layout[y][x] == self.character_key['PRINCESS_GWAELIN']['val']:
            self.map_two_sided_npc(path=PRINCESS_GWAELIN_PATH, name='PRINCESS_GWAELIN', underlying_tile='BRICK')
        elif self.layout[y][x] == self.character_key['DRAGONLORD']['val']:
            self.map_four_sided_npc(direction=Direction.DOWN.value, name='DRAGONLORD',
                                    underlying_tile='BRICK',
                                    image_path=DRAGONLORD_PATH, is_roaming=True)

    def map_four_sided_npc(self, direction, name, underlying_tile, image_path, is_roaming=False):
        sheet = get_image(image_path)
        sheet = scale(sheet, (sheet.get_width() * SCALE, sheet.get_height() * SCALE))
        images = parse_animated_spritesheet(sheet, is_roaming=True)
        character_sprites = RenderUpdates()
        character = AnimatedSprite(self.center_pt, direction,
                                   images[Direction.DOWN.value],
                                   images[Direction.LEFT.value],
                                   images[Direction.UP.value],
                                   images[Direction.RIGHT.value], name=name)
        if is_roaming:
            character.position = self.get_initial_character_location(
                character_name=character.name)
            self.roaming_characters.append(character)
        character_sprites.add(character)
        self.add_tile(tile_value=self.tile_key[underlying_tile]['val'],
                      tile_group=self.tile_key[underlying_tile]['group'])
        self.characters.append(character)
        self.character_sprites.append(character_sprites)

    def map_two_sided_npc(self, path, name, underlying_tile):
        sprites = RenderUpdates()
        sheet = get_image(path)
        sheet = scale(sheet, (sheet.get_width() * SCALE, sheet.get_height() * SCALE))
        images = parse_animated_spritesheet(sheet)
        character = AnimatedSprite(self.center_pt, Direction.DOWN.value,
                                   images[0], name=name)
        sprites.add(character)
        self.characters.append(character)
        self.character_sprites.append(sprites)
        self.add_tile(tile_value=self.tile_key[underlying_tile]['val'], tile_group=self.tile_key[underlying_tile]['group'])

    def map_player(self, current_loaded_map, underlying_tile='BRICK'):
        self.player = Player(center_point=self.center_pt,
                             down_images=self.hero_images[Direction.DOWN.value],
                             left_images=self.hero_images[Direction.LEFT.value],
                             up_images=self.hero_images[Direction.UP.value],
                             right_images=self.hero_images[Direction.RIGHT.value])
        # Make player start facing up if in Tantegel Throne Room, else face down.
        self.player_sprites = RenderUpdates(self.player)
        if isinstance(current_loaded_map, TantegelThroneRoom):
            self.player.direction = Direction.UP.value
        self.add_tile(tile_value=self.tile_key[underlying_tile]['val'], tile_group=self.tile_key[underlying_tile]['group'])
        self.characters.append(self.player)
        self.character_sprites.append(self.player_sprites)

    def map_floor_tiles(self, x, y):
        for tile, tile_dict in self.tile_key.items():
            if self.layout[y][x] == tile_dict['val'] and 'group' in tile_dict.keys():
                self.add_tile(tile_value=tile_dict['val'], tile_group=tile_dict['group'])

    def add_tile(self, tile_value, tile_group):
        if tile_value < 10:
            tile = BaseSprite(self.center_pt, self.map_tiles[tile_value][0])
        elif 20 > tile_value >= 10:
            tile = BaseSprite(self.center_pt, self.map_tiles[tile_value - 11][1])
        elif 30 > tile_value >= 20:
            tile = BaseSprite(self.center_pt, self.map_tiles[tile_value - 22][2])
        else:
            print("Invalid tile.")
            tile = None
        tile_group.add(tile)


class TestMap(DragonWarriorMap):

    def __init__(self, map_tiles, hero_images):
        super().__init__(map_tiles, hero_images)
        self.layout = test_map
        self.height = len(self.layout * TILE_SIZE)
        self.width = len(self.layout[0] * TILE_SIZE)
        self.music_file_path = village_music
        play_music(self.music_file_path)


class TantegelThroneRoom(DragonWarriorMap):
    """
    This is the first map in the game.
    """

    def __init__(self, map_tiles, hero_images):
        super().__init__(map_tiles, hero_images)
        self.layout = tantegel_throne_room
        self.height = len(self.layout * TILE_SIZE)
        self.width = len(self.layout[0] * TILE_SIZE)
        self.music_file_path = tantegel_castle_throne_room_music
        play_music(self.music_file_path)


class TantegelCourtyard(DragonWarriorMap):
    def __init__(self, map_tiles, hero_images):
        super().__init__(map_tiles, hero_images)
        self.layout = tantegel_courtyard
        self.height = len(self.layout * TILE_SIZE)
        self.width = len(self.layout[0] * TILE_SIZE)
        self.music_file_path = tantegel_castle_courtyard_music
        play_music(self.music_file_path)
