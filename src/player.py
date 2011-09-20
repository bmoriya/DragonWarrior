from animated_sprite import AnimatedSprite
from common import TILE_SIZE

class Player(AnimatedSprite):
    
    def __init__(self, center_point, direction, down_img, left_img, up_img, 
                 right_img):
        AnimatedSprite.__init__(self, center_point, direction, down_img, 
                                left_img, up_img, right_img)

    def update(self, wall_group):
        pass
        
    def set_centerpoint(self, center_point):
        self.center_point = center_point
