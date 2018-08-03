from typing import List
from enum import Enum

Hand = List[int]


class UserEvent(Enum):
    BET = 1
    CALL = 2
    CHECK = 3
