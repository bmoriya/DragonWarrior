import random
import sys

import numpy as np
import pygame
from pygame import init, Surface, QUIT, USEREVENT, time, quit
from pygame.display import set_mode, set_caption, flip
from pygame.event import get
from pygame.time import Clock
from pygame.time import get_ticks
from pygame.transform import scale

from src import maps
from src.common import Direction, play_sound, bump_sfx, MAP_TILES_PATH, UNARMED_HERO_PATH, RIGHT_FACE_GUARD_PATH, \
    LEFT_FACE_GUARD_PATH, ROAMING_GUARD_PATH, get_image, KING_LORIK_PATH
from src.config import NES_RES, SCALE, WIN_WIDTH, WIN_HEIGHT, TILE_SIZE
from src.maps import TantegelThroneRoom, parse_animated_spritesheet, TantegelCourtyard


def get_initial_camera_position(initial_hero_location):
    return int(np.negative(initial_hero_location.take(0) * TILE_SIZE / 2)), int(np.negative(
        initial_hero_location.take(1) * TILE_SIZE / 4.333333333333333))


class Game(object):
    FPS = 60
    GAME_TITLE = "Dragon Warrior"
    WIN_WIDTH = NES_RES[0] * SCALE
    WIN_HEIGHT = NES_RES[1] * SCALE

    ORIGIN = (0, 0)
    BLACK = (0, 0, 0)
    BACK_FILL_COLOR = BLACK
    MOVE_EVENT = USEREVENT + 1
    time.set_timer(MOVE_EVENT, 100)

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
        if maps.current_map is None:
            maps.current_map = maps.TantegelThroneRoom
        self.map_tiles = []
        self.bigmap_width = None
        self.bigmap_height = None
        self.bigmap = None
        self.current_map_width = None
        self.current_map_height = None
        self.background = None
        self.current_map = None

        self.curr_pos_x, self.curr_pos_y = None, None

        self.left_face_guard_images = None
        self.right_face_guard_images = None
        self.roaming_guard_images = None
        self.unarmed_hero_images = None
        self.load_images()
        self.map_tilesheet = None
        self.hero_layout_x_pos = None
        self.hero_layout_y_pos = None
        self.camera_pos = None

    def main(self):
        self.load_current_map()
        # Make the big scrollable map
        self.make_bigmap()
        self.background = Surface(self.screen.get_size()).convert()
        self.get_roaming_guard_images()
        initial_hero_location = self.current_map.get_initial_character_location('HERO')
        self.hero_layout_x_pos = initial_hero_location.take(0)
        self.hero_layout_y_pos = initial_hero_location.take(1)

        # TODO: Fix the initial camera_pos calculation.
        self.camera_pos = get_initial_camera_position(initial_hero_location)
        while True:
            self.clock.tick(self.FPS)
            self.events()
            self.draw()
            self.update()

    def draw(self):
        self.current_map.draw_map(self.bigmap)
        for sprites in self.current_map.character_sprites:
            sprites.clear(self.screen, self.background)
        self.screen.fill(self.BACK_FILL_COLOR)
        self.background = self.get_background()
        for character in self.current_map.characters:
            character.animate()
        for sprites in self.current_map.character_sprites:
            sprites.draw(self.background)

    def update(self):
        self.screen.blit(self.background, self.camera_pos)
        flip()

    def get_background(self):
        return self.bigmap.subsurface(self.ORIGIN[0], self.ORIGIN[1], self.current_map.width,
                                      self.current_map_height).convert()

    def move_roaming_characters(self):
        # TODO: Disable moving of roaming characters if a dialog box is open.
        # TODO: Extend roaming characters beyond just the roaming guard.
        for roaming_character in self.current_map.roaming_characters:
            roaming_character_x_pos = roaming_character.rect.y // TILE_SIZE
            roaming_character_y_pos = roaming_character.rect.x // TILE_SIZE
            now = get_ticks()
            if now - self.last_roaming_character_clock_check >= self.roaming_character_go_cooldown:
                self.last_roaming_character_clock_check = now
                roaming_character.direction = random.randrange(4)
                self.move_roaming_character(roaming_character.position.take(0), roaming_character.position.take(1),
                                            roaming_character, roaming_character_x_pos,
                                            roaming_character_y_pos)
            self.handle_roaming_character_map_edge_side_collision(roaming_character)

    def events(self):
        for event in get():
            if event.type == QUIT:
                quit()
                sys.exit()
        # TODO: Smooth out movement even more.
        key = pygame.key.get_pressed()
        self.hero_layout_x_pos = self.current_map.player.rect.y // TILE_SIZE
        self.hero_layout_y_pos = self.current_map.player.rect.x // TILE_SIZE
        self.move_roaming_characters()
        self.move_player(key)
        # # TODO: implement actual function of B, A, Start, Select buttons.
        if key[pygame.K_z]:
            # B button
            print("You pressed the z key.")
        if key[pygame.K_y]:
            # A button
            print("You pressed the y key.")
        if key[pygame.K_SPACE]:
            # Start button
            print("You pressed the space bar.")
        if key[pygame.K_ESCAPE]:
            # Select button
            print("You pressed the escape key.")

        # For debugging purposes, this prints out the current tile that the hero is standing on.
        # print(self.get_tile_by_coordinates(self.current_map.player.rect.y // TILE_SIZE,
        #                                    self.current_map.player.rect.x // TILE_SIZE))
        # THESE ARE THE VALUES WE ARE AIMING FOR FOR INITIAL TANTEGEL THRONE ROOM
        # camera_pos = -160, -96

    def get_tile_by_coordinates(self, y, x):
        return self.current_map.get_tile_by_value(self.current_map.layout[y][x])

    def get_roaming_guard_images(self):
        self.current_map.roaming_guard.down_images = self.roaming_guard_images[Direction.DOWN.value]
        self.current_map.roaming_guard.left_images = self.roaming_guard_images[Direction.LEFT.value]
        self.current_map.roaming_guard.up_images = self.roaming_guard_images[Direction.UP.value]
        self.current_map.roaming_guard.right_images = self.roaming_guard_images[Direction.RIGHT.value]

    def move_player(self, key):
        self.curr_pos_x, self.curr_pos_y = self.camera_pos
        next_pos_x, next_pos_y = self.curr_pos_x, self.curr_pos_y
        if key[pygame.K_DOWN]:
            self.current_map.player.direction = Direction.DOWN.value
            _, next_pos_y = self.move(delta_x=0, delta_y=-1)
        if key[pygame.K_LEFT]:
            self.current_map.player.direction = Direction.LEFT.value
            next_pos_x, _ = self.move(delta_x=-1, delta_y=0)
        if key[pygame.K_UP]:
            self.current_map.player.direction = Direction.UP.value
            _, next_pos_y = self.move(delta_x=0, delta_y=1)
        if key[pygame.K_RIGHT]:
            self.current_map.player.direction = Direction.RIGHT.value
            next_pos_x, _ = self.move(delta_x=1, delta_y=0)
            #  THIS MOVES SMOOTHLY
            # self.current_map.player.rect.x += 1  # increment
            # curr_pos_x -= 1
            # pygame.time.delay(10)
        # Sides collision
        next_pos_x = self.handle_lr_sides_collision(next_pos_x)
        next_pos_y = self.handle_tb_sides_collision(next_pos_y)
        # for reference:
        # self.current_map.height - TILE_SIZE is equal to WIN_HEIGHT - ((WIN_HEIGHT // 23) * 1.5)
        self.camera_pos = next_pos_x, next_pos_y

    def move(self, delta_x, delta_y):
        next_pos_x = self.curr_pos_x
        next_pos_y = self.curr_pos_y
        if not self.did_collide((self.current_map.player.rect.y // TILE_SIZE) + -delta_y,
                                (self.current_map.player.rect.x // TILE_SIZE) + delta_x):
            for x in range(TILE_SIZE):
                self.current_map.player.rect.x += delta_x
                next_pos_x = self.curr_pos_x + TILE_SIZE * -delta_x
                self.current_map.player.rect.y += -delta_y
                next_pos_y = self.curr_pos_y + TILE_SIZE * delta_y
                pygame.time.delay(10)
        return next_pos_x, next_pos_y

    def did_collide(self, delta_x, delta_y):
        if self.current_map.impassable_tiles and self.current_map.get_tile_by_value(
                self.current_map.layout[delta_x][delta_y]) in self.current_map.impassable_tiles:
            # TODO: Slow down the bump sound effect.
            play_sound(bump_sfx)
            return True
        return False

    def handle_tb_sides_collision(self, next_pos_y):
        max_bound = self.current_map.height
        min_bound = 0
        player_pos = self.current_map.player.rect.y
        if player_pos < min_bound:
            self.current_map.player.rect.y = min_bound
            play_sound(bump_sfx)
            next_pos_y = self.curr_pos_y
        elif player_pos > max_bound - TILE_SIZE:
            self.current_map.player.rect.y = max_bound - TILE_SIZE
            play_sound(bump_sfx)
            next_pos_y = self.curr_pos_y
        return next_pos_y

    def handle_lr_sides_collision(self, next_pos_x):
        max_bound = self.current_map.width
        min_bound = 0
        player_pos = self.current_map.player.rect.x
        if player_pos < min_bound:  # Simple Sides Collision
            self.current_map.player.rect.x = min_bound  # Reset Player Rect Coord
            play_sound(bump_sfx)
            next_pos_x = self.curr_pos_x
        elif player_pos > max_bound - TILE_SIZE:
            self.current_map.player.rect.x = max_bound - TILE_SIZE
            play_sound(bump_sfx)
            next_pos_x = self.curr_pos_x
        return next_pos_x

    def move_roaming_character(self, pos_x, pos_y, roaming_character, roaming_character_x_pos, roaming_character_y_pos):
        if roaming_character.direction == Direction.DOWN.value:
            if self.current_map.get_tile_by_value(self.current_map.layout[roaming_character_x_pos + 1][
                                                      roaming_character_y_pos]) not in self.current_map.impassable_tiles:
                roaming_character.rect.y += TILE_SIZE
                pos_y -= 1
        elif roaming_character.direction == Direction.LEFT.value:
            if self.current_map.get_tile_by_value(self.current_map.layout[roaming_character_x_pos][
                                                      roaming_character_y_pos - 1]) not in self.current_map.impassable_tiles:
                roaming_character.rect.x -= TILE_SIZE
                pos_x -= 1
        elif roaming_character.direction == Direction.UP.value:
            if self.current_map.get_tile_by_value(self.current_map.layout[roaming_character_x_pos - 1][
                                                      roaming_character_y_pos]) not in self.current_map.impassable_tiles:
                roaming_character.rect.y -= TILE_SIZE
                pos_y += 1
        elif roaming_character.direction == Direction.RIGHT.value:
            if self.current_map.get_tile_by_value(self.current_map.layout[roaming_character_x_pos][
                                                      roaming_character_y_pos + 1]) not in self.current_map.impassable_tiles:
                roaming_character.rect.x += TILE_SIZE
                pos_x += 1
        else:
            print("Invalid direction.")

    def handle_roaming_character_map_edge_side_collision(self, roaming_character):
        if roaming_character.rect.x < 0:  # Simple Sides Collision
            roaming_character.rect.x = 0  # Reset Player Rect Coord
        elif roaming_character.rect.x > self.current_map.width - TILE_SIZE:
            roaming_character.rect.x = self.current_map.width - TILE_SIZE
        if roaming_character.rect.y < 0:
            roaming_character.rect.y = 0
        elif self.current_map.roaming_guard.rect.y > self.current_map_height - TILE_SIZE:
            self.current_map.roaming_guard.rect.y = self.current_map_height - TILE_SIZE

    def make_bigmap(self):
        self.bigmap_width = self.current_map.width
        self.bigmap_height = self.current_map.height
        self.bigmap = Surface((self.bigmap_width, self.bigmap_height)).convert()
        self.bigmap.fill(self.BACK_FILL_COLOR)

    def load_current_map(self):
        self.current_map = TantegelThroneRoom(self.map_tiles, self.unarmed_hero_images, self.left_face_guard_images,
                                              self.right_face_guard_images, self.roaming_guard_images)
        # self.current_map = TantegelCourtyard
        self.current_map.width = len(self.current_map.layout[0]) * TILE_SIZE
        self.current_map_height = len(self.current_map.layout) * TILE_SIZE
        self.current_map.load_map()

    def load_images(self):
        """Load all the images for the game graphics.
        """
        # Load the map tile spritesheet
        self.map_tilesheet = get_image(MAP_TILES_PATH).convert()
        # Load unarmed hero images
        unarmed_hero_sheet = get_image(UNARMED_HERO_PATH)
        # Load King Lorik images
        king_lorik_sheet = get_image(KING_LORIK_PATH)
        # Guard images.
        left_face_guard_sheet = get_image(LEFT_FACE_GUARD_PATH)
        right_face_guard_sheet = get_image(RIGHT_FACE_GUARD_PATH)
        roaming_guard_sheet = get_image(ROAMING_GUARD_PATH)

        self.map_tilesheet = scale(self.map_tilesheet,
                                   (self.map_tilesheet.get_width() * SCALE,
                                    self.map_tilesheet.get_height() * SCALE))
        unarmed_hero_sheet = scale(unarmed_hero_sheet,
                                   (unarmed_hero_sheet.get_width() * SCALE, unarmed_hero_sheet.get_height() * SCALE))

        king_lorik_sheet = scale(king_lorik_sheet,
                                 (king_lorik_sheet.get_width() * SCALE, king_lorik_sheet.get_height() * SCALE))

        left_face_guard_sheet = scale(left_face_guard_sheet,
                                      (left_face_guard_sheet.get_width() * SCALE,
                                       left_face_guard_sheet.get_height() * SCALE))

        right_face_guard_sheet = scale(right_face_guard_sheet,
                                       (right_face_guard_sheet.get_width() * SCALE,
                                        right_face_guard_sheet.get_height() * SCALE))

        roaming_guard_sheet = scale(roaming_guard_sheet,
                                    (roaming_guard_sheet.get_width() * SCALE, roaming_guard_sheet.get_height() * SCALE))

        self.parse_map_tiles()

        # Get the images for the initial hero sprites
        self.unarmed_hero_images = parse_animated_spritesheet(unarmed_hero_sheet, is_roaming=True)

        # Get images for the King
        self.king_lorik_images = parse_animated_spritesheet(king_lorik_sheet)

        self.left_face_guard_images = parse_animated_spritesheet(left_face_guard_sheet)

        self.right_face_guard_images = parse_animated_spritesheet(right_face_guard_sheet)

        self.roaming_guard_images = parse_animated_spritesheet(roaming_guard_sheet, is_roaming=True)

    def parse_map_tiles(self):

        width, height = self.map_tilesheet.get_size()

        for x in range(0, width // TILE_SIZE):
            row = []
            self.map_tiles.append(row)

            for y in range(0, height // TILE_SIZE):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                row.append(self.map_tilesheet.subsurface(rect))


def run():
    game = Game()
    game.main()


if __name__ == "__main__":
    run()
