# Constants
from enum import IntEnum
from os.path import join, sep

import pygame

from src.config import SFX_DIR, SOUND_ENABLED, MUSIC_ENABLED, MUSIC_DIR, IMAGES_DIR, FONTS_DIR


class Direction(IntEnum):
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3


_sound_library = {}
bump_sfx = join(SFX_DIR, '42 Dragon Quest 1 - Bumping into Walls (22khz mono).wav')
menu_button_sfx = join(SFX_DIR, '32 Dragon Quest 1 - Menu Button (22khz mono).wav')
stairs_down_sfx = join(SFX_DIR, '30 Dragon Quest 1 - Stairs Down (22khz mono).wav')
stairs_up_sfx = join(SFX_DIR, '29 Dragon Quest 1 - Stairs Up (22khz mono).wav')


def play_sound(path='data/sound/sfx'):
    if SOUND_ENABLED:
        global _sound_library
        sound = _sound_library.get(path)
        if sound is None:
            canonicalized_path = path.replace('/', sep).replace('\\', sep)
            sound = pygame.mixer.Sound(canonicalized_path)
            _sound_library[path] = sound
        sound.play()


_music_library = {}
tantegel_castle_throne_room_music = join(MUSIC_DIR, '02 Dragon Quest 1 - Tantegel Castle (22khz_mono).ogg')
tantegel_castle_courtyard_music = join(MUSIC_DIR, '03 Dragon Quest 1 - Tantegel Castle (Lower) (22khz mono).ogg')
village_music = join(MUSIC_DIR, '04 Dragon Quest 1 - Peaceful Village (22khz mono).ogg')
overworld_music = join(MUSIC_DIR, '05 Dragon Quest 1 - Kingdom of Alefgard (22khz mono).ogg')


def play_music(path='data/sound/music'):
    if MUSIC_ENABLED:
        global _music_library
        music = _music_library.get(path)
        if music is None:
            canonicalized_path = path.replace('/', sep).replace('\\', sep)
            music = pygame.mixer.Sound(canonicalized_path)
            _music_library[path] = music
        music.play(-1)


_image_library = {}
MAP_TILES_PATH = join(IMAGES_DIR, 'tileset.png')
UNARMED_HERO_PATH = join(IMAGES_DIR, 'unarmed_hero.png')
KING_LORIK_PATH = join(IMAGES_DIR, 'king_lorik.png')
GUARD_PATH = join(IMAGES_DIR, 'guard.png')
MAN_PATH = join(IMAGES_DIR, 'man.png')
WOMAN_PATH = join(IMAGES_DIR, 'woman.png')
WISE_MAN_PATH = join(IMAGES_DIR, 'wise_man.png')
SOLDIER_PATH = join(IMAGES_DIR, 'soldier.png')
MERCHANT_PATH = join(IMAGES_DIR, 'merchant.png')
PRINCESS_GWAELIN_PATH = join(IMAGES_DIR, 'princess_gwaelin.png')
DRAGONLORD_PATH = join(IMAGES_DIR, 'dragonlord.png')


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', sep).replace('\\', sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


pygame.font.init()
DRAGON_QUEST_FONT_PATH = join(FONTS_DIR, 'dragon-quest.ttf')
DRAGON_QUEST_FONT = pygame.font.Font(DRAGON_QUEST_FONT_PATH, 15)
