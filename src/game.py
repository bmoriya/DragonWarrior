from os import pardir
from os.path import join
from pygame import init, error, Surface, QUIT
from pygame.display import set_mode, set_caption, flip
from pygame.event import get
from pygame.image import load
from pygame.transform import scale
from pygame.time import Clock

from common import TILE_SIZE, SCALE
from animated_sprite import AnimatedSprite

class Game(object):
    NESRES = (256, 240)
    FPS = 60
    GAME_TITLE = "Dragon Warrior"
    WIN_WIDTH = NESRES[0] * SCALE
    WIN_HEIGHT = NESRES[1] * SCALE
    DATA_DIR = join(pardir, 'data')
    MAP_TILES_PATH = join(DATA_DIR, 'tileset.png')
    UNARMED_HERO_PATH = join(DATA_DIR, 'unarmed_hero.png')
    KING_LORIK_PATH = join(DATA_DIR, 'king_lorik.png')
    RIGHT_GUARD_PATH = join(DATA_DIR, 'right_guard.png')
    LEFT_GUARD_PATH = join(DATA_DIR, 'left_guard.png')
    ROAMING_GUARD_PATH = join(DATA_DIR, 'roaming_guard.png')
    COLORKEY = (0, 128, 128)
    
    def __init__(self):
        #Initialize pygame
        init()
        
        #Create the game window.
        self.screen = set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        set_caption(self.GAME_TITLE)
        self.clock = Clock()
        self.load_images()
        
    def main(self):
        self.background = Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255))
        
        while True:
            self.clock.tick(self.FPS)
            for event in get():
                if event.type == QUIT:
                    return
            self.player.animate(self.background)
            self.screen.blit(self.background, (0, 0))
            flip()

    def load_images(self):
        '''
        Load all the images for the game graphics.
        '''
        try:
            #Load the map tile spritesheet
            map_tilesheet = load(self.MAP_TILES_PATH).convert()
            
            #Load unarmed hero images
            unarmed_herosheet = load(self.UNARMED_HERO_PATH)

            #Load King Lorik images
            king_lorik_sheet = load(self.KING_LORIK_PATH)

            #Guard images.
            right_guard_sheet = load(self.RIGHT_GUARD_PATH)
            left_guard_sheet = load(self.LEFT_GUARD_PATH)
            roaming_guard_sheet = load(self.ROAMING_GUARD_PATH)
            
        except error, e:
            print e
            return
        
        #Parse map tilesheet for individual tiles
        width, height = map_tilesheet.get_size()
        map_tilesheet = scale(map_tilesheet, (width * SCALE, height * SCALE))
        
        self.map_tiles = []
        for x in range(0, width / TILE_SIZE):
            row = []
            self.map_tiles.append(row)
            for y in range(0, height / TILE_SIZE):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                row.append(map_tilesheet.subsurface(rect))

        #Get the images for the initial hero sprites
        down_img, left_img, up_img, right_img = \
            self.parse_animated_spritesheet(
            unarmed_herosheet, is_roaming=True)
            
        self.player = AnimatedSprite((TILE_SIZE/2, TILE_SIZE/2), down_img, 
                                     left_img, up_img, right_img)

        #Get images for the King
        self.parse_animated_spritesheet(king_lorik_sheet, is_roaming=False)

    def parse_animated_spritesheet(self, sheet, is_roaming=True):
        '''
        Parses spritesheets and creates image lists. If is_roaming is True 
        the sprite will have four lists of images, one for each direction. If
        is_roaming is False then there will be one list of 2 images.
        
        If is_roaming is false make sure to only use the first returned list.
        '''
        sheet.set_colorkey(self.COLORKEY)
        sheet.convert_alpha()
        width, height = sheet.get_size()
        sheet = scale(sheet, (width * SCALE, height * SCALE))
        
        facing_down = []
        facing_left = []
        facing_up = []
        facing_right = []
        
        for i in xrange(0, 2):
            
            rect = (i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
            facing_down.append(sheet.subsurface(rect))
            
            if is_roaming == True:
                rect = ((i + 2) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE) 
                facing_left.append(sheet.subsurface(rect))
                
                rect = ((i + 4) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
                facing_up.append(sheet.subsurface(rect))
                
                rect = ((i + 6) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
                facing_right.append(sheet.subsurface(rect))
                
        return facing_down, facing_left, facing_up, facing_right
    


if __name__ == "__main__":
    game = Game()
    game.main()
