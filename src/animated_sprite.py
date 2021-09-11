from src.base_sprite import BaseSprite
from src.common import Direction


class AnimatedSprite(BaseSprite):
    def __init__(self, center_point, direction, images, name):
        down_images = images[0]
        left_images = images[1]
        up_images = images[2]
        right_images = images[3]
        super().__init__(center_point, images[0][0])
        self.name = name
        self.current_frame = 0
        self.frame_count = 0
        self.frame_delay = 2
        self.direction = direction
        self.images_map = {
            Direction.DOWN.value: down_images,
            Direction.LEFT.value: left_images,
            Direction.UP.value: up_images,
            Direction.RIGHT.value: right_images
        }

    def animate(self):
        max_frame = 1
        self.frame_count += 1
        if self.frame_count % 15 == 0:
            if self.frame_count > self.frame_delay:
                self.frame_count = 0
                self.current_frame += 1
            if self.current_frame > max_frame:
                self.current_frame = 0
        if self.direction in self.images_map.keys():
            self.image = self.images_map[self.direction][self.current_frame]
        self.dirty = 1

    def pause(self):
        self.dirty = 1
