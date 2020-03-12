# Constants
from enum import Enum

SCALE = 2
TILE_SIZE = 16 * SCALE


class Direction(Enum):
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3
