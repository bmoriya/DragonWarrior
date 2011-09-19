from os import pardir
from os.path import join
from pygame import init
from pygame.display import set_mode, set_caption, flip
from pygame.image import load

class Game(object):
    NESRES = (256, 240)
    SCALE = 3
    FPS = 60
    GAME_TITLE = "Dragon Warrior"
    WIN_WIDTH = NESRES[0] * SCALE
    WIN_HEIGHT = NESRES[1] * SCALE
    DATA_DIR = join(pardir, 'data')
    MAP_TILES_PATH = join(DATA_DIR, 'tileset.png')
    
    def __init__(self):
        #Initialize pygame
        init()
        
        #Create the game window.
        self.screen = set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        set_caption(self.GAME_TITLE)
        
        flip()

    def load_images(self):
        '''
        Load all the images for the game graphics.
        '''
        try:
            #Load the map tile spritesheet.
            map_tiles = load(self.MAP_TILES_PATH)
            
        except error, e:
            print e
            return
        

if __name__ == "__main__":
    game = Game()
