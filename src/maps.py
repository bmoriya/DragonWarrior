import numpy as np
from pygame.sprite import Group, LayeredDirty
from pygame.transform import scale
from typing import Tuple

from src.animated_sprite import AnimatedSprite
from src.base_sprite import BaseSprite
from src.common import Direction, tantegel_castle_throne_room_music, KING_LORIK_PATH, get_image, \
    GUARD_PATH, MAN_PATH, tantegel_castle_courtyard_music, WOMAN_PATH, WISE_MAN_PATH, \
    SOLDIER_PATH, MERCHANT_PATH, PRINCESS_GWAELIN_PATH, DRAGONLORD_PATH, UNARMED_HERO_PATH, MAP_TILES_PATH, \
    overworld_music
from src.config import TILE_SIZE, SCALE, COLOR_KEY
# Tile Key:
# Index values for the map tiles corresponding to location on tilesheet.
from src.player import Player
from src.roaming_character import RoamingCharacter

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
BOTTOM_TOP_RIGHT_COAST = 32


def parse_animated_spritesheet(sheet, is_roaming=False) -> Tuple[list, list, list, list]:
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
    def __init__(self, hero_images, layout):

        # Character variables

        self.scale = SCALE
        self.player = None
        self.player_sprites = None
        self.characters = []
        self.roaming_characters = []
        self.hero_images = hero_images
        self.character_sprites = []

        # Map variables

        self.tiles_in_current_loaded_map = None
        self.layout = layout
        self.layout_numpy_array = np.array(self.layout)
        self.center_pt = None
        self.map_tiles = parse_map_tiles(map_path=MAP_TILES_PATH)
        self.impassable_tiles = all_impassable_tiles
        self.tile_group_dict = {}
        self.staircases = {}
        self.height = len(self.layout) * TILE_SIZE
        self.width = len(self.layout[0]) * TILE_SIZE

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
        self.bottom_top_right_coast_group = Group()  # 32

        self.floor_tile_key = dict([
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
            ('BOTTOM_TOP_RIGHT_COAST', {'val': 32, 'group': self.bottom_top_right_coast_group}),
        ])
        self.character_key = dict([
            ('HERO',
             {'val': 33, 'four_sided': True, 'path': UNARMED_HERO_PATH, 'roaming': False,
              'underlying_tile': self.hero_underlying_tile()}),
            ('KING_LORIK',
             {'val': 34, 'four_sided': False, 'path': KING_LORIK_PATH, 'roaming': False, 'underlying_tile': 'BRICK'}),
            ('DOWN_FACE_GUARD',
             {'val': 35, 'four_sided': True, 'path': GUARD_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
              'underlying_tile': 'BRICK'}),
            ('LEFT_FACE_GUARD',
             {'val': 36, 'four_sided': True, 'path': GUARD_PATH, 'roaming': False, 'direction': Direction.LEFT.value,
              'underlying_tile': 'BRICK'}),
            ('UP_FACE_GUARD',
             {'val': 37, 'four_sided': True, 'path': GUARD_PATH, 'roaming': False, 'direction': Direction.UP.value,
              'underlying_tile': 'BRICK'}),
            ('RIGHT_FACE_GUARD',
             {'val': 38, 'four_sided': True, 'path': GUARD_PATH, 'roaming': False, 'direction': Direction.RIGHT.value,
              'underlying_tile': 'BRICK'}),
            ('ROAMING_GUARD',
             {'val': 39, 'four_sided': True, 'path': GUARD_PATH, 'roaming': True, 'direction': Direction.DOWN.value,
              'underlying_tile': 'BRICK'}),
            ('MAN',
             {'val': 40, 'four_sided': True, 'path': MAN_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
              'underlying_tile': 'BRICK'}),
            ('WOMAN',
             {'val': 41, 'four_sided': True, 'path': WOMAN_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
              'underlying_tile': 'GRASS'}),
            ('WISE_MAN',
             {'val': 42, 'four_sided': True, 'path': WISE_MAN_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
              'underlying_tile': 'BRICK'}),
            ('SOLDIER',
             {'val': 43, 'four_sided': True, 'path': SOLDIER_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
              'underlying_tile': 'BRICK'}),
            ('MERCHANT',
             {'val': 44, 'four_sided': True, 'path': MERCHANT_PATH, 'roaming': False, 'direction': Direction.DOWN.value,
              'underlying_tile': 'BRICK'}),
            ('PRINCESS_GWAELIN',
             {'val': 45, 'four_sided': False, 'path': PRINCESS_GWAELIN_PATH, 'roaming': False,
              'direction': Direction.DOWN.value, 'underlying_tile': 'BRICK'}),
            ('DRAGONLORD',
             {'val': 46, 'four_sided': True, 'path': DRAGONLORD_PATH, 'roaming': False,
              'direction': Direction.DOWN.value,
              'underlying_tile': 'BRICK'}),
        ])
        self.tile_key = dict(list(self.floor_tile_key.items()) + list(self.character_key.items()))
        self.all_floor_sprite_groups = [val.get('group') for val in self.floor_tile_key.values()]

    def get_tile_by_value(self, position: int) -> str:
        return list(self.tile_key.keys())[position]

    def get_initial_character_location(self, character_name: str) -> np.ndarray:
        hero_layout_position = np.asarray(
            np.where(self.layout_numpy_array == self.character_key[character_name]['val'])).T
        return hero_layout_position

    # def get_staircase_locations(self):
    #     staircase_locations = np.asarray(np.where(self.layout_numpy_array == self.tile_key['BRICK_STAIRDN']['val'])).T
    #     return staircase_locations

    def load_map(self) -> None:
        # start_time = time.time()
        x_offset = TILE_SIZE // 2
        y_offset = TILE_SIZE // 2
        tiles_in_current_loaded_map = set([self.get_tile_by_value(tile) for row in self.layout for tile in row])
        self.impassable_tiles = tuple(tiles_in_current_loaded_map & set(all_impassable_tiles))
        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                self.center_pt = (x * TILE_SIZE) + x_offset, (y * TILE_SIZE) + y_offset
                self.map_floor_tiles(x, y)
                self.map_character_tiles(x, y)
        # print("--- %s seconds ---" % (time.time() - start_time))

    def map_character_tiles(self, x, y) -> None:
        for character, character_dict in self.character_key.items():
            if self.layout[y][x] > 32:  # anything below 32 is a floor tile
                if self.layout[y][x] == character_dict['val']:
                    if self.layout[y][x] == 33:  # 'HERO' hardcoded value
                        self.map_player(character_dict['underlying_tile'])
                    elif character_dict['four_sided']:
                        self.map_four_sided_npc(name=character, direction=character_dict['direction'],
                                                underlying_tile=character_dict['underlying_tile'],
                                                image_path=character_dict['path'], is_roaming=character_dict['roaming'])
                    else:
                        self.map_two_sided_npc(image_path=character_dict['path'], name=character,
                                               underlying_tile=character_dict['underlying_tile'])

    def map_four_sided_npc(self, name, direction, underlying_tile, image_path, is_roaming=False) -> None:
        sheet = get_image(image_path)
        sheet = scale(sheet, (sheet.get_width() * self.scale, sheet.get_height() * self.scale))
        images = parse_animated_spritesheet(sheet, is_roaming=True)
        character_sprites = LayeredDirty()
        if is_roaming:
            character = RoamingCharacter(self.center_pt, direction, images, name)
            character.position = self.get_initial_character_location(character.name)
            self.roaming_characters.append(character)
        else:
            character = AnimatedSprite(self.center_pt, direction, images, name)
        character_sprites.add(character)
        self.add_tile_by_value_and_group(underlying_tile)
        self.characters.append(character)
        self.character_sprites.append(character_sprites)

    def add_tile_by_value_and_group(self, underlying_tile) -> None:
        self.add_tile(tile_value=self.tile_key[underlying_tile]['val'],
                      tile_group=self.tile_key[underlying_tile]['group'])

    def map_two_sided_npc(self, image_path, name, underlying_tile) -> None:
        sprites = LayeredDirty()
        sheet = get_image(image_path)
        sheet = scale(sheet, (sheet.get_width() * SCALE, sheet.get_height() * SCALE))
        images = parse_animated_spritesheet(sheet)
        character = AnimatedSprite(self.center_pt, Direction.DOWN.value, images, name)
        sprites.add(character)
        self.characters.append(character)
        self.character_sprites.append(sprites)
        self.add_tile_by_value_and_group(underlying_tile)

    def map_player(self, underlying_tile) -> None:
        # TODO(ELF): Fix underlying tiles so that they aren't all bricks.
        self.player = Player(center_point=self.center_pt,
                             images=self.hero_images)
        self.player_sprites = LayeredDirty(self.player)
        self.player.direction = self.hero_initial_direction()
        self.add_tile_by_value_and_group(underlying_tile)
        self.characters.append(self.player)
        self.character_sprites.append(self.player_sprites)

    def map_floor_tiles(self, x, y) -> None:
        for tile, tile_dict in self.tile_key.items():
            if self.layout[y][x] < 33:
                if self.layout[y][x] == tile_dict['val']:
                    self.add_tile(tile_value=tile_dict['val'], tile_group=tile_dict['group'])

    def add_tile(self, tile_value, tile_group) -> None:
        if tile_value < 10:
            tile = BaseSprite(self.center_pt, self.map_tiles[tile_value][0])
        elif 21 > tile_value >= 10:
            tile = BaseSprite(self.center_pt, self.map_tiles[tile_value - 11][1])
        elif 33 > tile_value >= 21:
            tile = BaseSprite(self.center_pt, self.map_tiles[tile_value - 22][2])
        else:
            print("Invalid tile.")
            tile = None
        tile_group.add(tile)

    @property
    def hero_underlying_tile(self):
        raise NotImplementedError("Method not implemented.")

    @property
    def hero_initial_direction(self):
        raise NotImplementedError("Method not implemented")


