from src.animated_sprite import AnimatedSprite
from src.common import Direction


class Player(AnimatedSprite):

    def __init__(self, center_point, direction, down_images=None):
        AnimatedSprite.__init__(center_point, direction, None)
        self.index = 0

    def set_center_point(self, center_point):
        self.center_point = center_point

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
