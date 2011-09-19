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
    UNARMED_HERO_PATH = join(DATA_DIR, 'unarmed_hero.png')
    TILE_SIZE = 16 * SCALE
    COLORKEY = (0, 128, 128)
    
    def __init__(self):
        #Initialize pygame
        init()
        
        #Create the game window.
        self.screen = set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        set_caption(self.GAME_TITLE)
        
        self.load_images()
        

    def load_images(self):
        '''
        Load all the images for the game graphics.
        '''
        try:
            #Load the map tile spritesheet
            map_tilesheet = load(self.MAP_TILES_PATH).convert()
            
            #Load unarmed hero images
            unarmed_herosheet = load(self.UNARMED_HERO_PATH)
            
        except error, e:
            print e
            return
        
        #Parse map tilesheet for individual tiles
        width, height = map_tilesheet.get_size()
        map_tilesheet = scale(map_tilesheet, (width * self.SCALE, 
                                              height * self.SCALE))
        
        self.map_tiles = []
        for x in range(0, width / self.TILE_SIZE):
            row = []
            self.map_tiles.append(row)
            for y in range(0, height / self.TILE_SIZE):
                rect = (x * self.TILE_SIZE, y * self.TILE_SIZE, 
                        self.TILE_SIZE, self.TILE_SIZE)
                row.append(map_tilesheet.subsurface(rect))

        #Scale and handle transparency on hero images
        unarmed_herosheet.set_colorkey(self.COLORKEY)
        unarmed_herosheet.convert_alpha()
        unarmed_herosheet = scale(unarmed_herosheet, (width * self.SCALE, 
                                                      height * self.SCALE))
        width, height = unarmed_herosheet.get_size()
        for i in xrange(0, 8):
            print i
        
        

if __name__ == "__main__":
    game = Game()
