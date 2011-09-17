from base_map import BaseMap
from main import terrain_tiles, char_tiles
from config import SCALE

class TantagelCastleMap(BaseMap):
    
    def __init__(self):
        
        BaseMap.__init__(self, wall_size=16 * SCALE)
        self.ROOF = 0
        self.HERO = 1
        self.WALL = 2
        self.BRICK = 3
        self.WOOD = 4
        self.DOOR = 5
        self.CHEST = 6
        self.STAIRDOWN = 7
        self.KING_LORIK = 8
        self.GUARD1 = 9
        self.GUARD2 = 10
        self.GUARD3 = 11
        
    def getLayout(self):
        return [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 2, 3, 3, 1, 3, 3, 6, 3, 3, 2, 0, 0, 0],
                [0, 0, 0, 2, 3, 4, 4, 4, 4, 4, 4, 3, 2, 0, 0, 0],
                [0, 0, 0, 2, 3, 4, 8, 4, 4, 3, 4, 3, 2, 0, 0, 0],
                [0, 0, 0, 2, 3, 3, 3, 6, 6, 3,11, 3, 2, 0, 0, 0],
                [0, 0, 0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 0, 0, 0],
                [0, 0, 0, 2, 3, 3, 9, 3,10, 3, 3, 3, 2, 0, 0, 0],
                [0, 0, 0, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 2, 3, 3, 3, 3, 3, 3, 3, 7, 2, 0, 0, 0],
                [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]
        
    def getSprites(self):
        global terrain_tiles, char_tiles
        
        roof = terrain_tiles[0][0]
        wall = terrain_tiles[0][1]
        hero = char_tiles[0][0]
        brick = terrain_tiles[0][3]
        wood = terrain_tiles[0][2]
        door = terrain_tiles[0][5]
        chest = terrain_tiles[0][4]
        stairdown = terrain_tiles[0][6] 
        king_lorik = char_tiles[5][0]
        
        return [roof, hero, wall, brick, wood, door, chest, stairdown, 
                king_lorik]