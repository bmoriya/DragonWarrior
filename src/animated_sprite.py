from src.base_sprite import BaseSprite


class AnimatedSprite(BaseSprite):
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

    def __init__(self, center_point, direction,
                 down_img=None, left_img=None, up_img=None, right_img=None):
        BaseSprite.__init__(self, center_point, down_img[0])

        if right_img is None:
            right_img = []
        if up_img is None:
            up_img = []
        if left_img is None:
            left_img = []
        if down_img is None:
            down_img = []
        self.current_frame = 0
        self.max_frame = 1
        self.frame_count = 0
        self.frame_delay = 12

        self.down_images = down_img
        self.left_images = left_img
        self.up_images = up_img
        self.right_images = right_img
        self.direction = direction
        self.center_point = center_point

    def animate(self):
        self.frame_count += 1
        if self.frame_count > self.frame_delay:
            self.frame_count = 0
            self.current_frame += 1

            if self.current_frame > self.max_frame:
                self.current_frame = 0

        if self.direction == self.DOWN:
            self.image = self.down_images[self.current_frame]
        elif self.direction == self.LEFT:
            self.image = self.left_images[self.current_frame]
        elif self.direction == self.UP:
            self.image = self.up_images[self.current_frame]
        elif self.direction == self.RIGHT:
            self.image = self.right_images[self.current_frame]
