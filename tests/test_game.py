from unittest import TestCase

import numpy as np
import pygame
from pygame.imageext import load_extended
from pygame.sprite import LayeredDirty
from pygame.transform import scale

from src.camera import Camera
from src.common import UNARMED_HERO_PATH, Direction
from src.config import SCALE, TILE_SIZE
from src.game import Game
from src.maps import DragonWarriorMap, parse_animated_spritesheet
from src.player import Player


def create_key_mock(pressed_key):
    def helper():
        tmp = [0] * 300
        tmp[pressed_key] = 1
        return tmp

    return helper


class TestMockMap(DragonWarriorMap):
    def __init__(self, hero_images):
        test_mock_map = [[33, 0],
                       [1, 2]]
        super().__init__(None, test_mock_map)

    def hero_underlying_tile(self):
        return 'BRICK'

    def hero_initial_direction(self):
        return Direction.DOWN.value()


class TestGame(TestCase):

    def setUp(self) -> None:
        self.game = Game()
        self.game.camera_pos = 0, 0
        self.center_pt = 0, 0
        # TODO: Fix camera edge case when using TestMockMap (smaller than + 8 and + 7).
        self.game.current_map = TestMockMap(hero_images=None)
        # self.game.current_map = TestMap(hero_images=None)

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
        self.game.current_map.player_sprites = LayeredDirty(self.game.current_map.player)
        self.game.hero_row = 0
        self.game.hero_column = 0
        self.hero_layout_column, self.hero_layout_row = self.game.current_map.player.rect.x // TILE_SIZE, self.game.current_map.player.rect.y // TILE_SIZE
        self.camera = Camera(hero_position=(int(self.hero_layout_column), int(self.hero_layout_row)),
                             current_map=self.game.current_map, speed=None)
        pygame.key.get_pressed = create_key_mock(pygame.K_RIGHT)
        pygame.key.get_pressed = create_key_mock(pygame.K_UP)
        pygame.key.get_pressed = create_key_mock(pygame.K_DOWN)
        pygame.key.get_pressed = create_key_mock(pygame.K_LEFT)

    # def test_get_initial_camera_position(self):
    #     initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
    #     self.camera.set_camera_position(initial_hero_location)
    #     self.assertEqual(0, self.camera.x)
    #     self.assertEqual(0, self.camera.y)

    def test_move_player_return_value(self):
        key = pygame.key.get_pressed()
        self.assertIsNone(self.game.move_player(key))

    def test_get_tile_by_coordinates(self):
        self.assertEqual('HERO', self.game.get_tile_by_coordinates(0, 0))
        self.assertEqual('ROOF', self.game.get_tile_by_coordinates(1, 0))
        self.assertEqual('WALL', self.game.get_tile_by_coordinates(0, 1))
        self.assertEqual('WOOD', self.game.get_tile_by_coordinates(1, 1))

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

    def test_get_next_coordinates(self):
        self.assertEqual((0, 1), self.game.get_next_coordinates(0, 0, Direction.DOWN.value))
        self.assertEqual((1, 0), self.game.get_next_coordinates(0, 0, Direction.RIGHT.value))

        self.assertEqual((1, 1), self.game.get_next_coordinates(1, 0, Direction.DOWN.value))
        self.assertEqual((0, 0), self.game.get_next_coordinates(1, 0, Direction.LEFT.value))

        self.assertEqual((0, 0), self.game.get_next_coordinates(0, 1, Direction.UP.value))
        self.assertEqual((1, 1), self.game.get_next_coordinates(0, 1, Direction.RIGHT.value))

        self.assertEqual((1, 0), self.game.get_next_coordinates(1, 1, Direction.UP.value))
        self.assertEqual((0, 1), self.game.get_next_coordinates(1, 1, Direction.LEFT.value))

    def test_unpause_all_movement(self):
        self.game.pause_all_movement()
        self.assertFalse(self.game.enable_animate)
        self.assertFalse(self.game.enable_roaming)
        self.assertFalse(self.game.enable_movement)
        self.game.unpause_all_movement()
        self.assertTrue(self.game.enable_animate)
        self.assertTrue(self.game.enable_roaming)
        self.assertTrue(self.game.enable_movement)
