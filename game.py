import random
import sys

import pygame
import pygameMenu
from pygame import init, Surface, USEREVENT, time, quit, FULLSCREEN
from pygame.display import set_mode, set_caption, flip
from pygame.event import get
from pygame.time import Clock
from pygame.time import get_ticks
from pygame.transform import scale

import maps
from camera import Camera
from common import Direction, play_sound, bump_sfx, MAP_TILES_PATH, UNARMED_HERO_PATH, get_image, \
    menu_button_sfx, DRAGON_QUEST_FONT_PATH
from config import NES_RES, SCALE, WIN_WIDTH, WIN_HEIGHT, TILE_SIZE, FULLSCREEN_ENABLED
from maps import parse_animated_spritesheet


def move_roaming_character(delta_x, delta_y, sprite):
    sprite.rect.x += delta_x
    sprite.rect.y += -delta_y


def get_next_coordinates(character_column, character_row, direction):
    if direction == Direction.UP.value:
        return character_row - 1, character_column
    elif direction == Direction.DOWN.value:
        return character_row + 1, character_column
    elif direction == Direction.LEFT.value:
        return character_row, character_column - 1
    elif direction == Direction.RIGHT.value:
        return character_row, character_column + 1


class Game:
    FPS = 60
    GAME_TITLE = "Dragon Warrior"
    WIN_WIDTH = NES_RES[0] * SCALE
    WIN_HEIGHT = NES_RES[1] * SCALE

    ORIGIN = (0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BACK_FILL_COLOR = BLACK
    MOVE_EVENT = USEREVENT + 1
    time.set_timer(MOVE_EVENT, 100)

    def __init__(self):

        # Initialize pygame
        self.command_menu_launched = False
        self.paused = False
        init()

        # Create the game window.
        if FULLSCREEN_ENABLED:
            self.screen = set_mode((WIN_WIDTH, WIN_HEIGHT), FULLSCREEN)
        else:
            self.screen = set_mode((WIN_WIDTH, WIN_HEIGHT))
        set_caption(self.GAME_TITLE)
        self.clock = Clock()
        self.roaming_character_go_cooldown = 3000
        self.current_map = None
        if maps.current_map is None:
            maps.current_map = maps.TantegelThroneRoom

        self.map_tiles = []
        self.bigmap_width = None
        self.bigmap_height = None
        self.bigmap = None
        self.current_map_height = None
        self.background = None
        self.next_tile = None
        self.next_tile_checked = False

        self.left_face_guard_images = None
        self.right_face_guard_images = None
        self.roaming_guard_images = None
        self.unarmed_hero_images = None
        self.load_images()
        self.map_tilesheet = None

        self.hero_layout_row = None
        self.hero_layout_column = None
        self.player_moving = False
        self.speed = 2

        self.load_current_map()
        for roaming_character in self.current_map.roaming_characters:
            roaming_character.last_roaming_clock_check = get_ticks()
            roaming_character.column = roaming_character.rect.x // TILE_SIZE
            roaming_character.row = roaming_character.rect.y // TILE_SIZE
        # Make the big scrollable map
        # TODO(ELF): Refactor these into the actual values and remove the None assignments that they replace.
        self.make_bigmap()
        self.background = Surface(self.screen.get_size()).convert()
        initial_hero_location = self.current_map.get_initial_character_location('HERO')
        self.hero_layout_row = initial_hero_location.take(0)
        self.hero_layout_column = initial_hero_location.take(1)
        hero_row = int(self.hero_layout_row)
        hero_col = int(self.hero_layout_column)
        self.camera = Camera(hero_position=(hero_row, hero_col), current_map=self.current_map, speed=None)
        self.enable_command_menu = False
        self.enable_animate = True
        self.enable_roaming = True
        self.enable_movement = True

    def main(self):
        while 1:
            self.clock.tick(self.FPS)
            self.events()
            self.draw()
            self.update()

    def events(self):

        for event in get():
            if event.type == pygame.QUIT or (event.type == pygame.K_LCTRL and event.key == pygame.K_q):
                quit()
                sys.exit()
        key = pygame.key.get_pressed()
        self.hero_layout_row = self.current_map.player.rect.y // TILE_SIZE
        self.hero_layout_column = self.current_map.player.rect.x // TILE_SIZE
        if self.enable_roaming:
            self.move_roaming_characters()
        if self.enable_movement:
            self.move_player(key)
        # # TODO: implement actual function of B, A, Start, Select buttons.
        if key[pygame.K_j]:
            # B button
            self.unlaunch_command_menu()
            print("You pressed the J key (B button).")
        if key[pygame.K_k]:
            # A button
            self.enable_command_menu = True
            self.pause_all_movement()
            print("You pressed the K key (A button).")

        if key[pygame.K_i]:
            # Start button
            if self.paused:
                self.unpause_all_movement()
            else:
                self.pause_all_movement()
            print("You pressed the I key (Start button).")
        if key[pygame.K_u]:
            # Select button
            print("You pressed the U key (Select button).")

        # For debugging purposes, this prints out the current tile that the hero is standing on.
        # print(self.get_tile_by_coordinates(self.current_map.player.rect.y // TILE_SIZE,
        #                                    self.current_map.player.rect.x // TILE_SIZE))
        # THESE ARE THE VALUES WE ARE AIMING FOR FOR INITIAL TANTEGEL THRONE ROOM
        # camera_pos = -160, -96

    def unlaunch_command_menu(self):
        self.enable_command_menu = False
        self.unpause_all_movement()
        self.command_menu_launched = False

    def unpause_all_movement(self):
        self.enable_animate = True
        self.enable_roaming = True
        self.enable_movement = True
        self.paused = False

    def pause_all_movement(self):
        self.enable_animate = False
        self.enable_roaming = False
        self.enable_movement = False
        self.paused = True

    def draw(self):
        self.current_map.draw_map(self.bigmap)
        for sprites in self.current_map.character_sprites:
            sprites.clear(self.screen, self.background)
        self.screen.fill(self.BACK_FILL_COLOR)
        self.background = self.bigmap.subsurface(self.ORIGIN[0], self.ORIGIN[1], self.current_map.width,
                                                 self.current_map.height).convert()
        for character in self.current_map.characters:
            if self.enable_animate:
                character.animate()
        for sprites in self.current_map.character_sprites:
            sprites.draw(self.background)
        if self.enable_command_menu:
            self.launch_command_menu()

    def launch_command_menu(self):
        if not self.command_menu_launched:
            play_sound(menu_button_sfx)

        menu_subsurface = self.background.subsurface((self.hero_layout_column * TILE_SIZE) - TILE_SIZE * 2,
                                                     (self.hero_layout_row * TILE_SIZE) - (TILE_SIZE * 6),
                                                     TILE_SIZE * 8, TILE_SIZE * 5)
        menu = pygameMenu.Menu(surface=menu_subsurface,
                               window_width=TILE_SIZE * 5,
                               window_height=TILE_SIZE * 8,
                               font=DRAGON_QUEST_FONT_PATH,
                               title='COMMAND',
                               back_box=False,
                               bgfun=self.update,
                               color_selected=Game.RED,
                               dopause=True,
                               draw_region_x=89,
                               draw_region_y=41,
                               draw_select=False,
                               enabled=False,
                               font_color=Game.WHITE,
                               font_size=16,
                               font_size_title=16,
                               font_title=DRAGON_QUEST_FONT_PATH,
                               fps=60,
                               joystick_enabled=True,
                               menu_alpha=100,
                               menu_color=Game.BLACK,
                               # menu_color_title=Game.WHITE,
                               # menu_height=_cfg.MENU_HEIGHT,
                               # menu_width=_cfg.MENU_WIDTH,
                               mouse_enabled=False,
                               mouse_visible=False,
                               # onclose=None,
                               option_margin=15,
                               option_shadow=False,
                               # option_shadow_offset=_cfg.MENU_SHADOW_OFFSET,
                               # option_shadow_position=_cfg.MENU_SHADOW_POSITION,
                               # rect_width=_cfg.MENU_SELECTED_WIDTH,
                               title_offsetx=280,
                               title_offsety=71,
                               widget_alignment=pygameMenu.locals.ALIGN_LEFT,
                               columns=2,
                               rows=4,
                               column_weights=None,
                               # force_fit_text=False
                               )
        menu.add_button('TALK', self.talk, align=pygameMenu.locals.ALIGN_LEFT)
        menu.add_button('STATUS', self.status, align=pygameMenu.locals.ALIGN_LEFT)
        menu.add_button('STAIRS', self.stairs, align=pygameMenu.locals.ALIGN_LEFT)
        menu.add_button('SEARCH', self.search, align=pygameMenu.locals.ALIGN_LEFT)
        menu.add_button('SPELL', self.spell, align=pygameMenu.locals.ALIGN_LEFT)
        menu.add_button('ITEM', self.item, align=pygameMenu.locals.ALIGN_LEFT)
        menu.add_button('DOOR', self.door, align=pygameMenu.locals.ALIGN_LEFT)
        menu.add_button('TAKE', self.take, align=pygameMenu.locals.ALIGN_LEFT)

        menu.draw()
        self.command_menu_launched = True

    def talk(self):
        print("TALK")

    def status(self):
        print("STATUS")

    def stairs(self):
        print("STAIRS")

    def search(self):
        print("SEARCH")

    def spell(self):
        print("SPELL")

    def item(self):
        print("ITEM")

    def door(self):
        print("DOOR")

    def take(self):
        print("TAKE")

    def update(self):
        self.screen.blit(self.background, self.camera.get_pos())
        flip()

    def get_tile_by_coordinates(self, row, column):
        if row < len(self.current_map.layout) and column < len(self.current_map.layout[0]):
            return self.current_map.get_tile_by_value(self.current_map.layout[row][column])

    def move_player(self, key):
        # block establishes direction if needed and whether to start
        # or stop moving
        # TODO ED separate dependency of camera pos and player pos
        curr_pos_x, curr_pos_y = self.camera.get_pos()

        if not self.player_moving:
            if key[pygame.K_UP] or key[pygame.K_w]:
                self.current_map.player.direction = Direction.UP.value
            elif key[pygame.K_DOWN] or key[pygame.K_s]:
                self.current_map.player.direction = Direction.DOWN.value
            elif key[pygame.K_LEFT] or key[pygame.K_a]:
                self.current_map.player.direction = Direction.LEFT.value
            elif key[pygame.K_RIGHT] or key[pygame.K_d]:
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

        self.camera.move(self.current_map.player.direction)
        if self.current_map.player.direction == Direction.UP.value:
            self.move(delta_x=0, delta_y=self.speed)
        elif self.current_map.player.direction == Direction.DOWN.value:
            self.move(delta_x=0, delta_y=-self.speed)
        elif self.current_map.player.direction == Direction.LEFT.value:
            self.move(delta_x=-self.speed, delta_y=0)
        elif self.current_map.player.direction == Direction.RIGHT.value:
            self.move(delta_x=self.speed, delta_y=0)

    def move(self, delta_x, delta_y):
        curr_cam_pos_x, curr_cam_pos_y = self.camera.get_pos()
        next_cam_pos_x = curr_cam_pos_x
        next_cam_pos_y = curr_cam_pos_y
        if not self.next_tile_checked:
            self.next_tile = self.get_next_tile(character_row=self.hero_layout_row,
                                                character_column=self.hero_layout_column,
                                                direction=self.current_map.player.direction)
            self.next_tile_checked = True
        # print(self.next_tile)
        if not self.is_impassable(self.next_tile):
            self.current_map.player.rect.x += delta_x
            next_cam_pos_x = curr_cam_pos_x + -delta_x
            self.current_map.player.rect.y += -delta_y
            next_cam_pos_y = curr_cam_pos_y + delta_y
        else:
            # TODO: Slow down the bump sound effect.
            play_sound(bump_sfx)

        next_cam_pos_x, next_cam_pos_y = self.handle_sides_collision(next_cam_pos_x, next_cam_pos_y)
        # = self.handle_tb_sides_collision(next_cam_pos_y)
        self.camera.set_pos((next_cam_pos_x, next_cam_pos_y))

    def get_next_tile(self, character_row, character_column, direction):
        if direction == Direction.UP.value:
            return self.get_tile_by_coordinates(character_row - 1, character_column)
        elif direction == Direction.DOWN.value:
            return self.get_tile_by_coordinates(character_row + 1, character_column)
        elif direction == Direction.LEFT.value:
            return self.get_tile_by_coordinates(character_row, character_column - 1)
        elif direction == Direction.RIGHT.value:
            return self.get_tile_by_coordinates(character_row, character_column + 1)

    def is_impassable(self, next_tile):
        return next_tile in self.current_map.impassable_tiles

    def handle_sides_collision(self, next_pos_x, next_pos_y):
        max_x_bound = self.current_map.width
        max_y_bound = self.current_map.height
        min_bound = 0
        player_pos_x = self.current_map.player.rect.x
        player_pos_y = self.current_map.player.rect.y
        if player_pos_x < min_bound:  # Simple Sides Collision
            self.current_map.player.rect.x = min_bound  # Reset Player Rect Coord
            play_sound(bump_sfx)
            next_pos_x += -self.speed
        elif player_pos_x > max_x_bound - TILE_SIZE:
            self.current_map.player.rect.x = max_x_bound - TILE_SIZE
            play_sound(bump_sfx)
            next_pos_x += self.speed
        elif player_pos_y < min_bound:
            self.current_map.player.rect.y = min_bound
            play_sound(bump_sfx)
            next_pos_y -= self.speed
        elif player_pos_y > max_y_bound - TILE_SIZE:
            self.current_map.player.rect.y = max_y_bound - TILE_SIZE
            play_sound(bump_sfx)
            next_pos_y += self.speed
        return next_pos_x, next_pos_y

    def move_roaming_characters(self):
        # TODO: Disable moving of roaming characters if a dialog box is open.
        # TODO: Extend roaming characters beyond just the roaming guard.
        for roaming_character in self.current_map.roaming_characters:
            now = get_ticks()
            if now - roaming_character.last_roaming_clock_check >= self.roaming_character_go_cooldown:
                roaming_character.last_roaming_clock_check = now
                if not roaming_character.moving:
                    roaming_character.direction = random.randrange(4)
                else:  # character not moving and no input
                    return
                roaming_character.moving = True
            else: # determine if character has reached new tile
                if (roaming_character.direction == Direction.UP.value or
                        roaming_character.direction == Direction.DOWN.value):
                    if roaming_character.rect.y % TILE_SIZE == 0:
                        roaming_character.moving = False
                        roaming_character.next_tile_checked = False
                        return
                elif (roaming_character.direction == Direction.LEFT.value or
                      roaming_character.direction == Direction.RIGHT.value):
                    if roaming_character.rect.x % TILE_SIZE == 0:
                        roaming_character.moving = False
                        roaming_character.next_tile_checked = False
                        return
            if roaming_character.direction == Direction.UP.value:
                move_roaming_character(delta_x=0, delta_y=self.speed, sprite=roaming_character)
            elif roaming_character.direction == Direction.DOWN.value:
                # if self.did_collide_roaming(roaming_character, roaming_character.row, roaming_character.column):
                move_roaming_character(delta_x=0, delta_y=-self.speed, sprite=roaming_character)
            elif roaming_character.direction == Direction.LEFT.value:
                # if self.did_collide_roaming(roaming_character, roaming_character.row, roaming_character.column):
                move_roaming_character(delta_x=-self.speed, delta_y=0, sprite=roaming_character)
            elif roaming_character.direction == Direction.RIGHT.value:
                # if self.did_collide_roaming(roaming_character, roaming_character.row, roaming_character.column):
                move_roaming_character(delta_x=self.speed, delta_y=0, sprite=roaming_character)
            else:
                print("Invalid direction.")

    def did_collide_roaming(self, roaming_character, roaming_character_row, roaming_character_column):
        return self.is_impassable(self.get_next_tile(roaming_character_column, roaming_character_row,
                                                     roaming_character.direction)) or self.did_collide_with_hero(
            roaming_character, roaming_character_column, roaming_character_row)

    def did_collide_with_hero(self, roaming_character, roaming_character_column, roaming_character_row):
        return get_next_coordinates(roaming_character_column, roaming_character_row, roaming_character.direction) != (
            self.hero_layout_row, self.hero_layout_column)

    def handle_roaming_character_map_edge_side_collision(self, roaming_character):
        if roaming_character.rect.x < 0:  # Simple Sides Collision
            roaming_character.rect.x = 0  # Reset Player Rect Coord
        elif roaming_character.rect.x > self.current_map.width - TILE_SIZE:
            roaming_character.rect.x = self.current_map.width - TILE_SIZE
        if roaming_character.rect.y < 0:
            roaming_character.rect.y = 0
        elif roaming_character.rect.y > self.current_map.height - TILE_SIZE:
            roaming_character.rect.y = self.current_map.height - TILE_SIZE

    def make_bigmap(self):
        self.bigmap_width = self.current_map.width
        self.bigmap_height = self.current_map.height
        self.bigmap = Surface((self.bigmap_width, self.bigmap_height)).convert()
        self.bigmap.fill(self.BACK_FILL_COLOR)

    def load_current_map(self):
        self.current_map = maps.TantegelThroneRoom(self.map_tiles, self.unarmed_hero_images)
        # self.current_map = TantegelCourtyard(self.map_tiles, self.unarmed_hero_images)
        # self.current_map = maps.TestMap(self.map_tiles, self.unarmed_hero_images)
        self.current_map.load_map()

    def load_images(self):
        """Load all the images for the game graphics.
        """
        # Load the map tile spritesheet
        self.map_tilesheet = get_image(MAP_TILES_PATH).convert()
        # Load unarmed hero images
        unarmed_hero_sheet = get_image(UNARMED_HERO_PATH)

        self.map_tilesheet = scale(self.map_tilesheet,
                                   (self.map_tilesheet.get_width() * SCALE,
                                    self.map_tilesheet.get_height() * SCALE))
        unarmed_hero_sheet = scale(unarmed_hero_sheet,
                                   (unarmed_hero_sheet.get_width() * SCALE, unarmed_hero_sheet.get_height() * SCALE))

        self.parse_map_tiles()

        # Get the images for the initial hero sprites
        self.unarmed_hero_images = parse_animated_spritesheet(unarmed_hero_sheet, is_roaming=True)

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
