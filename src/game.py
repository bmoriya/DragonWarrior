import sys
from os import pardir
from os.path import join
from pygame.sprite import RenderUpdates

import pygame
from pygame import init, Surface, QUIT, KEYDOWN
from pygame.display import set_mode, set_caption, flip
from pygame.image import load_extended
from pygame.time import Clock
from pygame.transform import scale
from src.animated_sprite import AnimatedSprite
from src.base_sprite import BaseSprite

import src.maps
import src.player
from src.common import TILE_SIZE, SCALE


class Game(object):
    NESRES = (256, 240)
    FPS = 60
    GAME_TITLE = "Dragon Warrior"
    WIN_WIDTH = NESRES[0] * SCALE
    WIN_HEIGHT = NESRES[1] * SCALE
    DATA_DIR = join(pardir, 'data')
    MAP_TILES_PATH = join(DATA_DIR, 'tileset.png')
    UNARMED_HERO_PATH = join(DATA_DIR, 'unarmed_hero.png')
    KING_LORIK_PATH = join(DATA_DIR, 'king_lorik.png')
    RIGHT_GUARD_PATH = join(DATA_DIR, 'right_guard.png')
    LEFT_GUARD_PATH = join(DATA_DIR, 'left_guard.png')
    ROAMING_GUARD_PATH = join(DATA_DIR, 'roaming_guard.png')
    COLORKEY = (0, 128, 128)
    SCROLL_STEP_X = 3
    SCROLL_STEP_Y = 3
    ORIGIN = (0, 0)
    corner_point = [0, 0]
    BLACK = (0, 0, 0)
    BACK_FILL_COLOR = BLACK

    def __init__(self):
        # Initialize pygame
        init()

        # Create the game window.
        self.screen = set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        set_caption(self.GAME_TITLE)
        self.clock = Clock()
        self.player = None
        self.map_tiles = []

        self.load_images()

    def main(self):
        self.load_current_map()

        # Move to map class
        # self.init_groups()
        # self.current_map = tantegel_throne_room
        # self.load_map()

        # Make the big scrollable map
        self.make_bigmap()

        self.current_map.draw_map(self.bigmap)
        self.current_map.draw_sprites(self.bigmap)

        self.background = Surface(self.screen.get_size()).convert()
        self.background.fill(self.BACK_FILL_COLOR)
        x_offset = TILE_SIZE / 2
        y_offset = TILE_SIZE / 2
        for y in range(len(self.current_map.layout)):
            for x in range(len(self.current_map.layout[y])):
                self.center_pt = [(x * TILE_SIZE) + x_offset,
                                  (y * TILE_SIZE) + y_offset]

        while True:
            self.current_map.clear_sprites(self.screen, self.background)

            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                #TODO: disable this if a dialog box is open.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_map.player.direction = AnimatedSprite.LEFT
                    if event.key == pygame.K_RIGHT:
                        self.current_map.player.direction = AnimatedSprite.RIGHT
                    if event.key == pygame.K_UP:
                        self.current_map.player.direction = AnimatedSprite.UP
                    if event.key == pygame.K_DOWN:
                        self.current_map.player.direction = AnimatedSprite.DOWN

            self.background = self.bigmap.subsurface(self.corner_point[0],
                                                     self.corner_point[1],
                                                     self.WIN_WIDTH,
                                                     self.WIN_HEIGHT).convert()
            self.current_map.animate()
            self.current_map.draw_sprites(self.background)

            self.screen.blit(self.background, self.ORIGIN)
            flip()

    def make_bigmap(self):
        self.bigmap_width = self.current_map.width
        self.bigmap_height = self.current_map.height
        self.bigmap = Surface((self.bigmap_width,
                               self.bigmap_height)).convert()
        self.bigmap.fill(self.BACK_FILL_COLOR)

    def load_current_map(self):
        self.current_map = src.maps.TantegelThroneRoom(self.player, self.map_tiles,
                                                       self.unarmed_hero_images,
                                                       self.king_lorik_images, self.left_guard_images,
                                                       self.right_guard_images,
                                                       self.roaming_guard_images)
        self.current_map.load_map()

    def load_images(self):
        """Load all the images for the game graphics.
        """
        # try:
        # Load the map tile spritesheet
        self.map_tilesheet = load_extended(self.MAP_TILES_PATH).convert()
        # Load unarmed hero images
        self.unarmed_hero_sheet = load_extended(self.UNARMED_HERO_PATH)
        # Load King Lorik images
        self.king_lorik_sheet = load_extended(self.KING_LORIK_PATH)
        # Guard images.
        self.left_guard_sheet = load_extended(self.LEFT_GUARD_PATH)
        self.right_guard_sheet = load_extended(self.RIGHT_GUARD_PATH)
        self.roaming_guard_sheet = load_extended(self.ROAMING_GUARD_PATH)

        # except error as e:
        #    print(e)
        #    return

        self.map_tilesheet = scale(self.map_tilesheet,
                                   (self.map_tilesheet.get_width() * SCALE,
                                    self.map_tilesheet.get_height() * SCALE))
        self.unarmed_hero_sheet = scale(self.unarmed_hero_sheet,
                                        (self.unarmed_hero_sheet.get_width() *
                                         SCALE,
                                         self.unarmed_hero_sheet.get_height() *
                                         SCALE))

        self.king_lorik_sheet = scale(self.king_lorik_sheet,
                                      (self.king_lorik_sheet.get_width() * SCALE,
                                       self.king_lorik_sheet.get_height() * SCALE))

        self.left_guard_sheet = scale(self.left_guard_sheet,
                                      (self.left_guard_sheet.get_width() * SCALE,
                                       self.left_guard_sheet.get_height() * SCALE))

        self.right_guard_sheet = scale(self.right_guard_sheet,
                                       (self.right_guard_sheet.get_width() * SCALE,
                                        self.right_guard_sheet.get_height() * SCALE))

        self.roaming_guard_sheet = scale(self.roaming_guard_sheet,
                                         (self.roaming_guard_sheet.get_width() * SCALE,
                                          self.roaming_guard_sheet.get_height() * SCALE))

        self.parse_map_tiles()

        # Get the images for the initial hero sprites
        self.unarmed_hero_images = self.parse_animated_spritesheet(
            self.unarmed_hero_sheet, is_roaming=True)

        # Get images for the King
        self.king_lorik_images = self.parse_animated_spritesheet(
            self.king_lorik_sheet, is_roaming=False)

        self.left_guard_images = self.parse_animated_spritesheet(
            self.left_guard_sheet, is_roaming=False)

        self.right_guard_images = self.parse_animated_spritesheet(
            self.right_guard_sheet, is_roaming=False)

        self.roaming_guard_images = self.parse_animated_spritesheet(
            self.roaming_guard_sheet, is_roaming=True)

    def parse_map_tiles(self):

        width, height = self.map_tilesheet.get_size()

        for x in range(0, width // TILE_SIZE):
            row = []
            self.map_tiles.append(row)

            for y in range(0, height // TILE_SIZE):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                row.append(self.map_tilesheet.subsurface(rect))

    def parse_animated_spritesheet(self, sheet, is_roaming=True):
        """
        Parses spritesheets and creates image lists. If is_roaming is True
        the sprite will have four lists of images, one for each direction. If
        is_roaming is False then there will be one list of 2 images.
        """
        sheet.set_colorkey(self.COLORKEY)
        sheet.convert_alpha()
        width, height = sheet.get_size()

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

    def run(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.main()
