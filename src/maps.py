import pygame
from pygame.sprite import Group, RenderUpdates

from src.animated_sprite import AnimatedSprite
from src.base_sprite import BaseSprite
from src.common import Direction
from src.config import TILE_SIZE, TANTEGEL_CASTLE_THRONE_ROOM_MUSIC_PATH
from src.player import Player

# Tile Key:
# Index values for the map tiles corresponding to location on tilesheet.

tile_key = {
    'ROOF': 0,
    'WALL': 1,
    'WOOD': 2,
    'BRICK': 3,
    'CHEST': 4,
    'DOOR': 5,
    'BRICK_STAIRDN': 6,
    'BRICK_STAIRUP': 7,
    'BARRIER': 8,
    'WEAPON_SIGN': 9,
    'INN_SIGN': 10,
    'CASTLE': 11,
    'TOWN': 12,
    'GRASS': 13,
    'TREES': 14,
    'HILLS': 15,
    'MOUNTAINS': 16,
    'CAVE': 17,
    'GRASS_STAIRDN': 18,
    'SAND': 19,
    'MARSH': 20,
    'BRIDGE': 21,
    'WATER': 22,
    'BOTTOM_COAST': 23,
    'BOTTOM_LEFT_COAST': 24,
    'LEFT_COAST': 25,
    'TOP_LEFT_COAST': 26,
    'TOP_COAST': 27,
    'TOP_RIGHT_COAST': 28,
    'RIGHT_COAST': 29,
    'BOTTOM_RIGHT_COAST': 30,
    'BOTTOM_TOP_LEFT_COAST': 31,
    'BOTTOM_TOP_COAST': 32,
    'BOTTOM_TOP_RIGHT_COAST': 33,
    'HERO': 34,
    'KING_LORIK': 35,
    'LEFT_FACE_GUARD': 36,
    'RIGHT_FACE_GUARD': 37,
    'ROAMING_GUARD': 38
}

impassable_tiles = (
    'ROOF', 'WALL', 'WOOD', 'DOOR', 'BARRIER', 'WEAPON_SIGN', 'INN_SIGN', 'MOUNTAINS', 'WATER', 'BOTTOM_COAST',
    'BOTTOM_LEFT_COAST', 'LEFT_COAST', 'TOP_LEFT_COAST', 'TOP_COAST', 'TOP_RIGHT_COAST', 'RIGHT_COAST',
    'BOTTOM_RIGHT_COAST', 'BOTTOM_TOP_LEFT_COAST', 'BOTTOM_TOP_COAST', 'BOTTOM_TOP_RIGHT_COAST', 'KING_LORIK',
    'LEFT_FACE_GUARD', 'RIGHT_FACE_GUARD')

tile_key_keys = list(tile_key.keys())
tile_key_values = list(tile_key.values())

tantegel_throne_room = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 4, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 2, 2, 2, 2, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 35, 2, 2, 3, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 34, 4, 4, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 38, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 37, 3, 36, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 6, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

tantegel_courtyard = [

]

current_map = None


# Working on class refactoring of maps


class DragonWarriorMap(object):
    def __init__(self):
        self.center_pt = None
        self.player = None


