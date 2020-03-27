from unittest import TestCase

from src.test_game import TestMap


class TestDragonWarriorMap(TestCase):

    def setUp(self) -> None:
        self.dragon_warrior_map = TestMap()

    def test_get_initial_character_location(self):
        self.assertEqual(self.dragon_warrior_map.get_initial_character_location('HERO').take(0), 0)
        self.assertEqual(self.dragon_warrior_map.get_initial_character_location('HERO').take(1), 0)
