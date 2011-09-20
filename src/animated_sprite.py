from common import TILE_SIZE, BACK_FILL_COLOR
from base_sprite import BaseSprite

class AnimatedSprite(BaseSprite):
    
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

    def __init__(self, center_point, down_img, left_img, up_img, right_img):
        BaseSprite.__init__(self, center_point, down_img[0])

        self.current_frame = 0
        self.max_frame = 1
        self.frame_count = 0
        self.frame_delay = 12
        
        self.down_images = down_img
        self.left_images = left_img
        self.up_images = up_img
        self.right_images = right_img
        self.direction = self.RIGHT
        self.center_point = center_point

    def update(self, key, surface):
        pass
        
    def animate(self, surface):
        self.frame_count += 1
        if self.frame_count > self.frame_delay:
            self.frame_count = 0
            self.current_frame += 1

            if self.current_frame > self.max_frame:
                self.current_frame = 0
        
        if self.direction == self.DOWN:
            surface.fill(BACK_FILL_COLOR, self.rect)
            surface.blit(self.down_images[self.current_frame], 
                         (self.rect[0], self.rect[1]))
        elif self.direction == self.LEFT:
            surface.fill(BACK_FILL_COLOR, self.rect)
            surface.blit(self.left_images[self.current_frame],
                         (self.rect[0], self.rect[1]))
        elif self.direction == self.UP:
            surface.fill(BACK_FILL_COLOR, self.rect)
            surface.blit(self.up_images[self.current_frame], 
                         (self.rect[0], self.rect[1]))
        elif self.direction == self.RIGHT:
            surface.fill(BACK_FILL_COLOR, self.rect)
            surface.blit(self.right_images[self.current_frame],
                         (self.rect[0], self.rect[1]))

