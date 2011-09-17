from os.path import join, pardir
from pygame.image import load
from pygame import error, RLEACCEL

class BaseMap(object):
    
    def __init__(self, wall_size):
        WALL_SIZE = wall_size
        self.ROOF = 0
        self.WALL = 1
        self.WOOD = 2
        self.BRICK = 3
        self.CHEST = 4
        self.DOOR = 5
        self.BRICK_STAIRDN = 6
        self.BRICK_STAIRUP = 7
        self.BARRIER = 8
        self.WEAPON_SIGN = 9
        self.INN_SIGN = 10
        self.CASTLE = 11
        self.TOWN = 12
        self.GRASS = 13
        self.TREES = 14
        self.HILLS = 15
        self.MOUNTAINS = 16
        self.CAVE = 17
        self.GRASS_STAIRDN = 18
        self.SAND = 19
        self.MARSH = 20
        self.BRIDGE = 21
        self.WATER = 22
        self.BOTTOM_COAST = 23
        self.BOTTOM_LEFT_COAST = 24
        self.LEFT_COAST = 25
        self.TOP_LEFT_COAST = 26
        self.TOP_COAST = 27
        self.TOP_RIGHT_COAST = 28
        self.RIGHT_COAST = 29
        self.BOTTOM_RIGHT_COAST = 30
        self.BOTTOM_TOP_LEFT_COAST = 31
        self.BOTTOM_TOP_COAST = 32
        self.BOTTOM_TOP_RIGHT_COAST = 33
        
    def getLayout(self):
        """Get the Layout of the level"""
        """Returns a [][] list"""
        pass
    
    def getImages(self):
        """Get a list of all the images used by the level"""
        """Returns a list of all the images used.  The indices 
        in the layout refer to sprites in the list returned by
        this function"""
        pass
    