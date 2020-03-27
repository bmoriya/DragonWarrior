from unittest import TestCase

import pygame
from pygame.imageext import load_extended
from pygame.transform import scale

from src.config import UNARMED_HERO_PATH, SCALE
from src.game import Game, get_initial_camera_position
from src.maps import DragonWarriorMap
from src.player import Player


def create_key_mock(pressed_key):
    def helper():
        tmp = [0] * 300
        tmp[pressed_key] = 1
        return tmp

    return helper


class TestMap(DragonWarriorMap):
    def __init__(self):
        super().__init__()
        self.layout = [[34, 0],
                       [1, 2]]


class TestGame(TestCase):

    def setUp(self) -> None:
        self.game = Game()
        self.game.camera_pos = 0, 0
        self.center_pt = 0, 0
        self.game.current_map = TestMap()
        self.initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
        unarmed_hero_sheet = load_extended(UNARMED_HERO_PATH)
        unarmed_hero_sheet = scale(unarmed_hero_sheet,
                                   (unarmed_hero_sheet.get_width() * SCALE, unarmed_hero_sheet.get_height() * SCALE))
        self.hero_images = self.game.parse_animated_spritesheet(unarmed_hero_sheet, is_roaming=True)
        self.game.current_map.player = Player(center_point=self.center_pt,
                                              down_img=self.hero_images[0],
                                              left_img=self.hero_images[1],
                                              up_img=self.hero_images[2],
                                              right_img=self.hero_images[3])
        self.game.hero_layout_x_pos = 0
        self.game.hero_layout_y_pos = 0
        pygame.key.get_pressed = create_key_mock(pygame.K_RIGHT)
        pygame.key.get_pressed = create_key_mock(pygame.K_UP)
        pygame.key.get_pressed = create_key_mock(pygame.K_DOWN)
        pygame.key.get_pressed = create_key_mock(pygame.K_LEFT)

    def test_get_initial_camera_position(self):
        initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
        self.assertEqual(get_initial_camera_position(initial_hero_location), (0, 0))
        self.game.current_map.layout = [[1, 0],
                                        [34, 2]]
        initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
        self.assertEqual(get_initial_camera_position(initial_hero_location), (-16, 0))
        self.game.current_map.layout = [[1, 34],
                                        [0, 2]]
        initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
        self.assertEqual(get_initial_camera_position(initial_hero_location), (0, -7))
        self.game.current_map.layout = [[1, 0],
                                        [2, 34]]
        initial_hero_location = self.game.current_map.get_initial_character_location('HERO')
        self.assertEqual(get_initial_camera_position(initial_hero_location), (-16, -7))

    def test_move_player(self):
        key = pygame.key.get_pressed()
        self.assertEqual(self.game.move_player(key), None)

    def test_get_tile_by_coordinates(self):
        self.assertEqual(self.game.get_tile_by_coordinates(0, 0), 'HERO')
        self.assertEqual(self.game.get_tile_by_coordinates(0, 1), 'ROOF')
        self.assertEqual(self.game.get_tile_by_coordinates(1, 0), 'WALL')
        self.assertEqual(self.game.get_tile_by_coordinates(1, 1), 'WOOD')
