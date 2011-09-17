'''
Created on Sep 13, 2011

@author: deadguy
'''
from pygame.font import Font
from pygame.time import Clock
from config import GAME_FONT_SIZE

class BaseMenu(object):
    '''
    classdocs
    '''

    def __init__(self, font, font_size=GAME_FONT_SIZE):
        self.clock = Clock()
        self.font = Font(font, font_size)
        
    def draw_menu(self, surface, position):
        '''
        Override this method.
        '''
        pass
    
    def handle_input(self, screen, surface):
        pass