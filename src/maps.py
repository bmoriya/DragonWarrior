from collections import OrderedDict
from os.path import join

import numpy as np
from pygame.sprite import Group, RenderUpdates
from pygame.transform import scale

from src.RoamingCharacter import RoamingCharacter
from src.animated_sprite import AnimatedSprite
from src.base_sprite import BaseSprite
from src.common import Direction, tantegel_castle_throne_room_music, KING_LORIK_PATH, get_image, \
    GUARD_PATH, MAN_PATH, village_music, tantegel_castle_courtyard_music, WOMAN_PATH, WISE_MAN_PATH, \
    SOLDIER_PATH, MERCHANT_PATH, PRINCESS_GWAELIN_PATH, DRAGONLORD_PATH, UNARMED_HERO_PATH, MAP_TILES_PATH, \
    overworld_music
from src.config import TILE_SIZE, SCALE, COLOR_KEY, IMAGES_DIR
# Tile Key:
# Index values for the map tiles corresponding to location on tilesheet.
from src.player import Player

all_impassable_tiles = (
    'ROOF', 'WALL', 'WOOD', 'DOOR', 'BARRIER', 'WEAPON_SIGN', 'INN_SIGN', 'MOUNTAINS', 'WATER', 'BOTTOM_COAST',
    'BOTTOM_LEFT_COAST', 'LEFT_COAST', 'TOP_LEFT_COAST', 'TOP_COAST', 'TOP_RIGHT_COAST', 'RIGHT_COAST',
    'BOTTOM_RIGHT_COAST', 'BOTTOM_TOP_LEFT_COAST', 'BOTTOM_TOP_COAST', 'BOTTOM_TOP_RIGHT_COAST', 'KING_LORIK',
    'DOWN_FACE_GUARD', 'LEFT_FACE_GUARD', 'UP_FACE_GUARD', 'RIGHT_FACE_GUARD', 'MAN', 'WOMAN', 'WISE_MAN', 'SOLDIER',
    'MERCHANT')

ROOF = 0
WALL = 1
WOOD = 2
BRICK = 3
CHEST = 4
DOOR = 5
BRICK_STAIRDN = 6
BRICK_STAIRUP = 7
BARRIER = 8
WEAPON_SIGN = 9
INN_SIGN = 10
CASTLE = 11
TOWN = 12
GRASS = 13
TREES = 14
HILLS = 15
MOUNTAINS = 16
CAVE = 17
GRASS_STAIRDN = 18
SAND = 19
MARSH = 20
BRIDGE = 21
WATER = 22
BOTTOM_COAST = 23
BOTTOM_LEFT_COAST = 24
LEFT_COAST = 25
TOP_LEFT_COAST = 26
TOP_COAST = 27
TOP_RIGHT_COAST = 28
RIGHT_COAST = 29
BOTTOM_RIGHT_COAST = 30
BOTTOM_TOP_LEFT_COAST = 31
BOTTOM_TOP_COAST = 32
BOTTOM_TOP_RIGHT_COAST = 33

character_key = OrderedDict([
    ('HERO',
     {'val': 34, 'four_sided': True, 'path': UNARMED_HERO_PATH, 'roaming': False, 'underlying_tile': 'BRICK'}),
    ('KING_LORIK',
     {'val': 35, 'four_sided': False, 'path': KING_LORIK_PATH, 'roaming': False, 'underlying_tile': 'BRICK'}),
    ('DOWN_FACE_GUARD',
     {'val': 36, 'four_sided': True, 'path': GUARD_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
      'underlying_tile': 'BRICK'}),
    ('LEFT_FACE_GUARD',
     {'val': 37, 'four_sided': True, 'path': GUARD_PATH, 'roaming': False, 'direction': Direction.LEFT.value,
      'underlying_tile': 'BRICK'}),
    ('UP_FACE_GUARD',
     {'val': 38, 'four_sided': True, 'path': GUARD_PATH, 'roaming': False, 'direction': Direction.UP.value,
      'underlying_tile': 'BRICK'}),
    ('RIGHT_FACE_GUARD',
     {'val': 39, 'four_sided': True, 'path': GUARD_PATH, 'roaming': False, 'direction': Direction.RIGHT.value,
      'underlying_tile': 'BRICK'}),
    ('ROAMING_GUARD',
     {'val': 40, 'four_sided': True, 'path': GUARD_PATH, 'roaming': True, 'direction': Direction.DOWN.value,
      'underlying_tile': 'BRICK'}),
    ('MAN',
     {'val': 41, 'four_sided': True, 'path': MAN_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
      'underlying_tile': 'BRICK'}),
    ('WOMAN',
     {'val': 42, 'four_sided': True, 'path': WOMAN_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
      'underlying_tile': 'GRASS'}),
    ('WISE_MAN',
     {'val': 43, 'four_sided': True, 'path': WISE_MAN_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
      'underlying_tile': 'BRICK'}),
    ('SOLDIER',
     {'val': 44, 'four_sided': True, 'path': SOLDIER_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
      'underlying_tile': 'BRICK'}),
    ('MERCHANT',
     {'val': 45, 'four_sided': True, 'path': MERCHANT_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
      'underlying_tile': 'BRICK'}),
    ('PRINCESS_GWAELIN',
     {'val': 46, 'four_sided': False, 'path': PRINCESS_GWAELIN_PATH, 'roaming': False,
      'direction': Direction.DOWN.value, 'underlying_tile': 'BRICK'}),
    ('DRAGONLORD',
     {'val': 47, 'four_sided': True, 'path': DRAGONLORD_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
      'underlying_tile': 'BRICK'}),
])

