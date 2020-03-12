from os.path import join, pardir

import pygame
from pygame.sprite import Group, RenderUpdates

from src.animated_sprite import AnimatedSprite
from src.base_sprite import BaseSprite
from src.common import TILE_SIZE, Direction
from src.player import Player

# Tile Key:
# Index values for the map tiles corresponding to location on tilesheet.
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
HERO = 34
KING_LORIK = 35
LEFT_GUARD = 36
RIGHT_GUARD = 37
ROAMING_GUARD = 38

tantegel_throne_room = [
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o1, 0o1, 0o1, 0o1, 0o1, 0o1, 0o1, 0o1, 0o1, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o3, 0o3, 0o3, 0o3, 0o3, 0o3, 0o4, 0o3, 0o1, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o3, 0o2, 0o2, 0o2, 0o2, 0o2, 0o2, 0o3, 0o1, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o3, 0o2, 35, 0o2, 0o2, 0o3, 0o2, 0o3, 0o1, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o3, 0o3, 34, 0o4, 0o4, 0o3, 0o3, 0o3, 0o1, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o3, 0o3, 0o3, 0o3, 0o3, 38, 0o3, 0o3, 0o1, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o3, 0o3, 37, 0o3, 36, 0o3, 0o3, 0o3, 0o1, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o1, 0o1, 0o1, 0o5, 0o1, 0o1, 0o1, 0o1, 0o1, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o3, 0o3, 0o3, 0o3, 0o3, 0o3, 0o3, 0o6, 0o1, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o1, 0o1, 0o1, 0o1, 0o1, 0o1, 0o1, 0o1, 0o1, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
]

tantegel_courtyard = [

]

current_map = None


# Working on class refactoring of maps


class TantegelThroneRoom(object):
    """
    This is the first map in the game.
    """

    def __init__(self, player, map_tiles, hero_images, king_lorik_images, left_guard_images, right_guard_images,
                 roaming_guard_images):
        self.center_pt = None
        self.current_map = TantegelThroneRoom
        self.roaming_guard_sprites = RenderUpdates()
        self.right_guard_sprites = RenderUpdates()
        self.left_guard_sprites = RenderUpdates()
        self.king_lorik_sprites = RenderUpdates()
        self.brick_stairdn_group = Group()
        self.door_group = Group()
        self.chest_group = Group()
        self.brick_group = Group()
        self.wood_group = Group()
        self.wall_group = Group()
        self.roof_group = Group()
        self.player = player
        self.map_tiles = map_tiles
        self.hero_images = hero_images
        self.king_lorik = None
        self.left_guard = None
        self.right_guard = None
        self.roaming_guard = None
        self.king_lorik_images = king_lorik_images
        self.left_guard_images = left_guard_images
        self.right_guard_images = right_guard_images
        self.roaming_guard_images = roaming_guard_images
        self.roaming_characters = []
        self.player_sprites = None
        self.characters = []
        self.character_sprites = []

        self.layout = tantegel_throne_room
        self.width = len(self.layout[0] * TILE_SIZE)
        self.height = len(self.layout * TILE_SIZE)
        data_dir = join(pardir, 'data')
        pygame.mixer.music.load(join(data_dir, '02_Dragon_Quest_1_-_Tantegel_Castle_(22khz_mono).ogg'))
        pygame.mixer.music.play(-1)

    def load_map(self):
        current_loaded_map = self

        x_offset = TILE_SIZE / 2
        y_offset = TILE_SIZE / 2

        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                self.center_pt = [(x * TILE_SIZE) + x_offset,
                                  (y * TILE_SIZE) + y_offset]
                if self.layout[y][x] == ROOF:
                    self.add_tile(tile_type=ROOF, tile_group=self.roof_group)
                elif self.layout[y][x] == WALL:
                    self.add_tile(tile_type=WALL, tile_group=self.wall_group)
                elif self.layout[y][x] == WOOD:
                    self.add_tile(tile_type=WOOD, tile_group=self.wood_group)
                elif self.layout[y][x] == BRICK:
                    self.add_tile(tile_type=BRICK, tile_group=self.brick_group)
                elif self.layout[y][x] == CHEST:
                    self.add_tile(tile_type=CHEST, tile_group=self.chest_group)
                elif self.layout[y][x] == DOOR:
                    self.add_tile(tile_type=DOOR, tile_group=self.door_group)
                elif self.layout[y][x] == BRICK_STAIRDN:
                    self.add_tile(tile_type=BRICK_STAIRDN, tile_group=self.brick_stairdn_group)
                elif self.layout[y][x] == HERO:
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
                    self.set_underlying_tile(tile_type=BRICK, tile_group=self.brick_group)
                elif self.layout[y][x] == KING_LORIK:
                    self.king_lorik = AnimatedSprite(self.center_pt, 0,
                                                     self.king_lorik_images[0])
                    self.king_lorik_sprites.add(self.king_lorik)
                    self.set_underlying_tile(tile_type=BRICK, tile_group=self.brick_group)
                elif self.layout[y][x] == LEFT_GUARD:
                    self.left_guard = AnimatedSprite(self.center_pt, 0,
                                                     self.left_guard_images[0])
                    self.left_guard_sprites.add(self.left_guard)
                    self.set_underlying_tile(tile_type=BRICK, tile_group=self.brick_group)
                elif self.layout[y][x] == RIGHT_GUARD:
                    self.right_guard = AnimatedSprite(self.center_pt, 0,
                                                      self.right_guard_images[0])
                    self.right_guard_sprites.add(self.right_guard)
                    self.set_underlying_tile(tile_type=BRICK, tile_group=self.brick_group)
                elif self.layout[y][x] == ROAMING_GUARD:
                    self.roaming_guard = AnimatedSprite(self.center_pt, 0,
                                                        self.roaming_guard_images[0])
                    self.roaming_guard_sprites.add(self.roaming_guard)
                    self.roaming_characters.append(self.roaming_guard)
                    self.set_underlying_tile(tile_type=BRICK, tile_group=self.brick_group)

        self.player_sprites = RenderUpdates(self.player)
        self.set_underlying_tile(tile_type=BRICK, tile_group=self.brick_group)
        self.characters = [self.player,
                           self.king_lorik,
                           self.left_guard,
                           self.right_guard,
                           self.roaming_guard]
        self.character_sprites = [self.player_sprites,
                                  self.king_lorik_sprites,
                                  self.left_guard_sprites,
                                  self.right_guard_sprites,
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

    def clear_sprites(self, screen, surface):
        self.player_sprites.clear(screen, surface)
        self.king_lorik_sprites.clear(screen, surface)
        self.left_guard_sprites.clear(screen, surface)
        self.right_guard_sprites.clear(screen, surface)
        self.roaming_guard_sprites.clear(screen, surface)
