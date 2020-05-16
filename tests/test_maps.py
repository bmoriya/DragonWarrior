from unittest import TestCase

from tests.test_game import TestMockMap


class TestDragonWarriorMap(TestCase):

    def setUp(self) -> None:
        self.dragon_warrior_map = TestMockMap(None)

    def test_get_initial_character_location(self):
        self.assertEqual(self.dragon_warrior_map.get_initial_character_location('HERO').take(0), 0)
        self.assertEqual(self.dragon_warrior_map.get_initial_character_location('HERO').take(1), 0)
