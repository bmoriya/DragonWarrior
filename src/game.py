# Brian Moriya
# brian.moriya@capturedbypenguins.com
from pygame import init, DOUBLEBUF, Surface, QUIT, KEYDOWN, K_ESCAPE
from pygame.display import set_caption, set_mode, flip
from pygame.event import get
from pygame.time import Clock

class Game(object):
    '''
    Generic class that Holds the game logic.
    '''

    def __init__(self, width=800, height=600, fps=30, title="", multiplier=1):
        '''
        
        Initializes pygame modules and sets up the screen, background and game 
        clock.
        '''
        init()
        set_caption(title)
        
        width *= multiplier
        height *= multiplier

        screen = set_mode((width, height), DOUBLEBUF)
        background = Surface(screen.get_size()).convert()
        clock = Clock()
        
        self.width = width
        self.height = height
        self.screen = screen
        self.background = background
        self.clock = clock
        self.fps = fps
        self.multiplier = multiplier

    def run(self):
        '''
        Runs the game.
        '''
        #Copy these members for efficiency.
        screen = self.screen
        background = self.background

        running = True
        while running:
            self.clock.tick(self.fps)
            running = self.event_loop()
            screen.blit(background, (0, 0))
            flip()

    def event_loop(self, is_running=True):
        '''
        Game events captured here.
        '''
        for event in get():
                if event.type == QUIT:
                    is_running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        is_running = False
        return is_running
