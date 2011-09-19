from os import pardir
from os.path import join
from pygame import init, error
from pygame.display import set_mode, set_caption, flip
from pygame.image import load
from pygame.transform import scale

class Game(object):
    NESRES = (256, 240)
    SCALE = 3
    FPS = 60
    GAME_TITLE = "Dragon Warrior"
    WIN_WIDTH = NESRES[0] * SCALE
    WIN_HEIGHT = NESRES[1] * SCALE
    DATA_DIR = join(pardir, 'data')
    MAP_TILES_PATH = join(DATA_DIR, 'tileset.png')
    TILE_SIZE = 16 * SCALE
    
    def __init__(self):
        #Initialize pygame
        init()
        
        #Create the game window.
        self.screen = set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        set_caption(self.GAME_TITLE)
        
        self.load_images()
        
        flip()

    def load_images(self):
        '''
        Load all the images for the game graphics.
        '''
        try:
            #Load the map tile spritesheet.
            map_tilesheet = load(self.MAP_TILES_PATH).convert()
            
        except error, e:
            print e
            return
        
        width, height = map_tilesheet.get_size()
        map_tilesheet = scale(map_tilesheet, (width * self.SCALE, 
                                              height * self.SCALE))
        self.screen.blit(map_tilesheet, (0, 0))
        
        #Parse map tilesheet for individual tiles
        self.map_tiles = []
        for x in range(0, width / self.TILE_SIZE):
            row = []
            self.map_tiles.append(row)
            for y in range(0, height / self.TILE_SIZE):
                rect = (x * self.TILE_SIZE, y * self.TILE_SIZE, 
                        self.TILE_SIZE, self.TILE_SIZE)
                row.append(self.map_tiles.subsurface(rect))
        

if __name__ == "__main__":
    game = Game()
