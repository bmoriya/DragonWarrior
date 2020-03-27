from src.animated_sprite import AnimatedSprite
from src.common import Direction


class Player(AnimatedSprite):

    def __init__(self, center_point, down_images, left_images, up_images, right_images, direction=Direction.DOWN.value):
        AnimatedSprite.__init__(self, center_point, direction, down_images, left_images, up_images, right_images)
        self.index = 0

    def set_center_point(self, center_point):
        self.center_point = center_point

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
