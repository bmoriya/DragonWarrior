from src.animated_sprite import AnimatedSprite
from src.base_sprite import BaseSprite


class RoamingCharacter(AnimatedSprite):
    def __init__(self, center_point, direction,
                 down_images=None, left_images=None, up_images=None, right_images=None, name=None):
        BaseSprite.__init__(self, center_point, down_images[0])
        self.last_roaming_clock_check = None
        self.name = name
        self.column = None
        self.row = None
        self.moving = False
        self.next_tile = None
        self.next_tile_checked = None
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
        self.down_images = down_images
        self.left_images = left_images
        self.up_images = up_images
        self.right_images = right_images
        self.direction = direction
        self.center_point = center_point
