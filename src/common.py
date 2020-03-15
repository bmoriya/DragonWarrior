# Constants
from enum import Enum
from os.path import join, sep

import numpy as np
import pygame

from src import maps
from src.config import SFX_DIR


class Direction(Enum):
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3


_sound_library = {}
bump_sfx = join(SFX_DIR, '42 Dragon Quest 1 - Bumping into Walls (22khz mono).wav')


def play_sound(path='data/sound/sfx'):
    global _sound_library
    sound = _sound_library.get(path)
    if sound is None:
        canonicalized_path = path.replace('/', sep).replace('\\', sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    sound.play()


_image_library = {}


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', sep).replace('\\', sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


def get_initial_character_location(current_map_layout, character_name):
    layout_numpy_array = np.array(current_map_layout)
    hero_layout_position = np.asarray(np.where(layout_numpy_array == maps.tile_key[character_name])).T
    return hero_layout_position