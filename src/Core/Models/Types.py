from typing import List
from enum import Enum

Hand = List[int]


class UserEventEnum(Enum):
    BET = 1
    CALL = 2
    CHECK = 3


class UserEvent:
    def __init__(self, event_type: UserEventEnum, bet: (int, int)):
        self.event_type = event_type
        self.bet = bet
