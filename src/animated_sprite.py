from pygame import K_DOWN, K_LEFT, K_UP, K_RIGHT
from pygame.sprite import Sprite

from common import TILE_SIZE

class AnimatedSprite(Sprite):
    
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

    def __init__(self, down_img, left_img, up_img, right_img):
        Sprite.__init__(self)

        self.current_frame = 0
        self.max_frame = 1
        self.frame_count = 0
        self.frame_delay = 12
        self.x = 0
        self.y = 0
        self.rect = (self.x, self.y, self.x + TILE_SIZE, self.y + TILE_SIZE)
        self.down_images = down_img
        self.left_images = left_img
        self.up_images = up_img
        self.right_images = right_img
        self.direction = self.DOWN

    def update(self, key, surface):
        if key == K_DOWN:
            surface.blit(self.down_images[self.current_frame], 
                         (self.x, self.y))
        elif key == K_LEFT:
            surface.blit(self.left_images[self.current_frame],
                         (self.x, self.y))
        elif key == K_UP:
            surface.blit(self.up_images[self.current_frame], 
                         (self.x, self.y))
        elif key == K_RIGHT:
            surface.blit(self.right_images[self.current_frame],
                         (self.x, self.y))

    def animate(self, surface):
        self.frame_count += 1
        if self.frame_count > self.frame_delay:
            self.frame_count = 0
            self.current_frame += 1

            if self.current_frame > self.max_frame:
                self.current_frame = 0
        
        if self.direction == self.DOWN:
            surface.fill((255, 255,255), self.rect)
            surface.blit(self.down_images[self.current_frame], 
                         (self.x, self.y))
