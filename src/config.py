from os.path import join, pardir
from win32api import GetSystemMetrics
from sys import platform

DATA_DIR = join(pardir, 'data')
IMAGES_DIR = join(DATA_DIR, 'images')
SOUND_DIR = join(DATA_DIR, 'sound')
MUSIC_DIR = join(SOUND_DIR, 'music')
SFX_DIR = join(SOUND_DIR, 'sfx')
DATA_DIR = join(pardir, 'data')
MAP_TILES_PATH = join(IMAGES_DIR, 'tileset.png')
UNARMED_HERO_PATH = join(IMAGES_DIR, 'unarmed_hero.png')
KING_LORIK_PATH = join(IMAGES_DIR, 'king_lorik.png')
RIGHT_GUARD_PATH = join(IMAGES_DIR, 'right_guard.png')
LEFT_GUARD_PATH = join(IMAGES_DIR, 'left_guard.png')
ROAMING_GUARD_PATH = join(IMAGES_DIR, 'roaming_guard.png')

TANTEGEL_CASTLE_THRONE_ROOM_MUSIC_PATH = join(MUSIC_DIR, '02_Dragon_Quest_1_-_Tantegel_Castle_(22khz_mono).ogg')

if platform == 'win32':
    CURRENT_SCREEN_RESOLUTION_WIDTH = GetSystemMetrics(0)
    CURRENT_SCREEN_RESOLUTION_HEIGHT = GetSystemMetrics(1)
    if CURRENT_SCREEN_RESOLUTION_WIDTH >= 1920 and CURRENT_SCREEN_RESOLUTION_HEIGHT <= 1080:
        SCALE = 3
    else:
        SCALE = 2
else:
    SCALE = 2
TILE_SIZE = 16 * SCALE
NES_RES = (256, 240)
WIN_WIDTH = NES_RES[0] * SCALE
WIN_HEIGHT = NES_RES[1] * SCALE
