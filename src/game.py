import random
import sys

import pygame as pg
from pygame import init, Surface, USEREVENT, time, quit, FULLSCREEN, RESIZABLE, DOUBLEBUF
from pygame.display import set_mode, set_caption
from pygame.event import get
from pygame.time import Clock
from pygame.time import get_ticks
from pygame.transform import scale

import menu
from RoamingCharacter import handle_roaming_character_sides_collision
from config import NES_RES
from maps import get_roaming_character_position
from src import maps
from src.camera import Camera
from src.common import Direction, play_sound, bump_sfx, UNARMED_HERO_PATH, get_image, \
    menu_button_sfx, stairs_down_sfx, stairs_up_sfx, BLACK
from src.config import SCALE, TILE_SIZE, FULLSCREEN_ENABLED, MUSIC_ENABLED
from src.maps import parse_animated_spritesheet


class Game:
    GAME_TITLE = "Dragon Warrior"
    FPS = 60
    BACK_FILL_COLOR = BLACK
    MOVE_EVENT = USEREVENT + 1
    time.set_timer(MOVE_EVENT, 100)

    def __init__(self):
        # Initialize pygame
        self.command_menu_subsurface = None
        self.character_rects = []
        self.map_rects = []
        self.opacity = 0
        init()

        self.command_menu_launched, self.paused = False, False
        # Create the game window.
        if FULLSCREEN_ENABLED:
            flags = FULLSCREEN | DOUBLEBUF
        else:
            flags = RESIZABLE | DOUBLEBUF
        self.scale = SCALE
        self.win_width = NES_RES[0] * self.scale
        self.win_height = NES_RES[1] * self.scale
        self.screen = set_mode((self.win_width, self.win_height), flags)
        self.screen.set_alpha(None)
        set_caption(self.GAME_TITLE)
        self.roaming_character_go_cooldown = 3000
        self.next_tile_checked = False
        unarmed_hero_sheet = get_image(UNARMED_HERO_PATH)
        unarmed_hero_tilesheet = scale(unarmed_hero_sheet, (
            unarmed_hero_sheet.get_width() * self.scale, unarmed_hero_sheet.get_height() * self.scale))
        self.unarmed_hero_images = parse_animated_spritesheet(unarmed_hero_tilesheet, is_roaming=True)

        self.current_map = maps.TantegelThroneRoom(hero_images=self.unarmed_hero_images)
        # self.current_map = maps.TantegelCourtyard(hero_images=self.unarmed_hero_images)
        # self.current_map = maps.Overworld(hero_images=self.unarmed_hero_images)

        # self.current_map = maps.TestMap(hero_images=self.unarmed_hero_images)
        self.bigmap_width, self.bigmap_height = self.current_map.width, self.current_map.height
        self.bigmap = Surface((self.bigmap_width, self.bigmap_height)).convert()
        self.bigmap.fill(self.BACK_FILL_COLOR)
        self.player_moving = False
        self.speed = 2
        for roaming_character in self.current_map.roaming_characters:
            roaming_character.last_roaming_clock_check = get_ticks()
            get_roaming_character_position(roaming_character)
        # Make the big scrollable map
        self.background = self.bigmap.subsurface(0, 0, self.current_map.width,
                                                 self.current_map.height).convert()
        self.current_map.load_map()
        initial_hero_location = self.current_map.get_initial_character_location('HERO')
        self.hero_layout_row, self.hero_layout_column = initial_hero_location.take(0), initial_hero_location.take(1)
        self.cmd_menu = menu.CommandMenu(self.background, self.hero_layout_row, self.hero_layout_column)
        self.next_tile = self.get_next_tile(character_column=self.hero_layout_column,
                                            character_row=self.hero_layout_row,
                                            direction=self.current_map.player.direction)
        self.camera = Camera(hero_position=(int(self.hero_layout_column), int(self.hero_layout_row)),
                             current_map=self.current_map, speed=None)
        self.command_menu_launch_signaled = False
        self.enable_animate, self.enable_roaming, self.enable_movement = True, True, True
        self.clock = Clock()
        if MUSIC_ENABLED:
            pg.mixer.music.load(self.current_map.music_file_path)
            pg.mixer.music.play(-1)
        self.events = get()
        self.background = self.bigmap.subsurface(0, 0, self.current_map.width,
                                                 self.current_map.height).convert()

        # pg.event.set_allowed([pg.QUIT])

    def main(self):
        """
        Main loop.
        :return: None
        """
        while 1:
            self.clock.tick(self.FPS)
            self.get_events()
            self.draw_all()
            self.update_screen()

    def get_events(self):
        """
        Handle all events in main loop.
        :return: None
        """
        self.events = get()

        for event in self.events:
            if event.type == pg.QUIT:
                quit()
                sys.exit()
        pg.event.pump()
        key = pg.key.get_pressed()
        self.hero_layout_column, self.hero_layout_row = self.current_map.player.rect.x // TILE_SIZE, self.current_map.player.rect.y // TILE_SIZE
        if self.enable_roaming and self.current_map.roaming_characters:
            self.move_roaming_characters()
        if self.enable_movement:
            self.move_player(key)

        for staircase_location, staircase_dict in self.current_map.staircases.items():
            if (self.hero_layout_row, self.hero_layout_column) == staircase_location:
                if staircase_dict['stair_direction'] == 'down':
                    play_sound(stairs_down_sfx)
                elif staircase_dict['stair_direction'] == 'up':
                    play_sound(stairs_up_sfx)
                self.map_change(staircase_dict['map'])

        if key[pg.K_j]:
            # B button
            self.unlaunch_command_menu()
            # print("J key pressed (B button).")
        if key[pg.K_k]:
            # A button
            # print("K key pressed (A button).")
            if not self.player_moving:
                self.command_menu_launch_signaled = True
                self.pause_all_movement()
        if key[pg.K_i]:
            # Start button
            if self.paused:
                self.unpause_all_movement()
            else:
                self.pause_all_movement()
            print("I key pressed (Start button).")
        if key[pg.K_u]:
            # Select button
            pass
            print("U key pressed (Select button).")
        # TODO: Allow for zoom in and out if Ctrl + PLUS | MINUS is pressed.

        # if key[pg.K_LCTRL] and (key[pg.K_PLUS] or key[pg.K_KP_PLUS]):
        #     self.scale = self.scale + 1

        # For debugging purposes, this prints out the current tile that the player is standing on.
        # print(self.get_tile_by_coordinates(self.current_map.player.rect.y // TILE_SIZE,
        #                                    self.current_map.player.rect.x // TILE_SIZE))

        # For debugging purposes, this prints out the current coordinates that the player is standing on.
        # print(self.current_map.player.rect.y // TILE_SIZE, self.current_map.player.rect.x // TILE_SIZE)

        # player_next_coordinates = get_next_coordinates(self.current_map.player.rect.x // TILE_SIZE,
        #                                                self.current_map.player.rect.y // TILE_SIZE,
        #                                                self.current_map.player.direction)
        # For debugging purposes, this prints out the next coordinates that the player will land on.
        # print(player_next_coordinates)

        # For debugging purposes, this prints out the next tile that the player will land on.
        # print(self.get_tile_by_coordinates(player_next_coordinates[1], player_next_coordinates[0]))

        pg.event.pump()

    def draw_all(self):
        """
        Draw map, sprites, background, menu and other surfaces.
        :return: None
        """
        for group in self.current_map.all_floor_sprite_groups:
            group.draw(self.bigmap)
        self.screen.fill(self.BACK_FILL_COLOR)
        self.background = self.bigmap.subsurface(0, 0, self.current_map.width, self.current_map.height).convert()

        for character in self.current_map.characters:
            if self.enable_animate:
                character.animate()
            else:
                character.pause()
        for sprites in self.current_map.character_sprites:
            self.character_rects.append(sprites.draw(self.background))
        if self.command_menu_launch_signaled:
            self.command_menu_subsurface = self.background.subsurface(
                (self.hero_layout_column * TILE_SIZE) - TILE_SIZE * 2,
                (self.hero_layout_row * TILE_SIZE) - (TILE_SIZE * 6),
                TILE_SIZE * 8, TILE_SIZE * 5)
            if not self.command_menu_launched:
                self.launch_command_menu()
            else:
                command_menu_rect = self.cmd_menu.command_menu.draw(self.command_menu_subsurface)
                if command_menu_rect:
                    self.character_rects.append(command_menu_rect)
        self.screen.blit(self.background, self.camera.get_pos())

    def update_screen(self):
        """Update the screen's display."""
        if self.command_menu_launched:
            self.cmd_menu.command_menu.update(self.events)
        pg.display.update()

    def fade_out(self, width, height):
        """
        Fade from current scene to black.
        :return: None
        """
        fade = pg.Surface((width, height))
        fade.fill(BLACK)
        self.opacity = 0
        for r in range(300):
            self.opacity += 1
            fade.set_alpha(self.opacity)
            self.background.fill(BLACK)
            self.screen.blit(fade, (0, 0))
            pg.display.update()
            pg.time.delay(5)

    def fade_in(self, width, height):
        # TODO(ELF): Fix fade_in.
        """
        Fade from black to current screen.
        :return: None
        """
        fade = pg.Surface((width, height))
        fade.fill(BLACK)
        self.opacity = 300
        for alpha in range(300):
            self.opacity -= 1
            fade.set_alpha(self.opacity)
            self.background.fill(BLACK)
            self.screen.blit(fade, (0, 0))
            pg.display.update()
            pg.time.delay(5)

    def map_change(self, next_map):
        """
        Change to a different map.
        :param next_map: The next map to be loaded.
        :return: None
        """
        self.pause_all_movement()
        self.background = Surface(self.screen.get_size()).convert()
        self.current_map = next_map
        self.bigmap_width, self.bigmap_height = self.current_map.width, self.current_map.height
        self.bigmap = Surface((self.bigmap_width, self.bigmap_height)).convert()
        self.bigmap.fill(self.BACK_FILL_COLOR)
        self.fade_out(self.win_width, self.win_height)
        if MUSIC_ENABLED:
            pg.mixer.music.stop()
        self.current_map.load_map()
        if MUSIC_ENABLED:
            pg.mixer.music.load(self.current_map.music_file_path)
            pg.mixer.music.play(-1)
        initial_hero_location = self.current_map.get_initial_character_location('HERO')
        self.hero_layout_row, self.hero_layout_column = initial_hero_location.take(0), initial_hero_location.take(1)
        self.camera = Camera(hero_position=(int(self.hero_layout_column), int(self.hero_layout_row)),
                             current_map=self.current_map, speed=None)
        self.fade_in(self.win_width, self.win_height)

        self.unpause_all_movement()

        # play_music(self.current_map.music_file_path)

    def unlaunch_command_menu(self):
        """
        Unlaunch the command menu.
        :return: None
        """
        self.command_menu_launch_signaled = False
        self.unpause_all_movement()
        self.command_menu_launched = False

    def unpause_all_movement(self):
        """
        Unpause movement of animation, roaming, and character.
        :return: None
        """
        self.enable_animate, self.enable_roaming, self.enable_movement = True, True, True
        self.paused = False

    def pause_all_movement(self):
        """
        Pause movement of animation, roaming, and character.
        :return: None
        """
        self.enable_animate, self.enable_roaming, self.enable_movement = False, False, False
        self.paused = True

    def launch_command_menu(self):
        """
        Launch the command menu, which is used by the player to interact with the world in the game.
        :return: None
        """
        if not self.command_menu_launched:
            play_sound(menu_button_sfx)
        command_menu_rect = self.cmd_menu.command_menu.draw(self.command_menu_subsurface)
        if command_menu_rect:
            self.character_rects.append(command_menu_rect)
        self.command_menu_launched = True

    def get_tile_by_coordinates(self, column, row):
        """
        Retrieve the tile name from the coordinates of the tile on the map.
        :param column: The column of the tile.
        :param row: The row of the tile.
        """
        if row < len(self.current_map.layout) and column < len(self.current_map.layout[0]):
            return self.current_map.get_tile_by_value(self.current_map.layout[row][column])

    def move_player(self, key):
        """
        Move the player in a specified direction.
        :param key: The key currently being pressed by the user.
        """
        # block establishes direction if needed and whether to start
        # or stop moving
        # TODO(ELF): separate dependency of camera pos and player pos
        curr_pos_x, curr_pos_y = self.camera.get_pos()

        if not self.player_moving:
            if key[pg.K_UP] or key[pg.K_w]:
                self.current_map.player.direction = Direction.UP.value
            elif key[pg.K_DOWN] or key[pg.K_s]:
                self.current_map.player.direction = Direction.DOWN.value
            elif key[pg.K_LEFT] or key[pg.K_a]:
                self.current_map.player.direction = Direction.LEFT.value
            elif key[pg.K_RIGHT] or key[pg.K_d]:
                self.current_map.player.direction = Direction.RIGHT.value
            else:  # player not moving and no moving key pressed
                return
            self.player_moving = True
        else:  # determine if player has reached new tile
            self.current_map.player_sprites.dirty = 1
            if (self.current_map.player.direction == Direction.UP.value or
                    self.current_map.player.direction == Direction.DOWN.value):
                if curr_pos_y % TILE_SIZE == 0:
                    self.player_moving, self.next_tile_checked = False, False
                    return
            elif (self.current_map.player.direction == Direction.LEFT.value or
                  self.current_map.player.direction == Direction.RIGHT.value):
                if curr_pos_x % TILE_SIZE == 0:
                    self.player_moving, self.next_tile_checked = False, False
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
        self.current_map.player_sprites.dirty = 1

    def move(self, delta_x, delta_y):
        """
        The method that actuates the movement of the player from within the move_player method.
        :param delta_x: Change in x position.
        :param delta_y: Change in y position.
        :return: None
        """
        curr_cam_pos_x, curr_cam_pos_y = self.camera.get_pos()
        next_cam_pos_x, next_cam_pos_y = curr_cam_pos_x, curr_cam_pos_y
        if not self.next_tile_checked:
            self.next_tile = self.get_next_tile(character_column=self.hero_layout_column,
                                                character_row=self.hero_layout_row,
                                                direction=self.current_map.player.direction)
            self.next_tile_checked = True
        roaming_character_locations = [(roaming_character.column, roaming_character.row) for roaming_character in
                                       self.current_map.roaming_characters]
        if not self.is_impassable(self.next_tile):
            if self.get_next_coordinates(self.hero_layout_column, self.hero_layout_row,
                                         self.current_map.player.direction) not in roaming_character_locations:
                if delta_x:
                    self.current_map.player.rect.x += delta_x
                    next_cam_pos_x = curr_cam_pos_x + -delta_x
                if delta_y:
                    self.current_map.player.rect.y += -delta_y
                    next_cam_pos_y = curr_cam_pos_y + delta_y
            else:
                play_sound(bump_sfx)
        else:
            play_sound(bump_sfx)

        next_cam_pos_x, next_cam_pos_y = self.handle_sides_collision(next_cam_pos_x, next_cam_pos_y)
        self.camera.set_pos((next_cam_pos_x, next_cam_pos_y))

    def get_next_tile(self, character_column: int, character_row: int, direction) -> str:
        """
        Retrieve the next tile to be stepped on by a particular character.
        :type character_column: int
        :type character_row: int
        :param character_column: The character's column within the map layout.
        :param character_row: The character's row within the map layout.
        :param direction: The direction which the character is facing.
        :return: str: The next tile that the character will step on (e.g., 'BRICK').
        """
        if direction == Direction.UP.value:
            return self.get_tile_by_coordinates(character_column, character_row - 1)
        elif direction == Direction.DOWN.value:
            return self.get_tile_by_coordinates(character_column, character_row + 1)
        elif direction == Direction.LEFT.value:
            return self.get_tile_by_coordinates(character_column - 1, character_row)
        elif direction == Direction.RIGHT.value:
            return self.get_tile_by_coordinates(character_column + 1, character_row)

    def get_next_coordinates(self, character_column, character_row, direction):
        if character_row < len(self.current_map.layout) and character_column < len(self.current_map.layout[0]):
            if direction == Direction.UP.value:
                return character_column, character_row - 1
            elif direction == Direction.DOWN.value:
                return character_column, character_row + 1,
            elif direction == Direction.LEFT.value:
                return character_column - 1, character_row
            elif direction == Direction.RIGHT.value:
                return character_column + 1, character_row

    def is_impassable(self, tile):
        """
        Check if a tile is impassable (a tile that blocks the player from moving).
        :param tile: Tile to be checked for impassibility.
        :return: bool: A boolean value stating whether or not the tile is impassable.
        """
        return tile in self.current_map.impassable_tiles

    def handle_sides_collision(self, next_pos_x: int, next_pos_y: int):
        """
        Handle collision with the sides of the map (for the player).
        :type next_pos_x: int
        :type next_pos_y: int
        :param next_pos_x: Next x position (in terms of tile size).
        :param next_pos_y: Next y position (in terms of tile size).
        :return: tuple: The x, y coordinates (in terms of tile size) of the next position of the player.
        """
        max_x_bound, max_y_bound, min_bound = self.current_map.width, self.current_map.height, 0
        player_pos_x, player_pos_y = self.current_map.player.rect.x, self.current_map.player.rect.y
        if player_pos_x < min_bound:
            self.current_map.player.rect.x = min_bound
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
        """
        Move all roaming characters in the current map.
        :return: None
        """
        # TODO: Extend roaming characters beyond just the roaming guard.
        for roaming_character in self.current_map.roaming_characters:
            get_roaming_character_position(roaming_character)
            now = get_ticks()
            if roaming_character.last_roaming_clock_check is None:
                roaming_character.last_roaming_clock_check = now
            if now - roaming_character.last_roaming_clock_check >= self.roaming_character_go_cooldown:
                roaming_character.last_roaming_clock_check = now
                if not roaming_character.moving:
                    roaming_character.direction = random.choice(list(map(int, Direction)))
                else:  # character not moving and no input
                    return
                roaming_character.moving = True
            else:  # determine if character has reached new tile
                if roaming_character.direction == Direction.UP.value or roaming_character.direction == Direction.DOWN.value:
                    if roaming_character.rect.y % TILE_SIZE == 0:
                        roaming_character.moving, roaming_character.next_tile_checked = False, False
                        return
                elif roaming_character.direction == Direction.LEFT.value or roaming_character.direction == Direction.RIGHT.value:
                    if roaming_character.rect.x % TILE_SIZE == 0:
                        roaming_character.moving, roaming_character.next_tile_checked = False, False
                        return
            if roaming_character.direction == Direction.UP.value:
                self.move_roaming_character(delta_x=0, delta_y=self.speed, roaming_character=roaming_character)
            elif roaming_character.direction == Direction.DOWN.value:
                self.move_roaming_character(delta_x=0, delta_y=-self.speed, roaming_character=roaming_character)
            elif roaming_character.direction == Direction.LEFT.value:
                self.move_roaming_character(delta_x=-self.speed, delta_y=0, roaming_character=roaming_character)
            elif roaming_character.direction == Direction.RIGHT.value:
                self.move_roaming_character(delta_x=self.speed, delta_y=0, roaming_character=roaming_character)
            else:
                print("Invalid direction.")
            handle_roaming_character_sides_collision(self.current_map, roaming_character)

    def move_roaming_character(self, delta_x, delta_y, roaming_character):
        """
        The method that actuates the movement of the roaming characters from within the move_roaming_characters method.
        :param delta_x: Change in x position.
        :param delta_y: Change in y position.
        :param roaming_character: Roaming character to be moved.
        :return: None
        """
        if not roaming_character.next_tile_checked:
            roaming_character.next_tile = self.get_next_tile(character_column=roaming_character.column,
                                                             character_row=roaming_character.row,
                                                             direction=roaming_character.direction)
            roaming_character.next_tile_checked = True
        if not self.is_impassable(roaming_character.next_tile) and (
                roaming_character.column, roaming_character.row) != (self.hero_layout_column, self.hero_layout_row):
            if delta_x:
                roaming_character.rect.x += delta_x
            if delta_y:
                roaming_character.rect.y += -delta_y


def run():
    game = Game()
    game.main()


if __name__ == "__main__":
    run()
