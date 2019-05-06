from pygame.sprite import Group, RenderUpdates

from src.animated_sprite import AnimatedSprite
from src.base_sprite import BaseSprite
from src.common import TILE_SIZE
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

tantagel_throne_room = [
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
    [00, 00, 00, 00, 00, 00, 00, 0o1, 0o3, 0o3, 0o3, 0o3, 0o3, 0o3, 0o3, 0o3, 0o1, 00, 00, 00, 00, 00, 00, 00],
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

tantagel_courtyard = [

]


# Working on class refactoring of maps
class TantagelThroneRoom(object):
    """
    This is the first map in the game.
    """

    def __init__(self, player, map_tiles, hero_images=None,
                 king_lorik_images=None, left_guard_images=None, right_guard_images=None, roaming_guard_images=None):
        if king_lorik_images is None:
            king_lorik_images = []
        if hero_images is None:
            hero_images = []
        if left_guard_images is None:
            left_guard_images = []
        if right_guard_images is None:
            right_guard_images = []
        if roaming_guard_images is None:
            roaming_guard_images = []
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
        self.king_lorik_images = king_lorik_images
        self.left_guard_images = left_guard_images
        self.right_guard_images = right_guard_images
        self.roaming_guard_images = roaming_guard_images
        self.layout = tantagel_throne_room
        self.width = len(self.layout[0] * TILE_SIZE)
        self.height = len(self.layout * TILE_SIZE)

    def load_map(self):

        x_offset = TILE_SIZE / 2
        y_offset = TILE_SIZE / 2

        self.king_lorik_sprites = RenderUpdates()
        self.left_guard_sprites = RenderUpdates()
        self.right_guard_sprites = RenderUpdates()
        self.roaming_guard_sprites = RenderUpdates()

        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                center_pt = [(x * TILE_SIZE) + x_offset,
                             (y * TILE_SIZE) + y_offset]
                if self.layout[y][x] == ROOF:
                    roof = BaseSprite(center_pt, self.map_tiles[ROOF][0])
                    self.roof_group.add(roof)
                elif self.layout[y][x] == WALL:
                    wall = BaseSprite(center_pt, self.map_tiles[WALL][0])
                    self.wall_group.add(wall)
                elif self.layout[y][x] == WOOD:
                    wood = BaseSprite(center_pt, self.map_tiles[WOOD][0])
                    self.wood_group.add(wood)
                elif self.layout[y][x] == BRICK:
                    brick = BaseSprite(center_pt, self.map_tiles[BRICK][0])
                    self.brick_group.add(brick)
                elif self.layout[y][x] == CHEST:
                    chest = BaseSprite(center_pt, self.map_tiles[CHEST][0])
                    self.chest_group.add(chest)
                elif self.layout[y][x] == DOOR:
                    door = BaseSprite(center_pt, self.map_tiles[DOOR][0])
                    self.door_group.add(door)
                elif self.layout[y][x] == BRICK_STAIRDN:
                    brick_stairdn = BaseSprite(center_pt, self.map_tiles[
                        BRICK_STAIRDN][0])
                    self.brick_stairdn_group.add(brick_stairdn)
                elif self.layout[y][x] == HERO:
                    self.player = Player(center_pt, 2,
                                         self.hero_images[0],
                                         self.hero_images[1],
                                         self.hero_images[2],
                                         self.hero_images[3])
                    brick = BaseSprite(center_pt, self.map_tiles[BRICK][0])
                    self.brick_group.add(brick)
                elif self.layout[y][x] == KING_LORIK:
                    self.king_lorik = AnimatedSprite(center_pt, 0,
                                                     self.king_lorik_images[0])
                    self.king_lorik_sprites.add(self.king_lorik)
                    brick = BaseSprite(center_pt, self.map_tiles[BRICK][0])
                    self.brick_group.add(brick)
                elif self.layout[y][x] == LEFT_GUARD:
                    self.left_guard = AnimatedSprite(center_pt, 0,
                                                     self.left_guard_images[0])
                    self.left_guard_sprites.add(self.left_guard)
                    brick = BaseSprite(center_pt, self.map_tiles[BRICK][0])
                    self.brick_group.add(brick)
                elif self.layout[y][x] == RIGHT_GUARD:
                    self.right_guard = AnimatedSprite(center_pt, 0,
                                                      self.right_guard_images[0])
                    self.right_guard_sprites.add(self.right_guard)
                    brick = BaseSprite(center_pt, self.map_tiles[BRICK][0])
                    self.brick_group.add(brick)

        self.player_sprites = RenderUpdates(self.player)

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

    def animate(self):
        self.player.animate()
        self.king_lorik.animate()
        self.left_guard.animate()
        self.right_guard.animate()

    def draw_sprites(self, surface):
        self.player_sprites.draw(surface)
        self.king_lorik_sprites.draw(surface)
        self.left_guard_sprites.draw(surface)
        self.right_guard_sprites.draw(surface)