all_characters_values = [character_dict['val'] for character_dict in character_key.values()]
all_characters_values.insert(0, 3)
all_characters_values.append(3)

brick_line = tuple([3] * 16)
test_map = [
    brick_line,
    [3] + [4] * 14 + [3],
    [3, 4] + [6] * 12 + [4, 3],
    [3, 4, 6] + [7] * 10 + [6, 4, 3],
    [3, 4, 6, 7] + [4] * 8 + [7, 6, 4, 3],
    [3, 4, 6, 7, 4] + [3] * 6 + [4, 7, 6, 4, 3],
    [3, 40, 40, 40, 40, 40, 40, 40, 40, 4, 3, 4, 7, 6, 4, 3],
    all_characters_values,
    [3, 4, 6, 7, 4, 3, 4, 4, 4, 4, 3, 4, 7, 6, 4, 3],
    [3, 4, 6, 7, 4] + [3] * 6 + [4, 7, 6, 4, 3],
    [3, 4, 6, 7] + [4] * 8 + [7, 6, 4, 3],
    [3, 4, 6] + [7] * 10 + [6, 4, 3],
    [3, 4] + [6] * 12 + [4, 3],
    [3] + [4] * 14 + [3],
    brick_line
]

# test_map = [[3, 3],
#             [34, 3]]

roof_line = tuple([ROOF] * 27)

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
    [ROOF] * 10 + [1] * 10 + [ROOF] * 7,  # 6
    [ROOF] * 10 + [1, 3, 3, 3, 3, 3, 3, 4, 3, 1] + [ROOF] * 7,  # 7
    [ROOF] * 10 + [1, 3, 2, 2, 2, 2, 2, 2, 3, 1] + [ROOF] * 7,  # 8
    [ROOF] * 10 + [1, 3, 2, 35, 2, 2, 3, 2, 3, 1] + [ROOF] * 7,  # 9
    [ROOF] * 10 + [1, 3, 3, 34, 4, 4, 3, 3, 3, 1] + [ROOF] * 7,  # 10
    [ROOF] * 10 + [1, 3, 3, 3, 3, 3, 40, 3, 3, 1] + [ROOF] * 7,  # 11
    [ROOF] * 10 + [1, 3, 3, 39, 3, 37, 3, 3, 3, 1] + [ROOF] * 7,  # 12
    [ROOF] * 10 + [1, 1, 1, 1, 3, 1, 1, 1, 1, 1] + [ROOF] * 7,  # 13
    [ROOF] * 10 + [1, 3, 3, 3, 3, 3, 3, 3, 6, 1] + [ROOF] * 7,  # 14
    [ROOF] * 10 + [1] * 10 + [ROOF] * 7,  # 15
    roof_line,  # 16
    roof_line,  # 17
    roof_line,  # 18
    roof_line,  # 19
    roof_line,  # 20
    roof_line,  # 21
]

courtyard_grass_line = [GRASS] * 30

