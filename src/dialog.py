'''
Created on Sep 13, 2011

@author: Brian Moriya
'''
from pygame import Surface, RLEACCEL
from pygame.draw import polygon, rect
from config import GAME_FONT, GAME_FONT_SIZE, WHITE, BLACK
from base_menu import BaseMenu

def arrow_image(color):
    '''
    Draws an arrow for using as a cursor in dialog menus.
    '''
    img = Surface((7, 6))
    img.fill((226, 59, 252))
    img.set_colorkey((226, 59, 252), RLEACCEL)
    polygon(img, color, ((0, 0), (3, 3), (6, 0)))
    return img

class Menu(BaseMenu):
    '''
    Menu that allows user to select from a list of options. Automatically sizes
    itself to fit the options it's displaying, based on the font size.
    '''
    
    def __init__(self, options):
        BaseMenu.__init__(self, GAME_FONT, GAME_FONT_SIZE)
        self.options = options
        self.current_option = 0
        self.height = (len(self.options) + 1) * self.font.get_height()
        
    def draw_menu(self, surface, position):
        '''
        Draws the menu on a given surface at the specified position. Position 
        should be a coordinate pair.
        '''
        self.position = position
        y = position[1]
        
        for i, option in enumerate(self.options):
            if i == self.current_option:
                icon = "> "
            else:
                icon = "  "
            
            text = self.font.render(icon + option, 1, WHITE)
            
            self.textpos = text.get_rect()
            self.textpos.centerx = position[0]
            self.textpos.centery = y
        
            surface.blit(text, (self.textpos))
            y += text.get_height() + 3
            i += 1
    
    def move_cursor(self, surface, direction):
        if direction > 0:
            if self.current_option < len(self.options) - 1:
                self.current_option += 1
        
        elif direction < 0:
            if self.current_option > 0:
                self.current_option -= 1
        
        surface.fill(BLACK)
        self.draw_menu(surface, self.position)
        
    def get_current_option(self):
        return self.current_option, self.options[self.current_option]
    
    