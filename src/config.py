from os.path import join

REPLIT_DATA_DIR = '../data'
DATA_DIR = '../data'
FONTS_DIR = join(DATA_DIR, 'fonts')
IMAGES_DIR = join(DATA_DIR, 'images')
SOUND_DIR = join(DATA_DIR, 'sound')

MUSIC_DIR = join(SOUND_DIR, 'music')
SFX_DIR = join(SOUND_DIR, 'sfx')

SCALE = 2
TILE_SIZE = 16 * SCALE
NES_RES = (256, 240)
WIN_WIDTH = NES_RES[0] * SCALE
WIN_HEIGHT = NES_RES[1] * SCALE
MUSIC_ENABLED = False
SOUND_ENABLED = True
FULLSCREEN_ENABLED = False
COLOR_KEY = (0, 128, 128)