tantegel_courtyard = [
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
    [1] * 7 + [13] * 8 + [1] * 7 + [13] + [1, 1, 1] + [13, 14] + [13] * 2,
    [1] + [3] * 5 + [1, 13, 14, 13, 14, 14, 13, 14, 13, 1] + [3] * 5 + [1, 13, 1, 45, 1] + [13] * 4,
    [1] + [3] * 5 + [1] + [13] * 8 + [1] + [3] * 5 + [1, 13, 1, 2, 1] + [13] * 4,
    [1] + [3, 3, 1, 3, 3] + [1] * 4 + [3, 3] + [1] * 4 + [3, 3, 1] * 2 + [13, 13, 13, 14, 14] + [13] * 3,
    [1] + [3] * 20 + [1, 13, 14, 14, 14] + [13] * 4,
    [1] + [3] * 5 + [1] * 10 + [3] * 5 + [1] + [13] * 5 + [42] + [13] * 2,
    [1] * 5 + [3, 1, 3, 36] + [3] * 6 + [1, 1, 1, 5] + [1] * 5 + [3, 1, 1, 1] + [13] * 2,
    [1] + [3, 3, 3, 1, 3, 1, 7, 34] + [3] * 4 + [1, 3] + [1] + [3] * 11 + [1] + [13] * 2,
    [1] + [3, 41, 3, 3, 3, 1, 3, 38] + [3] * 6 + [1] + [3] * 11 + [1] + [13] * 2,
    [1] + [3, 3, 3, 1, 3, 1, 1, 1] + [3] * 4 + [1] * 12 + [3, 3, 1] + [13] * 2,
    [1] * 5 + [3, 1, 14, 14] + [3] * 4 + [14, 14, 1] + [3, 3, 1] * 4 + [13] * 2,
    [1] + [3, 3, 3, 1, 3, 1, 14, 14, 3, 3, 41, 3, 14, 14, 1] + [3, 3, 1] * 4 + [13] * 2,
    [1] + [3, 40, 3, 1, 3, 1, 14, 13] + [3] * 4 + [13, 14] + [1] + [3] * 11 + [1] + [13] * 2,
    [1] + [4, 3, 4, 5, 3, 1, 13, 42] + [3] * 4 + [13, 13] + [1] + [3] * 11 + [1] + [13] * 2,
    [1] + [3, 4, 3, 1, 3, 1, 13, 13] + [3] * 4 + [13, 13, 1] + [3, 3, 1] * 4 + [13] * 2,
    [1] + [4, 3, 4, 1, 3, 1, 13] + [3] * 6 + [13, 1] + [3, 3, 1] * 4 + [13] * 2,
    [1] * 5 + [3, 1, 13, 3] + [22] * 4 + [3, 13] + [1] * 10 + [3, 1, 1] + [13] * 2,
    [1] + [3] * 8 + [22, 8, 8, 22] + [3] * 6 + [3, 3, 1] + [3] * 5 + [1] + [13] * 2,
    [1] + [3] * 8 + [22, 8, 8, 22] + [3] * 6 + [3, 3, 1] + [8] * 5 + [1] + [13] * 2,
    [1] + [1, 1, 3, 3, 1, 1, 1, 3, 22, 22, 22, 22, 3, 1, 1] + [3] * 5 + [1] + [8] * 5 + [1] + [13] * 2,
    [1] + [3] * 5 + [3, 1] + [3] * 6 + [1, 39] + [3] * 5 + [1] + [3] * 5 + [1] + [13] * 2,
    [1] + [3] * 5 + [3, 1, 1] + [3] * 4 + [1] * 6 + [3, 3, 1, 44] + [3] * 4 + [1, 22] + [13],
    [1] + [3, 3, 1] + [3] * 4 + [1] + [3] * 4 + [1] + [3] * 7 + [1] * 6 + [1, 22] + [13],
    [1] + [3] * 5 + [3, 3, 1] + [3] * 4 + [1] + [3] * 6 + [3, 1] + [22] * 7 + [13],
    [1] + [3, 22, 22, 3, 3, 1, 45, 1] + [3] * 4 + [1, 3, 3] + [1] * 6 + [22] * 7 + [13],
    [1] + [22] * 4 + [3, 45, 3, 1] + [3] * 4 + [1] + [3, 3, 1] * 2 + [3, 1] + [22] * 7 + [13],
    [1] + [22] * 4 + [3] + [3, 3, 1, 1] * 2 + [3] * 5 + [2, 43, 1] + [22] * 7 + [13],
    [1] + [22] * 5 + [3, 3, 1, 39, 3, 3, 37, 1] + [3, 3, 1] * 2 + [3, 1] + [22] * 7 + [13],
    [1] * 10 + [3, 3] + [1] * 10 + [22] * 7 + [13],
    [22, 22] + [13] * 8 + [3, 3] + [13] * 8 + [22] * 9 + [6],
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
    courtyard_grass_line,
]

