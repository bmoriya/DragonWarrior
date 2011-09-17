'''
Created on Sep 13, 2011

@author: Brian Moriya

Global variables and constants for configuring the game.
'''
from os import pardir
from os.path import join
from pygame import K_LEFT, K_UP, K_DOWN, K_RIGHT, K_z, K_x, K_SPACE, K_RETURN

#Native NES resolution
NESRES = (256, 240)

DATA_DIR = join(pardir, "data")
TILE_SHEET = join(DATA_DIR, "tileset.png")
CHAR_SHEET = join(DATA_DIR, "char_tiles.png")

#Frames per second
FPS = 60

#Scale for the native resolution, min value is 1.
SCALE = 3

#Size for the game window.
WIN_WIDTH = NESRES[0] * SCALE
WIN_HEIGHT = NESRES[1] * SCALE

#Files
GAME_FONT = "../data/Knigqst.ttf"
GAME_FONT_SIZE = 10 * SCALE

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Frequently used points
ORIGIN = (0, 0)

#Key aliases
UP = K_UP
DOWN = K_DOWN
LEFT = K_LEFT
RIGHT = K_RIGHT
A_BTN = K_z
B_BTN = K_x
SELECT = K_SPACE
START = K_RETURN

#Strings
GAME_NAME = "Dragon Warrior"
START_PROMPT = "Push Start"
QUEST_OPTIONS = ["Continue Saved Quest", "Begin New Quest", "Copy Quest", 
                 "Erase Quest"]