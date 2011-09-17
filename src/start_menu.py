'''
Created on Sep 13, 2011

@author: deadguy
'''
from pygame import QUIT, KEYDOWN, quit
from pygame.display import flip 
from pygame.font import Font
from pygame.event import get
from pygame.transform import scale
from pygame.time import Clock

from config import GAME_FONT, SCALE, WHITE, ORIGIN, FPS, START
from util import load_png
from base_menu import BaseMenu


class StartMenu(BaseMenu):
    '''
    The start menu is displayed when the game starts running.
    '''
    FONT_SIZE = 12
    START_PROMPT = "Push Start"
    TITLE_IMAGE = "title_menu.png"
    
    def __init__(self):
        BaseMenu.__init__(self, GAME_FONT, self.FONT_SIZE * SCALE)
        self.clock = Clock()
        
    def draw_menu(self, surface, position):
        
        #Push start text
        text = self.font.render(self.START_PROMPT, 1, WHITE)
        
        #Calculate placement of text on screen
        textpos = text.get_rect()
        textpos.centerx = position[0]
        textpos.centery = position[1]
        
        #Load game logo
        logo_image, rect = load_png(self.TITLE_IMAGE)
        
        #scale logo to fit screen size
        logo_image = scale(logo_image, (surface.get_width(), 
                                        surface.get_height() / 2))
        
        #Draw image and text on start screen.
        surface.blit(logo_image, ORIGIN)
        surface.blit(text, textpos)
        
        scale(surface, (surface.get_width() * SCALE, 
                           surface.get_height() * SCALE))
    
    def handle_input(self, screen, surface):
        '''
        Handle the start menu events.
        '''
        running = True
        while running:
            self.clock.tick(FPS)
        
            for event in get():
                if event.type == QUIT:
                    running = False
                    quit()
                if event.type == KEYDOWN:
                    if event.key == START:
                        running = False
                        
            screen.blit(surface, ORIGIN)
            flip()
            