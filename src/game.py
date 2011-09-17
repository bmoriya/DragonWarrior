from os import pardir
from os.path import join
from pygame import init
from pygame.display import set_mode, set_caption, flip

class Game(object):
    '''
    Glue that holds the game together.
    '''
    #Native NES resolution
    NESRES = (256, 240)
    
    #Important directories and file paths
    DATA_DIR = join(pardir, "data")
    TILE_SHEET = join(DATA_DIR, "tileset.png")
    CHAR_SHEET = join(DATA_DIR, "char_tiles.png")

    #Scale for the native resolution, min value is 1.
    SCALE = 3
    
    #Size for the game window.
    WIN_WIDTH = NESRES[0] * SCALE
    WIN_HEIGHT = NESRES[1] * SCALE
    
    GAME_NAME = "Dragon Warrior"
    
    def __init__(self):
        '''
        Initialize the game.
        '''
        init()
        set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        set_caption(self.GAME_NAME)

    def main(self):
        '''
        Function that runs the game.
        '''
        pass


if __name__ == "__main__":
    game = Game()
    game.main()
