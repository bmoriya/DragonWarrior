from os import pardir
from os.path import join
from pygame import init, error, Surface, QUIT, KEYDOWN
from pygame.display import set_mode, set_caption, flip
from pygame.event import get
from pygame.image import load
from pygame.sprite import Group, RenderUpdates
from pygame.transform import scale
from pygame.time import Clock

from src.common import TILE_SIZE, SCALE
from src.player import Player
from src.maps import TantagelThroneRoom


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
    cornerpoint = [0, 0]
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
        self.current_map = TantagelThroneRoom(self.player, self.map_tiles,
                                              self.unarmed_hero_images,
                                              self.king_lorik_images)
        self.current_map.init_groups()
        self.current_map.load_map()

        # Move to map class
        # self.init_groups()
        # self.current_map = tantagel_throne_room
        # self.load_map()

        # Make the big scrollable map
        self.bigmap_width = self.current_map.width
        self.bigmap_height = self.current_map.height
        self.bigmap = Surface((self.bigmap_width,
                               self.bigmap_height)).convert()
        self.bigmap.fill(self.BACK_FILL_COLOR)

        self.current_map.draw_map(self.bigmap)
        self.current_map.draw_sprites(self.bigmap)

        self.background = Surface(self.screen.get_size()).convert()
        self.background.fill(self.BACK_FILL_COLOR)

        while True:
            self.current_map.clear_sprites(self.screen, self.background)

            self.clock.tick(self.FPS)
            for event in get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    pass

            self.background = self.bigmap.subsurface(self.cornerpoint[0],
                                                     self.cornerpoint[1],
                                                     self.WIN_WIDTH,
                                                     self.WIN_HEIGHT).convert()
            self.current_map.animate()
            self.current_map.draw_sprites(self.background)

            self.screen.blit(self.background, self.ORIGIN)
            flip()

    def load_images(self):
        '''
        Load all the images for the game graphics.
        '''
        try:
            # Load the map tile spritesheet
            self.map_tilesheet = load(self.MAP_TILES_PATH).convert()

            # Load unarmed hero images
            self.unarmed_herosheet = load(self.UNARMED_HERO_PATH)

            # Load King Lorik images
            self.king_lorik_sheet = load(self.KING_LORIK_PATH)

            # Guard images.
            right_guard_sheet = load(self.RIGHT_GUARD_PATH)
            left_guard_sheet = load(self.LEFT_GUARD_PATH)
            roaming_guard_sheet = load(self.ROAMING_GUARD_PATH)

        except error as e:
            print(e)
            return

        self.map_tilesheet = scale(self.map_tilesheet,
                                   (self.map_tilesheet.get_width() * SCALE,
                                    self.map_tilesheet.get_height() * SCALE))
        self.unarmed_herosheet = scale(self.unarmed_herosheet,
                                       (self.unarmed_herosheet.get_width() *
                                        SCALE,
                                        self.unarmed_herosheet.get_height() *
                                        SCALE))

        self.king_lorik_sheet = scale(self.king_lorik_sheet,
                                      (self.king_lorik_sheet.get_width() * SCALE,
                                       self.king_lorik_sheet.get_height() * SCALE))
        self.parse_map_tiles()

        # Get the images for the initial hero sprites
        self.unarmed_hero_images = self.parse_animated_spritesheet(
            self.unarmed_herosheet, is_roaming=True)

        # Get images for the King
        self.king_lorik_images = self.parse_animated_spritesheet(
            self.king_lorik_sheet, is_roaming=False)

    def parse_map_tiles(self):

        width, height = self.map_tilesheet.get_size()

        for x in range(0, width // TILE_SIZE):
            row = []
            self.map_tiles.append(row)

            for y in range(0, height // TILE_SIZE):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                row.append(self.map_tilesheet.subsurface(rect))

    def parse_animated_spritesheet(self, sheet, is_roaming=True):
        '''
        Parses spritesheets and creates image lists. If is_roaming is True 
        the sprite will have four lists of images, one for each direction. If
        is_roaming is False then there will be one list of 2 images.
        '''
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

            if is_roaming == True:
                rect = ((i + 2) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
                facing_left.append(sheet.subsurface(rect))

                rect = ((i + 4) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
                facing_up.append(sheet.subsurface(rect))

                rect = ((i + 6) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
                facing_right.append(sheet.subsurface(rect))

        return facing_down, facing_left, facing_up, facing_right


if __name__ == "__main__":
    game = Game()
    game.main()
