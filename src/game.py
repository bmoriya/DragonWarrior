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
from common import get_tile_by_coordinates, is_facing_up, is_facing_down, is_facing_left, is_facing_right
from config import NES_RES
from maps import get_character_position
from roaming_character import handle_roaming_character_sides_collision
from src import maps
from src.camera import Camera
from src.common import Direction, play_sound, bump_sfx, UNARMED_HERO_PATH, get_image, \
    menu_button_sfx, stairs_down_sfx, stairs_up_sfx, BLACK, is_facing_medially, is_facing_laterally
from src.config import SCALE, TILE_SIZE, FULLSCREEN_ENABLED, MUSIC_ENABLED
from src.maps import parse_animated_spritesheet


class Game:
    GAME_TITLE = "Dragon Warrior"
    FPS = 60
    BACK_FILL_COLOR = BLACK
    MOVE_EVENT = USEREVENT + 1
    # time.set_timer(MOVE_EVENT, 100)

    def __init__(self):
        # Initialize pygame
        self.character_rects = []
        self.opacity = 0
        init()

        self.command_menu_launched, self.paused = False, False
        # Create the game window.
        if FULLSCREEN_ENABLED:
            flags = FULLSCREEN | DOUBLEBUF
        else:
            flags = RESIZABLE | DOUBLEBUF
        self.scale = SCALE
        # video_infos = pg.display.Info()
        # current_screen_width, current_screen_height = video_infos.current_w, video_infos.current_h
        self.win_width = NES_RES[0] * self.scale
        self.win_height = NES_RES[1] * self.scale
        # self.win_width = current_screen_width
        # self.win_height = current_screen_height
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
        self.bigmap = Surface((self.current_map.width, self.current_map.height)).convert()
        self.bigmap.fill(self.BACK_FILL_COLOR)
        self.player_moving = False
        self.speed = 2
        for roaming_character in self.current_map.roaming_characters:
            roaming_character.last_roaming_clock_check = get_ticks()
            get_character_position(roaming_character)
        # Make the big scrollable map
        self.background = self.bigmap.subsurface(0, 0, self.current_map.width,
                                                 self.current_map.height).convert()
        self.current_map.load_map()
        initial_hero_location = self.current_map.get_initial_character_location('HERO')
        self.hero_layout_row, self.hero_layout_column = initial_hero_location.take(0), initial_hero_location.take(1)
        self.cmd_menu = menu.CommandMenu(self.background, self.hero_layout_column, self.hero_layout_row)
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
        self.command_menu_subsurface = self.background.subsurface((self.hero_layout_column - 2) * TILE_SIZE,
                                                                  (self.hero_layout_row - 6) * TILE_SIZE,
                                                                  8 * TILE_SIZE,
                                                                  5 * TILE_SIZE)

        # pg.event.set_allowed([pg.QUIT])

    def main(self) -> None:
        """
        Main loop.
        :return: None
        """
        while True:
            self.clock.tick(self.FPS)
            self.get_events()
            self.draw_all()
            self.update_screen()

    def get_events(self) -> None:
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
        self.hero_layout_column = self.current_map.player.rect.x // TILE_SIZE
        self.hero_layout_row = self.current_map.player.rect.y // TILE_SIZE
        if self.enable_roaming and self.current_map.roaming_characters:
            self.move_roaming_characters()
        if self.enable_movement:
            self.move_player(key)

        for staircase_location, staircase_dict in self.current_map.staircases.items():
            self.process_staircase_warps(staircase_dict, staircase_location)

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

    def process_staircase_warps(self, staircase_dict: dict, staircase_location) -> None:
        if (self.hero_layout_row, self.hero_layout_column) == staircase_location:
            if staircase_dict['stair_direction'] == 'down':
                play_sound(stairs_down_sfx)
            elif staircase_dict['stair_direction'] == 'up':
                play_sound(stairs_up_sfx)
            self.map_change(staircase_dict['map'])

    def draw_all(self) -> None:
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
            self.command_menu_subsurface = self.background.subsurface((self.hero_layout_column - 2) * TILE_SIZE,
                                                                      (self.hero_layout_row - 6) * TILE_SIZE,
                                                                      8 * TILE_SIZE,
                                                                      5 * TILE_SIZE)
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

    def fade(self, width: int, height: int, fade_out: bool) -> None:
        """
        Fade to/from current scene to/from black.
        :return: None
        @param width: int
        Width of surface to fade.
        @param height:
        Height of surface to fade.
        @type fade_out: bool
        If true, fades out. If false, fades in.
        """
        fade = pg.Surface((width, height))
        fade.fill(BLACK)
        self.opacity = 0
        for alpha in range(300):
            if fade_out:
                self.opacity += 1
            else:
                # TODO(ELF): Fix fade in.
                self.opacity -= 1
            fade.set_alpha(self.opacity)
            self.background.fill(BLACK)
            self.screen.blit(fade, (0, 0))
            pg.display.update()
            pg.time.delay(5)

    def map_change(self, next_map) -> None:
        """
        Change to a different map.
        :param next_map: The next map to be loaded.
        :return: None
        """
        self.pause_all_movement()
        self.background = Surface(self.screen.get_size()).convert()
        self.current_map = next_map
        self.bigmap = Surface((self.current_map.width, self.current_map.height)).convert()
        self.bigmap.fill(self.BACK_FILL_COLOR)
        self.fade(self.win_width, self.win_height, fade_out=True)
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
        self.fade(self.win_width, self.win_height, fade_out=False)

        self.unpause_all_movement()

        # play_music(self.current_map.music_file_path)

    def unlaunch_command_menu(self) -> None:
        """
        Unlaunch the command menu.
        :return: None
        """
        self.command_menu_launch_signaled = False
        self.unpause_all_movement()
        self.command_menu_launched = False

    def unpause_all_movement(self) -> None:
        """
        Unpause movement of animation, roaming, and character.
        :return: None
        """
        self.enable_animate, self.enable_roaming, self.enable_movement = True, True, True
        self.paused = False

    def pause_all_movement(self) -> None:
        """
        Pause movement of animation, roaming, and character.
        :return: None
        """
        self.enable_animate, self.enable_roaming, self.enable_movement = False, False, False
        self.paused = True

    def launch_command_menu(self) -> None:
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

    def move_player(self, key) -> None:
        """
        Move the player in a specified direction.
        :param key: The key currently being pressed by the user.
        """
        # block establishes direction if needed and whether to start or stop moving
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
            if is_facing_medially(self.current_map.player):
                if curr_pos_y % TILE_SIZE == 0:
                    self.player_moving, self.next_tile_checked = False, False
                    return
            elif is_facing_laterally(self.current_map.player):
                if curr_pos_x % TILE_SIZE == 0:
                    self.player_moving, self.next_tile_checked = False, False
                    return

        self.camera.move(self.current_map.player.direction)
        if is_facing_medially(self.current_map.player):
            self.move_medially(self.current_map.player)
        elif is_facing_laterally(self.current_map.player):
            self.move_laterally(self.current_map.player)
        self.current_map.player_sprites.dirty = 1

    def move_laterally(self, character) -> None:
        if is_facing_left(character):
            if character.name == "HERO":
                self.move(delta_x=-self.speed, delta_y=0)
            else:
                self.move_roaming_character(character, delta_x=-self.speed, delta_y=0)
        elif is_facing_right(character):
            if character.name == "HERO":
                self.move(delta_x=self.speed, delta_y=0)
            else:
                self.move_roaming_character(character, delta_x=self.speed, delta_y=0)

    def move_medially(self, character) -> None:
        if is_facing_up(character):
            if character.name == "HERO":
                self.move(delta_x=0, delta_y=self.speed)
            else:
                self.move_roaming_character(character, delta_x=0, delta_y=self.speed)
        elif is_facing_down(character):
            if character.name == "HERO":
                self.move(delta_x=0, delta_y=-self.speed)
            else:
                self.move_roaming_character(character, delta_x=0, delta_y=-self.speed)

    def move(self, delta_x, delta_y) -> None:
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

        if not self.is_impassable(self.next_tile):
            if not self.roaming_character_in_path_of_character():
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

    def roaming_character_in_path_of_character(self) -> bool:
        roaming_character_locations = [(roaming_character.column, roaming_character.row) for roaming_character in
                                       self.current_map.roaming_characters]
        return self.get_next_coordinates(self.hero_layout_column, self.hero_layout_row,
                                         self.current_map.player.direction) in roaming_character_locations

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
            return get_tile_by_coordinates(character_column, character_row - 1, self.current_map)
        elif direction == Direction.DOWN.value:
            return get_tile_by_coordinates(character_column, character_row + 1, self.current_map)
        elif direction == Direction.LEFT.value:
            return get_tile_by_coordinates(character_column - 1, character_row, self.current_map)
        elif direction == Direction.RIGHT.value:
            return get_tile_by_coordinates(character_column + 1, character_row, self.current_map)

    def get_next_coordinates(self, character_column: int, character_row: int, direction: int) -> tuple:
        if character_row < len(self.current_map.layout) and character_column < len(self.current_map.layout[0]):
            if direction == Direction.UP.value:
                return character_column, character_row - 1
            elif direction == Direction.DOWN.value:
                return character_column, character_row + 1,
            elif direction == Direction.LEFT.value:
                return character_column - 1, character_row
            elif direction == Direction.RIGHT.value:
                return character_column + 1, character_row

    def is_impassable(self, tile: str) -> bool:
        """
        Check if a tile is impassable (a tile that blocks the player from moving).
        :param tile: Tile to be checked for impassibility.
        :return: bool: A boolean value stating whether or not the tile is impassable.
        """
        return tile in self.current_map.impassable_tiles

    def handle_sides_collision(self, next_pos_x: int, next_pos_y: int) -> tuple:
        """
        Handle collision with the sides of the map (for the player).
        :type next_pos_x: int
        :type next_pos_y: int
        :param next_pos_x: Next x position (in terms of tile size).
        :param next_pos_y: Next y position (in terms of tile size).
        :return: tuple: The x, y coordinates (in terms of tile size) of the next position of the player.
        """
        max_x_bound, max_y_bound, min_bound = self.current_map.width - TILE_SIZE, self.current_map.height - TILE_SIZE, 0
        if self.current_map.player.rect.x < min_bound:
            self.current_map.player.rect.x = min_bound
            play_sound(bump_sfx)
            next_pos_x += -self.speed
        elif self.current_map.player.rect.x > max_x_bound:
            self.current_map.player.rect.x = max_x_bound
            play_sound(bump_sfx)
            next_pos_x += self.speed
        elif self.current_map.player.rect.y < min_bound:
            self.current_map.player.rect.y = min_bound
            play_sound(bump_sfx)
            next_pos_y -= self.speed
        elif self.current_map.player.rect.y > max_y_bound:
            self.current_map.player.rect.y = max_y_bound
            play_sound(bump_sfx)
            next_pos_y += self.speed
        return next_pos_x, next_pos_y

    def move_roaming_characters(self) -> None:
        """
        Move all roaming characters in the current map.
        :return: None
        """
        # TODO: Extend roaming characters beyond just the roaming guard.
        for roaming_character in self.current_map.roaming_characters:
            get_character_position(roaming_character)
            now = get_ticks()
            if roaming_character.last_roaming_clock_check is None:
                roaming_character.last_roaming_clock_check = now
            if now - roaming_character.last_roaming_clock_check >= self.roaming_character_go_cooldown:
                roaming_character.last_roaming_clock_check = now
                if not roaming_character.is_moving:
                    roaming_character.direction = random.choice(list(map(int, Direction)))
                else:  # character not moving and no input
                    return
                roaming_character.is_moving = True
            else:  # determine if character has reached new tile
                if is_facing_medially(roaming_character):
                    if roaming_character.rect.y % TILE_SIZE == 0:
                        roaming_character.is_moving, roaming_character.next_tile_checked = False, False
                        return
                elif is_facing_laterally(roaming_character):
                    if roaming_character.rect.x % TILE_SIZE == 0:
                        roaming_character.is_moving, roaming_character.next_tile_checked = False, False
                        return
            if is_facing_medially(roaming_character):
                self.move_medially(roaming_character)
            elif is_facing_laterally(roaming_character):
                self.move_laterally(roaming_character)
            else:
                print("Invalid direction.")
            handle_roaming_character_sides_collision(self.current_map, roaming_character)

    def move_roaming_character(self, roaming_character, delta_x, delta_y) -> None:
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
