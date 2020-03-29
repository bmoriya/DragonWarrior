from unittest import TestCase

import pygame
from pygame.imageext import load_extended
from pygame.transform import scale

from src.camera import get_initial_camera_position, Camera
from src.common import UNARMED_HERO_PATH, Direction
from src.config import SCALE
from src.game import Game
from src.maps import DragonWarriorMap, parse_animated_spritesheet
from src.player import Player


def create_key_mock(pressed_key):
    def helper():
        tmp = [0] * 300
        tmp[pressed_key] = 1
        return tmp

    return helper


class TestMap(DragonWarriorMap):
    def __init__(self, map_tiles, hero_images, guard_images):
        super().__init__(None, None, )
        self.layout = [[34, 0],
                       [1, 2]]


class TestGame(TestCase):

    def setUp(self) -> None:
        self.game = Game()
        self.game.camera_pos = 0, 0
        self.center_pt = 0, 0
        self.game.current_map = TestMap(None, None, )
        self.initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
        unarmed_hero_sheet = load_extended(UNARMED_HERO_PATH)
        unarmed_hero_sheet = scale(unarmed_hero_sheet,
                                   (unarmed_hero_sheet.get_width() * SCALE, unarmed_hero_sheet.get_height() * SCALE))
        self.hero_images = parse_animated_spritesheet(unarmed_hero_sheet, is_roaming=True)
        self.game.current_map.player = Player(center_point=self.center_pt,
                                              down_images=self.hero_images[Direction.DOWN.value],
                                              left_images=self.hero_images[Direction.LEFT.value],
                                              up_images=self.hero_images[Direction.UP.value],
                                              right_images=self.hero_images[Direction.RIGHT.value])
        self.game.hero_row = 0
        self.game.hero_column = 0
        pygame.key.get_pressed = create_key_mock(pygame.K_RIGHT)
        pygame.key.get_pressed = create_key_mock(pygame.K_UP)
        pygame.key.get_pressed = create_key_mock(pygame.K_DOWN)
        pygame.key.get_pressed = create_key_mock(pygame.K_LEFT)

    def test_get_initial_camera_position(self):
        initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
        self.assertEqual(Camera.set_camera_position(initial_hero_location), (0, 0))
        self.game.current_map.layout = [[1, 0],
                                        [34, 2]]
        initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
        self.assertEqual(Camera.set_camera_position(initial_hero_location), (-16, 0))
        self.game.current_map.layout = [[1, 34],
                                        [0, 2]]
        initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
        self.assertEqual(Camera.set_camera_position(initial_hero_location), (0, -7))
        self.game.current_map.layout = [[1, 0],
                                        [2, 34]]
        initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
        self.assertEqual(Camera.set_camera_position(initial_hero_location), (-16, -7))

    def test_move_player_return_value(self):
        key = pygame.key.get_pressed()
        self.assertEqual(self.game.move_player(key), None)

    def test_get_tile_by_coordinates(self):
        self.assertEqual(self.game.get_tile_by_coordinates(0, 0), 'HERO')
        self.assertEqual(self.game.get_tile_by_coordinates(1, 0), 'ROOF')
        self.assertEqual(self.game.get_tile_by_coordinates(0, 1), 'WALL')
        self.assertEqual(self.game.get_tile_by_coordinates(1, 1), 'WOOD')

    # TODO: implement test_handle_roaming_character_map_edge_side_collision.

    # def test_handle_roaming_character_map_edge_side_collision(self):
    #     initial_roaming_guard_position = self.game.current_map.get_initial_character_location('ROAMING_GUARD')
    #     self.game.current_map.layout = [[3, 1, 3],
    #                                     [1, 38, 1],
    #                                     [34, 1, 3]]
    #     self.roaming_guard = AnimatedSprite(self.center_pt, 0,
    #                                         self.roaming_guard_images[0], name='ROAMING_GUARD')
    #     self.game.current_map.roaming_characters.append(self.roaming_guard)
    #     self.game.move_roaming_characters()
    #     self.assertEqual(initial_roaming_guard_position, )  # current roaming guard position)
