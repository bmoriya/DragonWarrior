from unittest import TestCase
from unittest.mock import MagicMock

from src.animated_sprite import AnimatedSprite
from src.common import Direction
from src.maps import parse_animated_spritesheet


class TestAnimatedSprite(TestCase):
    def setUp(self) -> None:
        mock = MagicMock()
        self.mock_images = parse_animated_spritesheet(mock, is_roaming=True)
        self.anim_sprite = AnimatedSprite(center_point=None, direction=None,
                                          down_images=self.mock_images[Direction.DOWN.value],
                                          left_images=self.mock_images[Direction.LEFT.value],
                                          up_images=self.mock_images[Direction.UP.value],
                                          right_images=self.mock_images[Direction.RIGHT.value],
                                          name='Mock')

    def test_initialized_values(self):
        self.assertEqual(self.anim_sprite.name, 'Mock')
        self.assertEqual(self.anim_sprite.down_images, self.mock_images[Direction.DOWN.value])
        self.assertEqual(self.anim_sprite.left_images, self.mock_images[Direction.LEFT.value])
        self.assertEqual(self.anim_sprite.up_images, self.mock_images[Direction.UP.value])
        self.assertEqual(self.anim_sprite.right_images, self.mock_images[Direction.RIGHT.value])
        self.assertEqual(self.anim_sprite.current_frame, 0)
        self.assertEqual(self.anim_sprite.max_frame, 1)
        self.assertEqual(self.anim_sprite.frame_count, 0)
        self.assertEqual(self.anim_sprite.frame_delay, 2)
        self.assertIsNone(self.anim_sprite.direction)
        self.assertIsNone(self.anim_sprite.center_point)

    def test_directional_values(self):
        self.assertEqual(self.mock_images[0], self.mock_images[Direction.DOWN.value])
        self.assertEqual(self.mock_images[1], self.mock_images[Direction.LEFT.value])
        self.assertEqual(self.mock_images[2], self.mock_images[Direction.UP.value])
        self.assertEqual(self.mock_images[3], self.mock_images[Direction.RIGHT.value])

    def test_animate_increment_frame_count(self):
        self.anim_sprite.frame_count = 0
        self.anim_sprite.animate()
        self.assertEqual(self.anim_sprite.frame_count, 1)

    def test_animate_current_frame(self):
        self.anim_sprite.frame_count = 14
        self.anim_sprite.animate()
        self.assertEqual(self.anim_sprite.current_frame, 1)

    def test_animate_down_direction(self):
        self.anim_sprite.direction = Direction.DOWN.value
        self.anim_sprite.animate()
        self.assertEqual(self.anim_sprite.image, self.anim_sprite.down_images[self.anim_sprite.current_frame])

    def test_animate_left_direction(self):
        self.anim_sprite.direction = Direction.LEFT.value
        self.anim_sprite.animate()
        self.assertEqual(self.anim_sprite.image, self.anim_sprite.left_images[self.anim_sprite.current_frame])

    def test_animate_up_direction(self):
        self.anim_sprite.direction = Direction.UP.value
        self.anim_sprite.animate()
        self.assertEqual(self.anim_sprite.image, self.anim_sprite.up_images[self.anim_sprite.current_frame])

    def test_animate_right_direction(self):
        self.anim_sprite.direction = Direction.RIGHT.value
        self.anim_sprite.animate()
        self.assertEqual(self.anim_sprite.image, self.anim_sprite.right_images[self.anim_sprite.current_frame])
