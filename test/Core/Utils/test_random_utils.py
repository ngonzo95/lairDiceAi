from unittest import TestCase
from Core.Utils.RandomUtils import random_hand


class TestRandomUtils(TestCase):

    def test_call_random_dice_with_number_dice_returns_hand_of_desired_size(self):
        self.assertEqual(len(random_hand(6)), 6)

    def test_call_random_all_entries_are_integers_between_1_and_6(self):
        hand = random_hand(100)
        for die in hand:
            self.assertTrue(die < 7, msg="die larger than 6 found")
            self.assertTrue(die > 0, msg="die smaller than 1 found")
