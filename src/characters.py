from pygame.transform import scale

from src.animated_sprite import AnimatedSprite
from src.common import ROAMING_GUARD_PATH, get_image, Direction, KING_LORIK_PATH, parse_animated_spritesheet
from src.config import SCALE


class Guard(AnimatedSprite):
    def __init__(self, center_point, direction, down_images=None):
        roaming_guard_sheet = get_image(ROAMING_GUARD_PATH)
        roaming_guard_sheet = scale(roaming_guard_sheet,
                                    (roaming_guard_sheet.get_width() * SCALE, roaming_guard_sheet.get_height() * SCALE))
        roaming_guard_images = parse_animated_spritesheet(roaming_guard_sheet, is_roaming=True)
        super().__init__(center_point, roaming_guard_images[Direction.DOWN.value], None, direction)

        self.down_images = roaming_guard_images[Direction.DOWN.value]
        self.left_images = roaming_guard_images[Direction.LEFT.value]
        self.up_images = roaming_guard_images[Direction.UP.value]
        self.right_images = roaming_guard_images[Direction.RIGHT.value]


class KingLorik(AnimatedSprite):
    def __init__(self, center_point, direction, down_images=None):
        king_lorik_sheet = get_image(KING_LORIK_PATH)
        king_lorik_sheet = scale(king_lorik_sheet,
                                 (king_lorik_sheet.get_width() * SCALE, king_lorik_sheet.get_height() * SCALE))
        king_lorik_images = parse_animated_spritesheet(king_lorik_sheet)
        self.down_images = king_lorik_images[Direction.DOWN.value]
        super().__init__(center_point, direction=None, down_images=self.down_images)

        self.direction = Direction.DOWN.value

        self.left_images = king_lorik_images[Direction.LEFT.value]
        self.up_images = king_lorik_images[Direction.UP.value]
        self.right_images = king_lorik_images[Direction.RIGHT.value]
        self.name = 'KING_LORIK'
