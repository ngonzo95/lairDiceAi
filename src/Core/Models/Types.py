from typing import List
from enum import Enum

Hand = List[int]


class UserEventEnum(Enum):
    BET = 1
    CALL = 2
    CHECK = 3


class UserEvent:
    def __init__(self, event_type: UserEventEnum, bet: (int, int) = (0, 0)):
        self.event_type = event_type
        self.bet = bet
        self.count = bet[0]
        self.die_number = bet[1]

    def __str__(self):
        if self.event_type == UserEventEnum.BET:
            return "BET: There are " + str(self.count) + " " + str(self.die_number) + "s"

        elif self.event_type == UserEventEnum.CALL:
            return "CALL"
        else:
            return "CHECK"