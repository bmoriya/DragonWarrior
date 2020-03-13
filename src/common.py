# Constants
from enum import Enum
from os.path import join, pardir

SCALE = 3
TILE_SIZE = 16 * SCALE
NES_RES = (256, 240)
WIN_WIDTH = NES_RES[0] * SCALE
WIN_HEIGHT = NES_RES[1] * SCALE

DATA_DIR = join(pardir, 'data')
IMAGES_DIR = join(DATA_DIR, 'images')
SOUND_DIR = join(DATA_DIR, 'sound')
MUSIC_DIR = join(SOUND_DIR, 'music')
SFX_DIR = join(SOUND_DIR, 'sfx')


class Direction(Enum):
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3
