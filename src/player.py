from src.animated_sprite import AnimatedSprite


class Player(AnimatedSprite):

    def __init__(self, center_point, direction, down_img, left_img, up_img,
                 right_img):
        AnimatedSprite.__init__(self, center_point, direction, down_img,
                                left_img, up_img, right_img)
        self.index = 0

    def update(self, wall_group):
        pass
        #self.index += 1
        #if self.index >= len(self.image):
        #    self.index = 0
        #self.image = self.image[self.index]


    def set_center_point(self, center_point):
        self.center_point = center_point
