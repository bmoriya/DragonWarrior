from src.animated_sprite import AnimatedSprite
from src.common import Direction


class Player(AnimatedSprite):

    def __init__(self, center_point, images, direction=Direction.DOWN.value):
        AnimatedSprite.__init__(self, center_point, direction, images, name='HERO')
