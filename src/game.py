from os import pardir
from os.path import join
from pygame import init, error, Surface, QUIT, KEYDOWN
from pygame.display import set_mode, set_caption, flip
from pygame.event import get
from pygame.image import load
from pygame.sprite import Group, RenderUpdates
from pygame.transform import scale
from pygame.time import Clock

from common import TILE_SIZE, SCALE, BACK_FILL_COLOR
from player import Player
from animated_sprite import AnimatedSprite
from base_sprite import BaseSprite
from maps import *

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
    SCROLL_STEP_X = 3
    SCROLL_STEP_Y = 3
    ORIGIN = (0, 0)
    cornerpoint = [0, 0]
    
    def __init__(self):
        #Initialize pygame
        init()
        
        #Create the game window.
        self.screen = set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        set_caption(self.GAME_TITLE)
        self.clock = Clock()
        self.load_images()
       
    def main(self):
        self.init_groups()
        self.current_map = tantagel_throne_room
        self.load_map()

        #Make the big scrollable map
        self.bigmap_width = len(self.current_map[0]) * TILE_SIZE
        self.bigmap_height = len(self.current_map) * TILE_SIZE
        self.bigmap = Surface((self.bigmap_width, 
                               self.bigmap_height)).convert()
        self.bigmap.fill(BACK_FILL_COLOR)
        
        self.draw_sprites()

        self.background = Surface(self.screen.get_size()).convert()
        self.background.fill(BACK_FILL_COLOR)
        
        while True:
            self.player_sprites.clear(self.screen, self.background)
            self.king_lorik_sprites.clear(self.screen, self.background)

            self.clock.tick(self.FPS)
            for event in get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    pass
            
            self.background = self.bigmap.subsurface(self.cornerpoint[0],
                                                     self.cornerpoint[1],
                                                     self.WIN_WIDTH,
                                                     self.WIN_HEIGHT).convert()
            self.player.animate(self.background)
            self.player_sprites.draw(self.background)
            self.screen.blit(self.background, self.ORIGIN)
            flip()

    def draw_sprites(self):
        '''
        Draw static sprites on the big map.
        '''
        self.roof_group.draw(self.bigmap)
        self.wall_group.draw(self.bigmap)
        self.wood_group.draw(self.bigmap)
        self.brick_group.draw(self.bigmap)
        self.chest_group.draw(self.bigmap)
        self.door_group.draw(self.bigmap)
        self.brick_stairdn_group.draw(self.bigmap)

    def load_map(self):
        x_offset = TILE_SIZE / 2
        y_offset = TILE_SIZE / 2

        for y in range (len(self.current_map)):
            for x in range(len(self.current_map[y])):
                center_pt = [(x * TILE_SIZE) + x_offset, 
                             (y * TILE_SIZE) + y_offset]
                if self.current_map[y][x] == ROOF:
                    roof = BaseSprite(center_pt, self.map_tiles[ROOF][0])
                    self.roof_group.add(roof)
                elif self.current_map[y][x] == WALL:
                    wall = BaseSprite(center_pt, self.map_tiles[WALL][0])
                    self.wall_group.add(wall)
                elif self.current_map[y][x] == WOOD:
                    wood = BaseSprite(center_pt, self.map_tiles[WOOD][0])
                    self.wood_group.add(wood)
                elif self.current_map[y][x] == BRICK:
                    brick = BaseSprite(center_pt, self.map_tiles[BRICK][0])
                    self.brick_group.add(brick)
                elif self.current_map[y][x] == CHEST:
                    chest = BaseSprite(center_pt, self.map_tiles[CHEST][0])
                    self.chest_group.add(chest)
                elif self.current_map[y][x] == DOOR:
                    door = BaseSprite(center_pt, self.map_tiles[DOOR][0])
                    self.door_group.add(door)
                elif self.current_map[y][x] == BRICK_STAIRDN:
                    brick_stairdn = BaseSprite(center_pt, self.map_tiles[
                            BRICK_STAIRDN][0])
                    self.brick_stairdn_group.add(brick_stairdn)
                elif self.current_map[y][x] == HERO:
                    self.player = Player(center_pt, 2, 
                                         self.hero_images[0], 
                                         self.hero_images[1], 
                                         self.hero_images[2], 
                                         self.hero_images[3])
                    brick = BaseSprite(center_pt, self.map_tiles[BRICK][0])
                    self.brick_group.add(brick)
                elif self.current_map[y][x] == KING_LORIK:
                    self.king_lorik = AnimatedSprite(center_pt, 0,
                                                     self.king_lorik_images[0])
                    brick = BaseSprite(center_pt, self.map_tiles[BRICK][0])
                    self.brick_group.add(brick)
        self.player_sprites = RenderUpdates(self.player)
            
    def init_groups(self):
        self.roof_group = Group()
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

    def load_images(self):
        '''
        Load all the images for the game graphics.
        '''
        try:
            #Load the map tile spritesheet
            map_tilesheet = load(self.MAP_TILES_PATH).convert()
            
            #Load unarmed hero images
            self.unarmed_herosheet = load(self.UNARMED_HERO_PATH)

            #Load King Lorik images
            self.king_lorik_sheet = load(self.KING_LORIK_PATH)

            #Guard images.
            right_guard_sheet = load(self.RIGHT_GUARD_PATH)
            left_guard_sheet = load(self.LEFT_GUARD_PATH)
            roaming_guard_sheet = load(self.ROAMING_GUARD_PATH)
            
        except error, e:
            print e
            return
        
        self.parse_map_tiles(map_tilesheet)

        #Get the images for the initial hero sprites
        self.hero_images = self.parse_animated_spritesheet(
            self.unarmed_herosheet, is_roaming=True)
            
        #Get images for the King
        self.king_lorik_images = self.parse_animated_spritesheet(
                            self.king_lorik_sheet, is_roaming=False)

    def parse_map_tiles(self, map_tilesheet):
        #Parse map tilesheet for individual tiles
        map_tilesheet = scale(map_tilesheet, 
                              (map_tilesheet.get_width() * SCALE, 
                               map_tilesheet.get_height() * SCALE))
        
        width, height = map_tilesheet.get_size()
        
        self.map_tiles = []

        for x in range(0, width / TILE_SIZE):
            row = []
            self.map_tiles.append(row)

            for y in range(0, height / TILE_SIZE):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                row.append(map_tilesheet.subsurface(rect))

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
