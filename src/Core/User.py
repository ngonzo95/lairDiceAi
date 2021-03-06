from Core.Models.Types import Hand, UserEventEnum, UserEvent
from Core.Exceptions.UserSetupException import UserSetupException
from Core.BetLog import BetLog

class User:
    def __init__(self, starting_number_of_dice, name="unknown user"):
        self._hand: Hand = []
        self._number_of_dice = starting_number_of_dice
        self._max_number_of_dice = starting_number_of_dice
        self.name = name

    def get_number_of_dice(self):
        return self._number_of_dice

    def gain_a_die(self):
        if self._number_of_dice < self._max_number_of_dice:
            self._number_of_dice += 1

    def lose_a_die(self):
        self._number_of_dice -= 1

    def set_hand(self, hand: Hand):
        self._hand = hand
        if len(hand) != self._number_of_dice:
            raise UserSetupException("Tried to set a hand with %d dice when the user"
                                     " has a hand of %d dice" % (len(hand), self._number_of_dice))

    def get_hand(self):
        return self._hand

    def play_a_turn(self, bets_this_round: BetLog) -> UserEvent:

        _, last_event = bets_this_round.get_bets()[-1]

        if last_event.count < 6:
            return UserEvent(UserEventEnum.BET, (last_event.count + 1, 2))
        else:
            return UserEvent(UserEventEnum.CHECK)
