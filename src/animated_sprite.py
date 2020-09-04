from src.base_sprite import BaseSprite
from src.common import Direction


class AnimatedSprite(BaseSprite):
    def __init__(self, center_point, direction, down_images, left_images, up_images, right_images, name):
        super().__init__(center_point, down_images[0])
        self.name = name
        if down_images is None:
            down_images = []
        if left_images is None:
            left_images = []
        if up_images is None:
            up_images = []
        if right_images is None:
            right_images = []
        self.current_frame = 0
        self.max_frame = 1
        self.frame_count = 0
        self.frame_delay = 2
        self.direction = direction
        self.center_point = center_point
        # TODO: Implement the use of the images map in the animate method.
        self.images_map = {
            Direction.DOWN.value: down_images,
            Direction.LEFT.value: left_images,
            Direction.UP.value: up_images,
            Direction.RIGHT.value: right_images
        }

    def animate(self):
        self.frame_count += 1
        if self.frame_count % 15 == 0:
            if self.frame_count > self.frame_delay:
                self.frame_count = 0
                self.current_frame += 1
            if self.current_frame > self.max_frame:
                self.current_frame = 0
        if self.direction in self.images_map.keys():
            self.image = self.images_map[self.direction][self.current_frame]
        self.dirty = 1

    def pause(self):
        self.dirty = 1
