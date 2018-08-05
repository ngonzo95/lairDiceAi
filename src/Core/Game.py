from Core.User import User
from Core.Utils.RandomUtils import random_hand
from Core.Models.Types import UserEventEnum, UserEvent


class Game:
    def __init__(self, number_of_users=5, number_of_dice=6):
        self._users = []
        self._currentPlayer = 0
        self._dice_totals = [0, 0, 0, 0, 0, 0]
        for i in range(number_of_users):
            self._users.append(User(number_of_dice))

    def setup_round(self):
        self._dice_totals = [0, 0, 0, 0, 0, 0]
        for user in self._users:
            hand = random_hand(user.get_number_of_dice())
            user.set_hand(hand)
            for die in hand:
                self._dice_totals[die-1] += 1

    def play_a_round(self):
        last_user_event = UserEvent(UserEventEnum.BET, (0, 0))

        while last_user_event == UserEventEnum.BET:
            self._users[self._currentPlayer].play_a_turn()
            self._currentPlayer += 1

        calculateResult(last_user_event)

    def play_game(self):
        while True:
            self.setup_round()
            self.play_a_round()
