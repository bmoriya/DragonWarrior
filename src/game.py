from os import pardir
from os.path import join
from pygame import init, error, Surface
from pygame.display import set_mode, set_caption, flip
from pygame.image import load
from pygame.sprite import Group
from pygame.transform import scale

from base_sprite import BaseSprite
#from tantagel_throne_room import TantagelThroneRoom
from maps import tantagel_throne_room

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
    
    #Size for the game's sprites in pixels
    TILE_SIZE = 16 * SCALE

    GAME_NAME = "Dragon Warrior"
    
    #Colors
    BLACK = (0, 0, 0)

    #Index values for the map tiles corresponding to location on tilesheet.
    ROOF = 0
    WALL = 1
    WOOD = 2
    BRICK = 3
    CHEST = 4
    DOOR = 5
    BRICK_STAIRDN = 6
    BRICK_STAIRUP = 7
    BARRIER = 8
    WEAPON_SIGN = 9
    INN_SIGN = 10
    CASTLE = 11
    TOWN = 12
    GRASS = 13
    TREES = 14
    HILLS = 15
    MOUNTAINS = 16
    CAVE = 17
    GRASS_STAIRDN = 18
    SAND = 19
    MARSH = 20
    BRIDGE = 21
    WATER = 22
    BOTTOM_COAST = 23
    BOTTOM_LEFT_COAST = 24
    LEFT_COAST = 25
    TOP_LEFT_COAST = 26
    TOP_COAST = 27
    TOP_RIGHT_COAST = 28
    RIGHT_COAST = 29
    BOTTOM_RIGHT_COAST = 30
    BOTTOM_TOP_LEFT_COAST = 31
    BOTTOM_TOP_COAST = 32
    BOTTOM_TOP_RIGHT_COAST = 33
    
    
    def __init__(self):
        '''
        Initialize the game.
        '''
        init()
        self.screen = set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        set_caption(self.GAME_NAME)
        self.screen.fill(self.BLACK)

        #Load images from spritesheets and combine them into a sprite list.
        self.sprites = self.load_spritesheet(self.TILE_SHEET, width=16,
                                             height=16)
        self.sprites.extend(self.load_spritesheet(self.CHAR_SHEET, 
                                                  width=16, height=16))
        
    def main(self):
        '''
        Function that runs the game.
        '''
        
        #Keep for debugging. prints entire sprite sheets.
        for x, row in enumerate(self.sprites):
            for y, tile in enumerate(row):
                self.screen.blit(tile, (x*16*self.SCALE, y*16*self.SCALE))
#                print x, y
        
        self.roof_group = Group()
        '''
        self.wall_group = Group()
        self.wood_group = Group()
        self.brick_group = Group()
        self.chest_group = Group()
        self.door_group = Group()
        self.brick_stairdn_group = Group()
        self.brick_stairup_group = Group()
        self.barrier_group = Group()
        self.weapon_sign_group = Group()
        self.inn_sign_group = Group()
        self.castle_group = Group()
        self.current_map = TantagelThroneRoom()
        '''
        self.load_map(tantagel_throne_room)
        
        bigmap_width = 24 * self.TILE_SIZE
        bigmap_height = 23 * self.TILE_SIZE
        self.bigmap = Surface((bigmap_width, bigmap_height))
        self.bigmap.fill(self.BLACK)
        
        self.roof_group.draw(self.bigmap)
        '''
        self.wall_group.draw(self.bigmap)
        self.wood_group.draw(self.bigmap)
        self.brick_group.draw(self.bigmap)
        self.chest_group.draw(self.bigmap)
        self.door_group.draw(self.bigmap)
        self.brick_stairdn_group.draw(self.bigmap)
        '''
        self.bigmap.convert()
        
        self.background = Surface(self.screen.get_size())
        self.background = self.bigmap.subsurface(0, 0, self.WIN_WIDTH, 
                                                 self.WIN_HEIGHT)
        self.background.convert()
        self.screen.blit(self.background, (0, 0))
        
        flip()

    def load_map(self, current_map):
        x_offset = self.TILE_SIZE / 2
        y_offset = self.TILE_SIZE / 2

        for y in range (len(current_map)):
            for x in range(len(current_map[y])):
                center_pt = [(x * self.TILE_SIZE) + x_offset,
                             (y * self.TILE_SIZE) + y_offset]
                print x, y
                
                if current_map[y][x] == self.ROOF:
                    roof = BaseSprite(center_pt, self.sprites[self.ROOF][0])
                    self.roof_group.add(roof)
                elif current_map[y][x] == self.WALL:
                    wall = BaseSprite(center_pt, self.sprites[self.WALL][1])
                    self.wall_group.add(wall)
                '''
                elif current_map[y][x] == self.WOOD:
                    wood = BaseSprite(center_pt, self.sprites[self.WOOD])
                    self.wood_group.add(wood)
                elif current_map[y][x] == self.BRICK:
                    brick = BaseSprite(center_pt, self.sprites[self.BRICK])
                    self.brick_group.add(brick)
                elif current_map[y][x] == self.CHEST:
                    chest = BaseSprite(center_pt, self.sprites[self.CHEST])
                    self.chest_group.add(chest)
                elif current_map[y][x] == self.DOOR:
                    door = BaseSprite(center_pt, self.sprites[self.DOOR])
                    self.door_group.add(door)
                elif current_map[y][x] == self.BRICK_STAIRDN:
                    brick_stairdn = BaseSprite(center_pt, 
                                               self.sprites[
                            self.BRICK_STAIRDN])
                    self.brick_stairdn_group.add(brick_stairdn)
                '''

    def load_spritesheet(self, filename, width, height, colorkey=None):
        '''
        Loads spritesheet and slices into images of given width and height.

        Returns:
        a list of lists containing the sliced images. First index 
        value would correspond to the row number and the second would be
        column the sprite is found in on the physical sheet.
        '''
        try:
            image = load(filename).convert()
            image = scale(image, (image.get_width() * self.SCALE,
                          image.get_height() * self.SCALE))
        except error, e:
            print e
            return
        image_width, image_height = image.get_size()
        width = self.TILE_SIZE
        height = self.TILE_SIZE
        tile_table = []
        
        for x in range(0, image_width / width):
            row = []
            tile_table.append(row)
            for y in range(0, image_height / height):
                rect = (x * width, y * height, width, height)
                row.append(image.subsurface(rect))
        return tile_table


if __name__ == "__main__":
    game = Game()
    game.main()
