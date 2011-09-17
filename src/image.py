'''
Created on Sep 14, 2011

@author: deadguy
'''
from pygame import error
from pygame.image import load

def load_spritesheet(filename, width, height, colorkey=None):
    try:
        tile_sheet = load(filename)
        if colorkey:
            tile_sheet.set_colorkey(colorkey)
            tile_sheet.convert_alpha()
        else:
            tile_sheet.convert()
    except error, e:
        print e
        return
    
    tile_sheet_width, tile_sheet_height = tile_sheet.get_size()
    tiles = []
    for tile_x in range(0, tile_sheet_width / width):
        row = []
        tiles.append(row)
        for tile_y in range(0, tile_sheet_height / height):
            rect = (tile_x * width, tile_y * height, width, height)
            row.append(tile_sheet.subsurface(rect))
    
    return tiles
