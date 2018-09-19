from Core.User import User
from Core.Utils.RandomUtils import random_hand
from Core.Models.Types import UserEventEnum, UserEvent
from Core.BetLog import BetLog


class Game:
    def __init__(self, number_of_users=5, number_of_dice=6):
        self._users = []
        self._current_player = 0
        self._dice_totals = [0, 0, 0, 0, 0, 0]
        self.bet_log = BetLog()

        for i in range(number_of_users):
            self._users.append(User(number_of_dice))

    def get_current_player(self) -> User:
        return self._users[self._current_player]

    def get_previous_player(self) -> User:
        previous_player_index = self._current_player - 1
        return self._users[previous_player_index]

    @staticmethod
    def is_valid_event(current: UserEvent, last: UserEvent):
        if current.die_number < 1 or current.die_number > 6:
            return False

        return current.count > last.count or (current.count == last.count and current.die_number > last.die_number)

    def resolve_bet(self, current: UserEvent, last: UserEvent):
        if current.event_type == UserEventEnum.CALL:
            if last.count == self._dice_totals[last.die_number-1]:
                self.get_current_player().gain_a_die()
            else:
                self.get_current_player().lose_a_die()
        else:
            if last.count > self._dice_totals[last.die_number-1]:
                self.get_previous_player().lose_a_die()
            else:
                self.get_current_player().lose_a_die()

        if self.get_current_player().get_number_of_dice() == 0:
            self._users.remove(self.get_current_player())

        if self.get_previous_player().get_number_of_dice() == 0:
            self._users.remove(self.get_previous_player())

    def setup_round(self):
        self._dice_totals = [0, 0, 0, 0, 0, 0]
        self.bet_log.clear_bets()

        for user in self._users:
            hand = random_hand(user.get_number_of_dice())
            user.set_hand(hand)
            for die in hand:
                self._dice_totals[die - 1] += 1

    def play_a_round(self):
        last_user_event = UserEvent(UserEventEnum.BET, (0, 0))
        current_user_event = UserEvent(UserEventEnum.BET, (0, 0))
        self.bet_log.add_bet("seed event", UserEvent(UserEventEnum.BET, (0, 0)))

        while last_user_event.event_type == UserEventEnum.BET:
            current_user_event = self.get_current_player().play_a_turn(self.bet_log)
            self.bet_log.add_bet(self.get_current_player().name, current_user_event)

            if current_user_event.event_type == UserEventEnum.BET:
                if not self.is_valid_event(current_user_event, last_user_event):
                    current_user_event = UserEvent(UserEventEnum.BET, (1000, 1000))
                self._current_player += 1

                if self._current_player == len(self._users):
                    self._current_player = 0

            last_user_event = current_user_event

        self.resolve_bet(current_user_event, last_user_event)

    def play_game(self):
        while len(self._users) > 1:
            self.setup_round()
            self.play_a_round()

        print("The winner was user" + self._users[0].name)