class TantegelThroneRoom(DragonWarriorMap):
    """
    This is the first map in the game, the Tantegel Castle throne room.
    """

    def __init__(self, hero_images):
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
            [ROOF] * 10 + [1, 3, 2, 34, 2, 2, 3, 2, 3, 1] + [ROOF] * 7,  # 9
            [ROOF] * 10 + [1, 3, 3, 33, 4, 4, 3, 3, 3, 1] + [ROOF] * 7,  # 10
            [ROOF] * 10 + [1, 3, 3, 3, 3, 3, 39, 3, 3, 1] + [ROOF] * 7,  # 11
            [ROOF] * 10 + [1, 3, 3, 38, 3, 36, 3, 3, 3, 1] + [ROOF] * 7,  # 12
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
        super().__init__(hero_images, tantegel_throne_room)
        self.staircases = {(14, 18): {'map': TantegelCourtyard(self.hero_images), 'stair_direction': 'down'}}
        self.music_file_path = tantegel_castle_throne_room_music

    def hero_underlying_tile(self):
        return 'BRICK'

    def hero_initial_direction(self):
        return Direction.UP.value


class TantegelCourtyard(DragonWarriorMap):
    """
    This is the courtyard of Tantegel Castle.
    """

    def __init__(self, hero_images):
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
            [1] + [3] * 5 + [1, 13, 14, 13, 14, 14, 13, 14, 13, 1] + [3] * 5 + [1, 13, 1, 44, 1] + [13] * 4,
            [1] + [3] * 5 + [1] + [13] * 8 + [1] + [3] * 5 + [1, 13, 1, 2, 1] + [13] * 4,
            [1] + [3, 3, 1, 3, 3] + [1] * 4 + [3, 3] + [1] * 4 + [3, 3, 1] * 2 + [13, 13, 13, 14, 14] + [13] * 3,
            [1] + [3] * 20 + [1, 13, 14, 14, 14] + [13] * 4,
            [1] + [3] * 5 + [1] * 10 + [3] * 5 + [1] + [13] * 5 + [41] + [13] * 2,
            [1] * 5 + [3, 1, 3, 35] + [3] * 6 + [1, 1, 1, 5] + [1] * 5 + [3, 1, 1, 1] + [13] * 2,
            [1] + [3, 3, 3, 1, 3, 1, 33, 3] + [3] * 4 + [1, 3] + [1] + [3] * 11 + [1] + [13] * 2,
            [1] + [3, 40, 3, 3, 3, 1, 3, 37] + [3] * 6 + [1] + [3] * 11 + [1] + [13] * 2,
            [1] + [3, 3, 3, 1, 3, 1, 1, 1] + [3] * 4 + [1] * 12 + [3, 3, 1] + [13] * 2,
            [1] * 5 + [3, 1, 14, 14] + [3] * 4 + [14, 14, 1] + [3, 3, 1] * 4 + [13] * 2,
            [1] + [3, 3, 3, 1, 3, 1, 14, 14, 3, 3, 40, 3, 14, 14, 1] + [3, 3, 1] * 4 + [13] * 2,
            [1] + [3, 39, 3, 1, 3, 1, 14, 13] + [3] * 4 + [13, 14] + [1] + [3] * 11 + [1] + [13] * 2,
            [1] + [4, 3, 4, 5, 3, 1, 13, 41] + [3] * 4 + [13, 13] + [1] + [3] * 11 + [1] + [13] * 2,
            [1] + [3, 4, 3, 1, 3, 1, 13, 13] + [3] * 4 + [13, 13, 1] + [3, 3, 1] * 4 + [13] * 2,
            [1] + [4, 3, 4, 1, 3, 1, 13] + [3] * 6 + [13, 1] + [3, 3, 1] * 4 + [13] * 2,
            [1] * 5 + [3, 1, 13, 3] + [22] * 4 + [3, 13] + [1] * 10 + [3, 1, 1] + [13] * 2,
            [1] + [3] * 8 + [22, 8, 8, 22] + [3] * 6 + [3, 3, 1] + [3] * 5 + [1] + [13] * 2,
            [1] + [3] * 8 + [22, 8, 8, 22] + [3] * 6 + [3, 3, 1] + [8] * 5 + [1] + [13] * 2,
            [1] + [1, 1, 3, 3, 1, 1, 1, 3, 22, 22, 22, 22, 3, 1, 1] + [3] * 5 + [1] + [8] * 5 + [1] + [13] * 2,
            [1] + [3] * 5 + [3, 1] + [3] * 6 + [1, 38] + [3] * 5 + [1] + [3] * 5 + [1] + [13] * 2,
            [1] + [3] * 5 + [3, 1, 1] + [3] * 4 + [1] * 6 + [3, 3, 1, 43] + [3] * 4 + [1, 22] + [13],
            [1] + [3, 3, 1] + [3] * 4 + [1] + [3] * 4 + [1] + [3] * 7 + [1] * 6 + [1, 22] + [13],
            [1] + [3] * 5 + [3, 3, 1] + [3] * 4 + [1] + [3] * 6 + [3, 1] + [22] * 7 + [13],
            [1] + [3, 22, 22, 3, 3, 1, 44, 1] + [3] * 4 + [1, 3, 3] + [1] * 6 + [22] * 7 + [13],
            [1] + [22] * 4 + [3, 44, 3, 1] + [3] * 4 + [1] + [3, 3, 1] * 2 + [3, 1] + [22] * 7 + [13],
            [1] + [22] * 4 + [3] + [3, 3, 1, 1] * 2 + [3] * 5 + [2, 42, 1] + [22] * 7 + [13],
            [1] + [22] * 5 + [3, 3, 1, 38, 3, 3, 36, 1] + [3, 3, 1] * 2 + [3, 1] + [22] * 7 + [13],
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
        super().__init__(hero_images, tantegel_courtyard)

        up_staircase = {'map': Overworld(self.hero_images), 'stair_direction': 'up'}
        staircases_keys = [(37, min(n, 26)) for n in range(9, 27, 1)]
        staircases_values = [up_staircase] * len(staircases_keys)
        self.staircases = dict(zip(staircases_keys, staircases_values))
        self.music_file_path = tantegel_castle_courtyard_music

    def hero_underlying_tile(self):
        return 'BRICK_STAIRUP'

    def hero_initial_direction(self):
        return Direction.RIGHT.value