class TantegelThroneRoom(DragonWarriorMap):
    """
    This is the first map in the game.
    """

    def __init__(self, map_tiles, hero_images, king_lorik_images, left_face_guard_images, right_face_guard_images,
                 roaming_guard_images):

        super().__init__()
        self.current_map = TantegelThroneRoom
        self.roaming_guard_sprites = RenderUpdates()
        self.right_face_guard_sprites = RenderUpdates()
        self.left_face_guard_sprites = RenderUpdates()
        self.king_lorik_sprites = RenderUpdates()
        self.brick_stairdn_group = Group()
        self.door_group = Group()
        self.chest_group = Group()
        self.brick_group = Group()
        self.wood_group = Group()
        self.wall_group = Group()
        self.roof_group = Group()

        self.map_tiles = map_tiles
        self.hero_images = hero_images
        self.player_sprites = None
        self.king_lorik = None
        self.left_face_guard = None
        self.right_face_guard = None
        self.roaming_guard = None
        self.king_lorik_images = king_lorik_images
        self.left_face_guard_images = left_face_guard_images
        self.right_face_guard_images = right_face_guard_images
        self.roaming_guard_images = roaming_guard_images
        self.roaming_characters = []

        self.characters = []
        self.character_sprites = []

        self.layout = tantegel_throne_room
        self.width = len(self.layout[0] * TILE_SIZE)
        self.height = len(self.layout * TILE_SIZE)
        self.music_file_path = TANTEGEL_CASTLE_THRONE_ROOM_MUSIC_PATH
        pygame.mixer.music.load(self.music_file_path)
        pygame.mixer.music.play(-1)

    def load_map(self):
        current_loaded_map = self

        x_offset = TILE_SIZE / 2
        y_offset = TILE_SIZE / 2

        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                self.center_pt = [(x * TILE_SIZE) + x_offset,
                                  (y * TILE_SIZE) + y_offset]
                if self.layout[y][x] == tile_key['ROOF']:
                    self.add_tile(tile_type=tile_key['ROOF'], tile_group=self.roof_group)
                elif self.layout[y][x] == tile_key['WALL']:
                    self.add_tile(tile_type=tile_key['WALL'], tile_group=self.wall_group)
                elif self.layout[y][x] == tile_key['WOOD']:
                    self.add_tile(tile_type=tile_key['WOOD'], tile_group=self.wood_group)
                elif self.layout[y][x] == tile_key['BRICK']:
                    self.add_tile(tile_type=tile_key['BRICK'], tile_group=self.brick_group)
                elif self.layout[y][x] == tile_key['CHEST']:
                    self.add_tile(tile_type=tile_key['CHEST'], tile_group=self.chest_group)
                elif self.layout[y][x] == tile_key['DOOR']:
                    self.add_tile(tile_type=tile_key['DOOR'], tile_group=self.door_group)
                elif self.layout[y][x] == tile_key['BRICK_STAIRDN']:
                    self.add_tile(tile_type=tile_key['BRICK_STAIRDN'], tile_group=self.brick_stairdn_group)
                elif self.layout[y][x] == tile_key['HERO']:
                    # Make player start facing up if in Tantegel Throne Room, else face down.
                    if isinstance(current_loaded_map, TantegelThroneRoom):

                        self.player = Player(center_point=self.center_pt, direction=Direction.UP.value,
                                             down_img=self.hero_images[Direction.DOWN.value],
                                             left_img=self.hero_images[Direction.LEFT.value],
                                             up_img=self.hero_images[Direction.UP.value],
                                             right_img=self.hero_images[Direction.RIGHT.value])
                    else:
                        self.player = Player(center_point=self.center_pt, direction=Direction.DOWN.value,
                                             down_img=self.hero_images[Direction.DOWN.value],
                                             left_img=self.hero_images[Direction.LEFT.value],
                                             up_img=self.hero_images[Direction.UP.value],
                                             right_img=self.hero_images[Direction.RIGHT.value])
                    self.set_underlying_tile(tile_type=tile_key['BRICK'], tile_group=self.brick_group)
                elif self.layout[y][x] == tile_key['KING_LORIK']:
                    self.king_lorik = AnimatedSprite(self.center_pt, 0,
                                                     self.king_lorik_images[0])
                    self.king_lorik_sprites.add(self.king_lorik)
                    self.set_underlying_tile(tile_type=tile_key['BRICK'], tile_group=self.brick_group)
                elif self.layout[y][x] == tile_key['LEFT_FACE_GUARD']:
                    self.left_face_guard = AnimatedSprite(self.center_pt, 0,
                                                          self.left_face_guard_images[0])
                    self.left_face_guard_sprites.add(self.left_face_guard)
                    self.set_underlying_tile(tile_type=tile_key['BRICK'], tile_group=self.brick_group)
                elif self.layout[y][x] == tile_key['RIGHT_FACE_GUARD']:
                    self.right_face_guard = AnimatedSprite(self.center_pt, 0,
                                                           self.right_face_guard_images[0])
                    self.right_face_guard_sprites.add(self.right_face_guard)
                    self.set_underlying_tile(tile_type=tile_key['BRICK'], tile_group=self.brick_group)
                elif self.layout[y][x] == tile_key['ROAMING_GUARD']:
                    self.roaming_guard = AnimatedSprite(self.center_pt, 0,
                                                        self.roaming_guard_images[0])
                    self.roaming_guard_sprites.add(self.roaming_guard)
                    self.roaming_characters.append(self.roaming_guard)
                    self.set_underlying_tile(tile_type=tile_key['BRICK'], tile_group=self.brick_group)

        self.player_sprites = RenderUpdates(self.player)
        self.set_underlying_tile(tile_type=tile_key['BRICK'], tile_group=self.brick_group)
        self.characters = [self.player,
                           self.king_lorik,
                           self.left_face_guard,
                           self.right_face_guard,
                           self.roaming_guard]
        self.character_sprites = [self.player_sprites,
                                  self.king_lorik_sprites,
                                  self.left_face_guard_sprites,
                                  self.right_face_guard_sprites,
                                  self.roaming_guard_sprites]

    def set_underlying_tile(self, tile_type, tile_group):
        tile = BaseSprite(self.center_pt, self.map_tiles[tile_type][0])
        tile_group.add(tile)

    def add_tile(self, tile_type, tile_group):
        tile = BaseSprite(self.center_pt, self.map_tiles[tile_type][0])
        tile_group.add(tile)

    def draw_map(self, surface):
        """
        Draw static sprites on the big map.
        """
        self.roof_group.draw(surface)
        self.wall_group.draw(surface)
        self.wood_group.draw(surface)
        self.brick_group.draw(surface)
        self.chest_group.draw(surface)
        self.door_group.draw(surface)
        self.brick_stairdn_group.draw(surface)
