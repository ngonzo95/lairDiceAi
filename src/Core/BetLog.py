from Core.Models.Types import UserEvent


class BetLog:
    def __init__(self):
        self._bet_log = []

    def __str__(self):
        result_str = "starting Bet Log printout \n"
        for name, event in self._bet_log:
            result_str += name + " " + str(event) + "\n"
        return result_str

    def add_bet(self, user_name:str, event:UserEvent):
        self._bet_log.append((user_name, event))

    def get_bets(self):
        return self._bet_log

    def clear_bets(self):
        self._bet_log = []
