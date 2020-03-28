import random
import sys

import pygame
from pygame import init, Surface, USEREVENT, time, quit, FULLSCREEN
from pygame.display import set_mode, set_caption, flip
from pygame.event import get
from pygame.time import Clock
from pygame.time import get_ticks
from pygame.transform import scale

from src import maps
from src.common import Direction, play_sound, bump_sfx, MAP_TILES_PATH, UNARMED_HERO_PATH, RIGHT_FACE_GUARD_PATH, \
    LEFT_FACE_GUARD_PATH, ROAMING_GUARD_PATH, get_image, KING_LORIK_PATH
from src.config import NES_RES, SCALE, WIN_WIDTH, WIN_HEIGHT, TILE_SIZE, FULLSCREEN_ENABLED
from src.maps import TantegelThroneRoom, parse_animated_spritesheet


def get_initial_camera_position(initial_hero_location):
    top_left_x = initial_hero_location[0] * TILE_SIZE
    top_left_y = initial_hero_location[1] * TILE_SIZE
    return top_left_x, top_left_y
    # return WIN_WIDTH // TILE_SIZE, WIN_HEIGHT // TILE_SIZE


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
        if FULLSCREEN_ENABLED:
            self.screen = set_mode((WIN_WIDTH, WIN_HEIGHT), FULLSCREEN)
        else:
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
        self.current_map_height = None
        self.background = None
        self.current_map = None
        self.next_tile = None
        self.next_tile_checked = False

        self.left_face_guard_images = None
        self.right_face_guard_images = None
        self.roaming_guard_images = None
        self.unarmed_hero_images = None
        self.load_images()
        self.map_tilesheet = None
        self.camera_pos = None

        self.hero_layout_row = None
        self.hero_layout_column = None
        self.player_moving = False
        self.speed = 2

    def main(self):
        self.load_current_map()
        # Make the big scrollable map
        self.make_bigmap()
        self.background = Surface(self.screen.get_size()).convert()
        initial_hero_location = self.current_map.get_initial_character_location('HERO')
        self.hero_layout_row = initial_hero_location.take(0)
        self.hero_layout_column = initial_hero_location.take(1)

        # TODO: Fix the initial camera_pos calculation.

        width_midpoint = len(self.current_map.layout[0]) / 2
        height_midpoint = len(self.current_map.layout) / 2
        if self.hero_layout_row <= height_midpoint and self.hero_layout_column <= width_midpoint:
            self.camera_pos = get_initial_camera_position((int((self.hero_layout_column - width_midpoint)*10), (int(self.hero_layout_row - height_midpoint)*2)))
        elif self.hero_layout_row <= height_midpoint and self.hero_layout_column >= width_midpoint:
            self.camera_pos = get_initial_camera_position((int(self.hero_layout_row - width_midpoint), int(self.hero_layout_column - width_midpoint)))
        elif self.hero_layout_row >= height_midpoint and self.hero_layout_column <= width_midpoint:
            self.camera_pos = get_initial_camera_position((int(self.hero_layout_row - width_midpoint), int(self.hero_layout_column - width_midpoint)))
        elif self.hero_layout_row >= height_midpoint and self.hero_layout_column >= width_midpoint:
            self.camera_pos = get_initial_camera_position((int(self.hero_layout_row - width_midpoint), int(self.hero_layout_column - width_midpoint)))
        else:
            self.camera_pos = get_initial_camera_position((width_midpoint - self.hero_layout_row,
                                                           height_midpoint - self.hero_layout_column))
        # AIMING FOR -5, -3 (or -160, -96 when multiplied by TILE_SIZE) for Tantegel Throne Room
        # self.camera_pos = 2 * TILE_SIZE, 4 * TILE_SIZE
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
            if event.type == pygame.QUIT or (event.type == pygame.K_LCTRL and event.key == pygame.K_ESCAPE):
                quit()
                sys.exit()
        # TODO: Smooth out movement even more.
        key = pygame.key.get_pressed()
        self.hero_layout_row = self.current_map.player.rect.y // TILE_SIZE
        self.hero_layout_column = self.current_map.player.rect.x // TILE_SIZE
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

    def get_tile_by_coordinates(self, row, column):
        if row < len(self.current_map.layout) and column < len(self.current_map.layout[0]):
            return self.current_map.get_tile_by_value(self.current_map.layout[row][column])

    def move_player(self, key):
        # block establishes direction if needed and whether to start
        # or stop moving
        # TODO ED separate dependency of camera pos and player pos
        curr_pos_x, curr_pos_y = self.camera_pos

        if not self.player_moving:
            if key[pygame.K_UP]:
                self.current_map.player.direction = Direction.UP.value
            elif key[pygame.K_DOWN]:
                self.current_map.player.direction = Direction.DOWN.value
            elif key[pygame.K_LEFT]:
                self.current_map.player.direction = Direction.LEFT.value
            elif key[pygame.K_RIGHT]:
                self.current_map.player.direction = Direction.RIGHT.value
            else:  # player not moving and no moving key pressed
                return
            self.player_moving = True
        else:  # determine if player has reached new tile
            if (self.current_map.player.direction == Direction.UP.value or
                    self.current_map.player.direction == Direction.DOWN.value):
                if curr_pos_y % TILE_SIZE == 0:
                    self.player_moving = False
                    self.next_tile_checked = False
                    return
            elif (self.current_map.player.direction == Direction.LEFT.value or
                  self.current_map.player.direction == Direction.RIGHT.value):
                if curr_pos_x % TILE_SIZE == 0:
                    self.player_moving = False
                    self.next_tile_checked = False
                    return

        if self.current_map.player.direction == Direction.UP.value:
            self.move(delta_x=0, delta_y=self.speed)
        elif self.current_map.player.direction == Direction.DOWN.value:
            self.move(delta_x=0, delta_y=-self.speed)
        elif self.current_map.player.direction == Direction.LEFT.value:
            self.move(delta_x=-self.speed, delta_y=0)
        elif self.current_map.player.direction == Direction.RIGHT.value:
            self.move(delta_x=self.speed, delta_y=0)

    def move(self, delta_x, delta_y):
        curr_cam_pos_x, curr_cam_pos_y = self.camera_pos
        next_cam_pos_x = curr_cam_pos_x
        next_cam_pos_y = curr_cam_pos_y
        if not self.next_tile_checked:
            self.next_tile = self.get_next_tile()
            self.next_tile_checked = True
        print(self.next_tile)
        if not self.did_collide(self.next_tile):
            self.current_map.player.rect.x += delta_x
            next_cam_pos_x = curr_cam_pos_x + -delta_x
            self.current_map.player.rect.y += -delta_y
            next_cam_pos_y = curr_cam_pos_y + delta_y
        else:
            # TODO: Slow down the bump sound effect.
            play_sound(bump_sfx)

        next_cam_pos_x = self.handle_lr_sides_collision(next_cam_pos_x, delta_x)
        next_cam_pos_y = self.handle_tb_sides_collision(next_cam_pos_y)
        self.camera_pos = next_cam_pos_x, next_cam_pos_y

    def get_next_tile(self):
        if self.current_map.player.direction == Direction.UP.value:
            return self.get_tile_by_coordinates(self.hero_layout_row - 1, self.hero_layout_column)
        elif self.current_map.player.direction == Direction.DOWN.value:
            return self.get_tile_by_coordinates(self.hero_layout_row + 1, self.hero_layout_column)
        elif self.current_map.player.direction == Direction.LEFT.value:
            return self.get_tile_by_coordinates(self.hero_layout_row, self.hero_layout_column - 1)
        elif self.current_map.player.direction == Direction.RIGHT.value:
            return self.get_tile_by_coordinates(self.hero_layout_row, self.hero_layout_column + 1)

    def did_collide(self, next_tile):
        return next_tile in self.current_map.impassable_tiles

    def handle_tb_sides_collision(self, next_pos_y):
        max_bound = self.current_map.height
        min_bound = 0
        player_pos = self.current_map.player.rect.y
        if player_pos < min_bound:
            self.current_map.player.rect.y = min_bound
            play_sound(bump_sfx)
            next_pos_y -= self.speed
        elif player_pos > max_bound - TILE_SIZE:
            self.current_map.player.rect.y = max_bound - TILE_SIZE
            play_sound(bump_sfx)
            next_pos_y += self.speed
        return next_pos_y

    def handle_lr_sides_collision(self, next_pos_x, delta_x):
        max_bound = self.current_map.width
        min_bound = 0
        player_pos = self.current_map.player.rect.x
        if player_pos < min_bound:  # Simple Sides Collision
            self.current_map.player.rect.x = min_bound  # Reset Player Rect Coord
            play_sound(bump_sfx)
            next_pos_x += delta_x
        elif player_pos > max_bound - TILE_SIZE:
            self.current_map.player.rect.x = max_bound - TILE_SIZE
            play_sound(bump_sfx)
            next_pos_x += delta_x
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
        self.current_map = TantegelThroneRoom(self.map_tiles, self.unarmed_hero_images, self.roaming_guard_images)
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
