from unittest import TestCase
from Core.User import User
from Core.Exceptions.UserSetupException import UserSetupException


class TestUser(TestCase):
    def setUp(self):
        self.starting_number_of_dice = 6
        self.user = User(self.starting_number_of_dice)

    def test_get_number_of_dice_should_return_number_of_dice(self):
        self.assertEqual(self.user.get_number_of_dice(), self.starting_number_of_dice)

    def test_gain_a_die_when_number_of_dice_less_that_starting_number_increase_by_1(self):
        self.user._number_of_dice = 3
        self.user.gain_a_die()
        self.assertEqual(self.user.get_number_of_dice(), 4)

    def test_gain_a_die_when_number_of_dice_equal_to_starting_number_changes_nothing(self):
        self.user.gain_a_die()
        self.assertEqual(self.user.get_number_of_dice(), self.starting_number_of_dice)

    def test_lose_a_die_should_decrease_number_of_dice_by_one(self):
        self.user.lose_a_die()
        self.assertEqual(self.user.get_number_of_dice(), self.starting_number_of_dice - 1)

    def test_set_hand_when_right_size_sets_hand(self):
        hand_to_set = [1, 2, 3, 4, 5, 6]
        self.user.set_hand(hand_to_set)
        self.assertEqual(self.user._hand, hand_to_set )

    def test_set_hand_when_wrong_size_throws(self):
        hand_to_set = [1, 2, 3]
        with self.assertRaises(UserSetupException):
            self.user.set_hand(hand_to_set)

