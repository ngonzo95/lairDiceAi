from unittest import TestCase
from unittest.mock import Mock
from Core.Game import Game
import random


class TestGame(TestCase):
    def setUp(self):
        self.num_users = 4
        self.num_dice = 7
        self.game = Game(self.num_users, self.num_dice)

    def test_setup_game_creates_a_list_of_users_each_having_the_right_number_of_dice(self):
        self.assertEqual(len(self.game._users), self.num_users)

        for user in self.game._users:
            self.assertEqual(user.get_number_of_dice(), self.num_dice)

    def test_set_up_round_gives_each_player_a_hand_equal_to_the_number_of_dice_they_have(self):
        for user in self.game._users:
            for _ in range (random.randint(0, self.num_dice-1)):
                user.lose_a_die()

        self.game.setup_round()

        for user in self.game._users:
            self.assertEqual(len(user.get_hand()), user.get_number_of_dice() )

    def test_set_up_rounds_creates_accurate_dice_totals(self):
        self.game.setup_round()
        all_dice = []
        for user in self.game._users:
            all_dice += user.get_hand()
        for i in range(6):
            self.assertEqual(all_dice.count(i+1), self.game._dice_totals[i])

    def test_play_round(self):
        None
