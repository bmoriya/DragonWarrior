from src import maps
from src.animated_sprite import AnimatedSprite
from src.common import Direction


class Player(AnimatedSprite):

    def __init__(self, center_point, down_img, left_img, up_img, right_img, direction=Direction.DOWN.value):
        AnimatedSprite.__init__(self, center_point, direction, down_img,
                                left_img, up_img, right_img)
        self.index = 0

    def update(self, wall_group):
        pass
        # self.index += 1
        # if self.index >= len(self.image):
        #    self.index = 0
        # self.image = self.image[self.index]

    def set_center_point(self, center_point):
        self.center_point = center_point

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    @staticmethod
    def get_tile_by_value(position):
        return maps.tile_key_keys[maps.tile_key_values.index(position)]