tantegel_courtyard = [[13] * 7 + row + [13] * 7 for row in tantegel_courtyard]

overworld = [

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

    facing_down, facing_left, facing_up, facing_right = [], [], [], []

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
    def __init__(self, hero_images):

        # Character variables

        self.player = None
        self.player_sprites = None
        self.characters = []
        self.roaming_characters = []
        self.hero_images = hero_images
        self.character_sprites = []

        # Map variables

        self.tiles_in_current_loaded_map = None
        self.layout = [[]]
        self.layout_numpy_array = np.empty(0)
        self.center_pt = None
        self.map_tiles = parse_map_tiles(map_path=MAP_TILES_PATH)
        self.impassable_tiles = all_impassable_tiles
        self.tile_group_dict = {}
        self.staircases = {}

        self.roof_group = Group()  # 0
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
        self.tile_key.update(character_key)

    def get_tile_by_value(self, position):
        return list(self.tile_key.keys())[position]

    def get_initial_character_location(self, character_name):
        hero_layout_position = np.asarray(np.where(self.layout_numpy_array == self.tile_key[character_name]['val'])).T
        return hero_layout_position

    # def get_staircase_locations(self):
    #     staircase_locations = np.asarray(np.where(self.layout_numpy_array == self.tile_key['BRICK_STAIRDN']['val'])).T
    #     return staircase_locations

    def draw_map(self, surface):
        """
        Draw static sprites on the big map.
        """
        for col_dict in self.tile_key.values():
            group = col_dict.get('group')
            if group is not None:
                group.draw(surface)

    def load_map(self):
        # start_time = time.time()
        current_loaded_map = self

        x_offset = TILE_SIZE // 2
        y_offset = TILE_SIZE // 2

        tiles_in_current_loaded_map = set([self.get_tile_by_value(tile) for row in self.layout for tile in row])
        self.impassable_tiles = tuple(tiles_in_current_loaded_map & set(all_impassable_tiles))
        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                self.center_pt = (x * TILE_SIZE) + x_offset, (y * TILE_SIZE) + y_offset
                self.map_floor_tiles(x, y)
                self.map_character_tiles(current_loaded_map, x, y)
        # print("--- %s seconds ---" % (time.time() - start_time))

    def map_character_tiles(self, current_loaded_map, x, y):
        for character, character_dict in character_key.items():
            if self.layout[y][x] >= 34:
                if self.layout[y][x] == character_dict['val']:
                    if self.layout[y][x] == character_key['HERO']['val']:
                        self.map_player(current_loaded_map, character_dict['underlying_tile'])
                    elif character_dict['four_sided']:
                        self.map_four_sided_npc(name=character, direction=character_dict['direction'],
                                                underlying_tile=character_dict['underlying_tile'],
                                                image_path=character_dict['path'], is_roaming=character_dict['roaming'])
                    else:
                        self.map_two_sided_npc(image_path=character_dict['path'], name=character,
                                               underlying_tile=character_dict['underlying_tile'])

    def map_four_sided_npc(self, name, direction, underlying_tile, image_path, is_roaming=False):
        sheet = get_image(image_path)
        sheet = scale(sheet, (sheet.get_width() * SCALE, sheet.get_height() * SCALE))
        images = parse_animated_spritesheet(sheet, is_roaming=True)
        character_sprites = RenderUpdates()
        if is_roaming:
            character = RoamingCharacter(self.center_pt, direction,
                                         images[Direction.DOWN.value],
                                         images[Direction.LEFT.value],
                                         images[Direction.UP.value],
                                         images[Direction.RIGHT.value], name=name)
            character.position = self.get_initial_character_location(character_name=character.name)
            self.roaming_characters.append(character)
        else:
            character = AnimatedSprite(self.center_pt, direction,
                                       images[Direction.DOWN.value],
                                       images[Direction.LEFT.value],
                                       images[Direction.UP.value],
                                       images[Direction.RIGHT.value], name=name)
        character_sprites.add(character)
        self.add_tile(tile_value=self.tile_key[underlying_tile]['val'],
                      tile_group=self.tile_key[underlying_tile]['group'])
        self.characters.append(character)
        self.character_sprites.append(character_sprites)

    def map_two_sided_npc(self, image_path, name, underlying_tile):
        sprites = RenderUpdates()
        sheet = get_image(image_path)
        sheet = scale(sheet, (sheet.get_width() * SCALE, sheet.get_height() * SCALE))
        images = parse_animated_spritesheet(sheet)
        character = AnimatedSprite(self.center_pt, Direction.DOWN.value,
                                   images[0], name=name)
        sprites.add(character)
        self.characters.append(character)
        self.character_sprites.append(sprites)
        self.add_tile(tile_value=self.tile_key[underlying_tile]['val'],
                      tile_group=self.tile_key[underlying_tile]['group'])

    def map_player(self, current_loaded_map, underlying_tile):
        # TODO(ELF): Fix underlying tiles so that they aren't all bricks.
        self.player = Player(center_point=self.center_pt,
                             down_images=self.hero_images[Direction.DOWN.value],
                             left_images=self.hero_images[Direction.LEFT.value],
                             up_images=self.hero_images[Direction.UP.value],
                             right_images=self.hero_images[Direction.RIGHT.value])
        # Make player start facing up if in Tantegel Throne Room, else face down.
        self.player_sprites = RenderUpdates(self.player)
        if isinstance(current_loaded_map, TantegelThroneRoom):
            self.player.direction = Direction.UP.value
        self.add_tile(tile_value=self.tile_key[underlying_tile]['val'],
                      tile_group=self.tile_key[underlying_tile]['group'])
        self.characters.append(self.player)
        self.character_sprites.append(self.player_sprites)

    def map_floor_tiles(self, x, y):
        for tile, tile_dict in self.tile_key.items():
            if self.layout[y][x] <= 33:
                if self.layout[y][x] == tile_dict['val']:
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

    def __init__(self, hero_images):
        super().__init__(hero_images)
        self.layout = test_map
        self.layout_numpy_array = np.array(self.layout)
        self.height = len(self.layout * TILE_SIZE)
        self.width = len(self.layout[0] * TILE_SIZE)
        self.music_file_path = village_music


class TantegelThroneRoom(DragonWarriorMap):
    """
    This is the first map in the game.
    """

    def __init__(self, hero_images):
        super().__init__(hero_images)
        self.layout = tantegel_throne_room
        self.layout_numpy_array = np.array(self.layout)
        self.height = len(self.layout * TILE_SIZE)
        self.width = len(self.layout[0] * TILE_SIZE)
        self.staircases = {(14, 18): {'map': TantegelCourtyard(self.hero_images), 'stair_direction': 'down'}}
        self.music_file_path = tantegel_castle_throne_room_music


class TantegelCourtyard(DragonWarriorMap):
    def __init__(self, hero_images):
        super().__init__(hero_images)
        self.layout = tantegel_courtyard
        self.layout_numpy_array = np.array(self.layout)
        self.height = len(self.layout * TILE_SIZE)
        self.width = len(self.layout[0] * TILE_SIZE)
        self.music_file_path = tantegel_castle_courtyard_music


class Overworld(DragonWarriorMap):
    def __init__(self, hero_images):
        super().__init__(hero_images)
        self.layout = overworld
        self.layout_tiles = parse_map_tiles(join(IMAGES_DIR, 'alefgard.gif'))
        self.layout_numpy_array = np.array(self.layout)
        self.height = len(self.layout * TILE_SIZE)
        self.width = len(self.layout[0] * TILE_SIZE)
        self.music_file_path = overworld_music


def parse_map_tiles(map_path):
    map_sheet = get_image(map_path).convert()
    map_tilesheet = scale(map_sheet, (map_sheet.get_width() * SCALE, map_sheet.get_height() * SCALE))
    map_tiles = []
    width, height = map_tilesheet.get_size()

    for x in range(0, width // TILE_SIZE):
        row = []
        map_tiles.append(row)

        for y in range(0, height // TILE_SIZE):
            rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            row.append(map_tilesheet.subsurface(rect))
    return map_tiles