class Overworld(DragonWarriorMap):
    """
    This is Alefgard, the overworld by which the player travels between cities.
    """

    def __init__(self, hero_images):
        overworld = [
            [WATER] * 26,
            [WATER] * 26,
            [WATER] * 26,
            [WATER] * 26,
            [WATER] * 26,
            [WATER] * 26,
            [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 23, 23, 22, 22, 22],
            [24, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 30, 13, 13, 13, 13, 13, 13, 13, 13, 24, 23, 23],
            [13, 24, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 30, 13, 13, 13, 13, 13, 13, 15, 15, 15, 15, 15, 15, 15],
            [13, 13, 13, 24, 22, 22, 22, 22, 22, 22, 22, 29, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15],
            [14, 13, 13, 13, 24, 22, 22, 22, 22, 22, 22, 30, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [14, 14, 14, 13, 13, 24, 23, 22, 22, 23, 30, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [14, 14, 14, 13, 13, 13, 13, 24, 30, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 26, 27, 28, 14, 14, 14, 14],
            [14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 31, 22, 22, 22, 32, 14, 14, 14],
            [14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 25, 22, 30, 15, 15, 15, 15],
            [14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 31, 23, 30, 15, 15, 15, 15, 15],
            [19, 19, 19, 19, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15],
            [19, 19, 19, 19, 19, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15],
            [19, 19, 19, 19, 19, 19, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15],
            [19, 19, 17, 19, 19, 19, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15],
            [19, 19, 19, 19, 19, 19, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [14, 19, 19, 19, 19, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 13, 13, 13],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 13, 13, 13, 13, 13],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
            [14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14],
            [14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14],
            [14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 16, 16, 16, 16, 16],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 16, 16, 16, 16, 16, 16, 16, 16],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 16, 16, 16, 16, 16, 16, 16, 15, 15, 15, 15, 15, 15],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 16, 16, 16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 15],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15],
            [32, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15],
            [13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13],
            [13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
            [32, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 12, 13, 13, 13, 13],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 26, 27, 27, 27],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 33, 13, 13, 13, 26, 27, 22, 22, 22, 22],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 26, 27, 22, 22, 22, 22, 23, 23],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 26, 27, 22, 22, 22, 22, 23, 30, 16, 16],
            [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 26, 27, 22, 22, 22, 22, 23, 30, 16, 16, 16, 16],
            [14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 26, 22, 22, 22, 22, 22, 30, 20, 20, 20, 16, 16, 16],
            [14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 31, 22, 22, 22, 22, 22, 30, 16, 20, 11, 20, 16, 16, 16],
            [14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 25, 22, 22, 22, 30, 16, 16, 20, 20, 20, 19, 19, 16],
            [14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 25, 22, 22, 29, 16, 16, 16, 16, 16, 16, 16, 19, 19],
            [14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 25, 22, 22, 22, 32, 16, 16, 16, 16, 19, 19, 19, 19],
            [14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 26, 22, 22, 22, 29, 16, 16, 16, 19, 19, 19, 19, 19, 16],
            [14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 26, 22, 22, 22, 22, 22, 28, 16, 16, 19, 19, 19, 19, 19, 19],
            [16, 16, 14, 14, 14, 14, 14, 15, 15, 15, 31, 22, 22, 22, 22, 22, 22, 29, 16, 16, 16, 19, 19, 19, 19, 19],
            [16, 16, 16, 16, 14, 14, 14, 14, 15, 15, 15, 24, 22, 22, 22, 22, 22, 22, 28, 16, 16, 19, 19, 19, 19, 19],
            [16, 16, 16, 16, 16, 14, 14, 14, 14, 15, 15, 15, 25, 22, 22, 22, 22, 22, 29, 16, 16, 19, 19, 19, 19, 19],
            [13, 13, 17, 16, 16, 14, 14, 14, 15, 15, 15, 15, 25, 22, 22, 22, 22, 22, 29, 16, 16, 16, 19, 19, 19, 16],
            [13, 16, 16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 25, 22, 22, 22, 22, 22, 22, 28, 16, 16, 19, 19, 16, 16],
            [16, 16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 26, 22, 22, 22, 22, 22, 22, 22, 30, 16, 16, 20, 16, 16, 16],
            [16, 16, 16, 16, 15, 15, 15, 15, 15, 15, 26, 22, 22, 22, 22, 22, 22, 22, 29, 16, 16, 20, 20, 16, 16, 16],
            [16, 16, 16, 16, 16, 16, 16, 16, 26, 27, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 16, 16, 20, 20, 16, 16],
            [16, 16, 14, 14, 14, 14, 31, 27, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 16, 16, 20, 20, 16],
            [14, 14, 14, 14, 14, 13, 13, 24, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 29, 16, 16, 20, 20, 20],
            [14, 14, 14, 14, 13, 13, 13, 13, 13, 24, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 22, 28, 16, 16, 20, 20],
            [14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 25, 22, 22, 22, 22, 22, 22, 22, 22, 28, 22, 22, 28, 16, 16, 16],
            [14, 13, 13, 13, 13, 13, 13, 13, 13, 26, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 22, 22, 22, 27, 28, 16],
            [13, 13, 13, 13, 13, 13, 13, 13, 26, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 22, 22, 22, 22, 22, 27],
            [16, 16, 16, 16, 16, 16, 16, 16, 26, 27, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 22, 22, 20, 22, 22, 22],
            [16, 16, 16, 16, 16, 16, 16, 16, 26, 27, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 22, 22, 20, 20, 22, 22],
            [16, 16, 16, 16, 16, 16, 16, 16, 26, 27, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 22, 22, 20, 20, 22, 22],
            [16, 16, 16, 16, 16, 16, 16, 16, 26, 27, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 22, 22, 20, 20, 22, 22],
            [16, 16, 16, 16, 16, 16, 16, 16, 26, 27, 22, 22, 22, 22, 22, 22, 22, 22, 22, 28, 22, 22, 20, 20, 22, 22],
        ]
        super().__init__(hero_images, overworld)
        self.music_file_path = overworld_music
        self.staircases = {}

    def hero_underlying_tile(self):
        return 'CASTLE'

    def hero_initial_direction(self):
        return Direction.DOWN.value


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


def get_next_coordinates(character_column, character_row, direction):
    if direction == Direction.UP.value:
        return character_row - 1, character_column
    elif direction == Direction.DOWN.value:
        return character_row + 1, character_column
    elif direction == Direction.LEFT.value:
        return character_row, character_column - 1
    elif direction == Direction.RIGHT.value:
        return character_row, character_column + 1


def get_character_position(character):
    character.column, character.row = character.rect.x // TILE_SIZE, character.rect.y // TILE_SIZE
