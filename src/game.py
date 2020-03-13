import random
import sys

import pygame
from pygame import init, Surface, QUIT
from pygame.display import set_mode, set_caption, flip
from pygame.image import load_extended
from pygame.time import Clock
from pygame.time import get_ticks
from pygame.transform import scale

import src.common
import src.maps
import src.player
from src.common import Direction
from src.config import MAP_TILES_PATH, UNARMED_HERO_PATH, KING_LORIK_PATH, LEFT_GUARD_PATH, RIGHT_GUARD_PATH, \
    ROAMING_GUARD_PATH, NES_RES, SCALE, WIN_WIDTH, WIN_HEIGHT, TILE_SIZE


class Game(object):
    FPS = 60
    GAME_TITLE = "Dragon Warrior"
    WIN_WIDTH = NES_RES[0] * SCALE
    WIN_HEIGHT = NES_RES[1] * SCALE

    COLOR_KEY = (0, 128, 128)
    ORIGIN = (0, 0)
    BLACK = (0, 0, 0)
    BACK_FILL_COLOR = BLACK
    MOVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE_EVENT, 100)

    def __init__(self):

        # Initialize pygame
        init()

        # Create the game window.
        self.screen = set_mode((WIN_WIDTH, WIN_HEIGHT))
        set_caption(self.GAME_TITLE)
        self.clock = Clock()
        self.last_roaming_character_clock_check = get_ticks()
        self.roaming_character_go_cooldown = 3000
        self.sprite_movement_wait_period = 10
        if src.maps.current_map is None:
            src.maps.current_map = src.maps.TantegelThroneRoom
            self.player = None
        self.map_tiles = []

        self.bigmap_width = None
        self.bigmap_height = None
        self.bigmap = None

        self.current_map_width = None
        self.current_map_height = None

        self.background = None
        self.current_map = None
        self.king_lorik_images = None

        self.left_guard_images = None

        self.right_guard_images = None

        self.roaming_guard_images = None
        self.unarmed_hero_images = None
        self.load_images()

        self.map_tilesheet = None

    def main(self):
        self.load_current_map()

        # Move to map class
        # self.init_groups()
        # self.current_map = tantegel_throne_room
        # self.load_map()

        # Make the big scrollable map
        self.make_bigmap()

        # self.current_map.draw_map(self.bigmap)
        for sprites in self.current_map.character_sprites:
            sprites.draw(self.bigmap)

        self.background = Surface(self.screen.get_size()).convert()

        self.current_map.roaming_guard.down_images = self.roaming_guard_images[Direction.DOWN.value]
        self.current_map.roaming_guard.left_images = self.roaming_guard_images[Direction.LEFT.value]
        self.current_map.roaming_guard.up_images = self.roaming_guard_images[Direction.UP.value]
        self.current_map.roaming_guard.right_images = self.roaming_guard_images[Direction.RIGHT.value]

        camera_pos = self.ORIGIN

        while True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            camera_pos = self.current_map.player.move(camera_pos=camera_pos, current_map_width=self.current_map_width,
                                                      current_map_height=self.current_map_height)

            self.current_map.draw_map(self.bigmap)
            self.current_map.clear_sprites(self.screen, self.background)
            self.screen.fill(self.BACK_FILL_COLOR)

            self.background = self.bigmap.subsurface(self.ORIGIN[0], self.ORIGIN[1], self.current_map_width,
                                                     self.current_map_height).convert()
            # TODO: disable moving of roaming characters if a dialog box is open.
            self.move_roaming_character()
            for character in self.current_map.characters:
                character.animate()
            for sprites in self.current_map.character_sprites:
                sprites.draw(self.background)

            self.screen.blit(self.background, camera_pos)

            # self.screen.blit(self.background, self.ORIGIN)
            flip()

    def move_roaming_character(self):
        # TODO: extend roaming characters beyond just the roaming guard.
        for roaming_character in self.current_map.roaming_characters:
            roaming_character_direction = random.randrange(4)
            self.move_roaming_character_direction(roaming_character, roaming_character_direction)
            # roaming character sides collision
            if roaming_character.rect.x < 0:  # Simple Sides Collision
                roaming_character.rect.x = 0  # Reset Player Rect Coord
                # pos_x = camera_pos[0]  # Reset Camera Pos Coord
            elif roaming_character.rect.x > int(WIN_WIDTH - ((WIN_WIDTH // 24) * 1.5)):
                roaming_character.rect.x = int(WIN_WIDTH - ((WIN_WIDTH // 24) * 1.5))
                # pos_x = camera_pos[0]
            if roaming_character.rect.y < 0:
                roaming_character.rect.y = 0
                # pos_y = camera_pos[1]
            elif self.current_map.roaming_guard.rect.y > WIN_HEIGHT - TILE_SIZE:
                self.current_map.roaming_guard.rect.y = WIN_HEIGHT - TILE_SIZE

    def move_roaming_character_direction(self, roaming_character, direction):
        now = get_ticks()
        if now - self.last_roaming_character_clock_check >= self.roaming_character_go_cooldown:
            self.last_roaming_character_clock_check = now
            roaming_character.direction = direction
            if direction == Direction.UP.value:
                roaming_character.rect.y -= TILE_SIZE
            elif direction == Direction.LEFT.value:
                roaming_character.rect.x -= TILE_SIZE
            elif direction == Direction.DOWN.value:
                roaming_character.rect.y += TILE_SIZE
            elif direction == Direction.RIGHT.value:
                roaming_character.rect.x += TILE_SIZE
            else:
                print("Invalid direction.")

    def make_bigmap(self):
        self.bigmap_width = self.current_map.width
        self.bigmap_height = self.current_map.height
        self.bigmap = Surface((self.bigmap_width, self.bigmap_height)).convert()
        self.bigmap.fill(self.BACK_FILL_COLOR)

    def load_current_map(self):
        self.current_map = src.maps.TantegelThroneRoom(self.player, self.map_tiles,
                                                       self.unarmed_hero_images,
                                                       self.king_lorik_images, self.left_guard_images,
                                                       self.right_guard_images,
                                                       self.roaming_guard_images)
        self.current_map_width = len(self.current_map.layout[0]) * TILE_SIZE
        self.current_map_height = len(self.current_map.layout) * TILE_SIZE
        self.current_map.load_map()

    def load_images(self):
        """Load all the images for the game graphics.
        """
        # try:
        # Load the map tile spritesheet
        self.map_tilesheet = load_extended(MAP_TILES_PATH).convert()
        # Load unarmed hero images
        unarmed_hero_sheet = load_extended(UNARMED_HERO_PATH)
        # Load King Lorik images
        king_lorik_sheet = load_extended(KING_LORIK_PATH)
        # Guard images.
        left_guard_sheet = load_extended(LEFT_GUARD_PATH)
        right_guard_sheet = load_extended(RIGHT_GUARD_PATH)
        roaming_guard_sheet = load_extended(ROAMING_GUARD_PATH)

        self.map_tilesheet = scale(self.map_tilesheet,
                                   (self.map_tilesheet.get_width() * SCALE,
                                    self.map_tilesheet.get_height() * SCALE))
        unarmed_hero_sheet = scale(unarmed_hero_sheet,
                                   (unarmed_hero_sheet.get_width() * SCALE, unarmed_hero_sheet.get_height() * SCALE))

        king_lorik_sheet = scale(king_lorik_sheet,
                                 (king_lorik_sheet.get_width() * SCALE, king_lorik_sheet.get_height() * SCALE))

        left_guard_sheet = scale(left_guard_sheet,
                                 (left_guard_sheet.get_width() * SCALE, left_guard_sheet.get_height() * SCALE))

        right_guard_sheet = scale(right_guard_sheet,
                                  (right_guard_sheet.get_width() * SCALE, right_guard_sheet.get_height() * SCALE))

        roaming_guard_sheet = scale(roaming_guard_sheet,
                                    (roaming_guard_sheet.get_width() * SCALE, roaming_guard_sheet.get_height() * SCALE))

        self.parse_map_tiles()

        # Get the images for the initial hero sprites
        self.unarmed_hero_images = self.parse_animated_spritesheet(unarmed_hero_sheet, is_roaming=True)

        # Get images for the King
        self.king_lorik_images = self.parse_animated_spritesheet(king_lorik_sheet)

        self.left_guard_images = self.parse_animated_spritesheet(left_guard_sheet)

        self.right_guard_images = self.parse_animated_spritesheet(right_guard_sheet)

        self.roaming_guard_images = self.parse_animated_spritesheet(roaming_guard_sheet, is_roaming=True)

    def parse_map_tiles(self):

        width, height = self.map_tilesheet.get_size()

        for x in range(0, width // TILE_SIZE):
            row = []
            self.map_tiles.append(row)

            for y in range(0, height // TILE_SIZE):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                row.append(self.map_tilesheet.subsurface(rect))

    def parse_animated_spritesheet(self, sheet, is_roaming=False):
        """
        Parses spritesheets and creates image lists. If is_roaming is True
        the sprite will have four lists of images, one for each direction. If
        is_roaming is False then there will be one list of 2 images.
        """
        sheet.set_colorkey(self.COLOR_KEY)
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


def run():
    game = Game()
    game.main()


if __name__ == "__main__":
    run()
