from Core.Models.Types import Hand
import numpy as np


def random_dice(number_of_dice: int) -> Hand:
    return Hand(np.random.randint(1, 7, number_of_dice))
