from unittest import TestCase
from Core.Models.Types import UserEvent, UserEventEnum
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
            for _ in range(random.randint(0, self.num_dice - 1)):
                user.lose_a_die()

        self.game.setup_round()

        for user in self.game._users:
            self.assertEqual(len(user.get_hand()), user.get_number_of_dice())

    def test_set_up_rounds_creates_accurate_dice_totals(self):
        self.game.setup_round()
        all_dice = []
        for user in self.game._users:
            all_dice += user.get_hand()
        for i in range(6):
            self.assertEqual(all_dice.count(i + 1), self.game._dice_totals[i])

    def test_validate_with_greater_count_returns_true(self):
        result = self.game.is_valid_event(UserEvent(UserEventEnum.BET, (4, 5)), UserEvent(UserEventEnum.BET, (3, 5)))
        self.assertTrue(result)

    def test_validate_with_lesser_count_returns_false(self):
        result = self.game.is_valid_event(UserEvent(UserEventEnum.BET, (4, 5)), UserEvent(UserEventEnum.BET, (6, 5)))
        self.assertFalse(result)

    def test_validate_with_equal_count_smaller_number_returns_false(self):
        result = self.game.is_valid_event(UserEvent(UserEventEnum.BET, (4, 4)), UserEvent(UserEventEnum.BET, (4, 5)))
        self.assertFalse(result)

    def test_validate_with_equal_count_equal_number_returns_false(self):
        result = self.game.is_valid_event(UserEvent(UserEventEnum.BET, (4, 4)), UserEvent(UserEventEnum.BET, (4, 4)))
        self.assertFalse(result)

    def test_validate_with_equal_count_larger_number_returns_true(self):
        result = self.game.is_valid_event(UserEvent(UserEventEnum.BET, (4, 4)), UserEvent(UserEventEnum.BET, (4, 4)))
        self.assertFalse(result)

    def test_validate_with_dice_number_greater_than_6_returns_fail(self):
        result = self.game.is_valid_event(UserEvent(UserEventEnum.BET, (4, 7)), UserEvent(UserEventEnum.BET, (1, 1)))
        self.assertFalse(result)

    def test_validate_with_dice_number_less_than_1_returns_fail(self):
        result = self.game.is_valid_event(UserEvent(UserEventEnum.BET, (4, 0)), UserEvent(UserEventEnum.BET, (1, 1)))
        self.assertFalse(result)

    def test_resolve_bet_when_user_called_and_wrong_removes_1_die_from_current_player(self):
        self.game.setup_round()
        number_of_3s = self.game._dice_totals[3 - 1]
        number_of_4s = self.game._dice_totals[4 - 1]
        self.game._current_player = random.randint(0, self.num_users - 1)

        self.game.resolve_bet(UserEvent(UserEventEnum.CALL), UserEvent(UserEventEnum.BET, (number_of_3s + 2, 3)))
        self.assertEqual(self.num_dice - 1, self.game.get_current_player().get_number_of_dice())

        self.game.resolve_bet(UserEvent(UserEventEnum.CALL), UserEvent(UserEventEnum.BET, (number_of_4s - 1, 4)))
        self.assertEqual(self.num_dice - 2, self.game.get_current_player().get_number_of_dice())

    def test_resolve_bet_when_user_called_and_correct_adds_1_die_to_current_player(self):
        self.game.setup_round()
        number_of_3s = self.game._dice_totals[3 - 1]
        self.game._current_player = random.randint(0, self.num_users - 1)
        self.game.get_current_player().lose_a_die()
        self.game.resolve_bet(UserEvent(UserEventEnum.CALL), UserEvent(UserEventEnum.BET, (number_of_3s, 3)))

        self.assertEqual(self.num_dice, self.game.get_current_player().get_number_of_dice())

    def test_resolve_bet_when_user_checks_and_table_has_equal_to_or_less_than_remove_1_die_from_current_player(self):
        self.game.setup_round()
        number_of_3s = self.game._dice_totals[3 - 1]
        self.game._current_player = random.randint(0, self.num_users - 1)
        self.game.resolve_bet(UserEvent(UserEventEnum.CHECK), UserEvent(UserEventEnum.BET, (number_of_3s, 3)))

        self.assertEqual(self.num_dice-1, self.game.get_current_player().get_number_of_dice())

    def test_resolve_bet_when_user_checks_and_table_has_greater_than_remove_1_die_from_last_player(self):
        self.game.setup_round()
        number_of_3s = self.game._dice_totals[3 - 1]
        self.game._current_player = random.randint(0, self.num_users - 1)
        self.game.resolve_bet(UserEvent(UserEventEnum.CHECK), UserEvent(UserEventEnum.BET, (number_of_3s+1, 3)))

        self.assertEqual(self.num_dice-1, self.game.get_previous_player().get_number_of_dice())

    def test_resolve_bet_remove_current_player_if_they_have_no_die(self):
        self.game.setup_round()
        number_of_3s = self.game._dice_totals[3 - 1]
        self.game._current_player = random.randint(0, self.num_users - 1)
        self.game.get_current_player()._number_of_dice = 1
        user = self.game.get_current_player()

        self.game.resolve_bet(UserEvent(UserEventEnum.CHECK), UserEvent(UserEventEnum.BET, (number_of_3s, 3)))

        self.assertFalse(user in self.game._users)

    def test_resolve_bet_remove_last_player_if_they_have_no_die(self):
        self.game.setup_round()
        number_of_3s = self.game._dice_totals[3 - 1]
        self.game._current_player = random.randint(0, self.num_users - 1)
        self.game.get_previous_player()._number_of_dice = 1
        user = self.game.get_previous_player()

        self.game.resolve_bet(UserEvent(UserEventEnum.CHECK), UserEvent(UserEventEnum.BET, (number_of_3s+1, 3)))

        self.assertFalse(user in self.game._users)

    def test_play_round(self):
        counter = 1
        for user in self.game._users:
            user.name = "User " + str(counter)
            counter += 1

        self.game.setup_round()
        self.game.play_a_round()
        print(self.game.bet_log)
        print(self.game._dice_totals)

        result = "At the end of the round the dice totals for each user are: \n"
        for user in self.game._users:
            result += user.name + ": " + str(user.get_number_of_dice()) + "\n"

        print(result)

    def test_play_game(self):
        counter = 1
        for user in self.game._users:
            user.name = "User " + str(counter)
            counter += 1

        self.game.play_game()