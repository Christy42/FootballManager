from procedures.procedure import Procedure
import random

class EndQuarter(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class EndHalf(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class TimeOut(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class RunClock(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class EndPlay(Procedure):
    # TODO: I guess calls a figure next play function which then calls run or pass etc. as appropriate
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        # TODO: Need to turn temp yards into real yards, recalculate down and distance.  Deal with TD/ Safety
        self.match.state.end_play_checks()


class ChoosePlay(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        if self.match.state.possession == 0:
            self.match.state.team1.choose_play_offense()
            self.match.state.team2.choose_play_defense()
        else:
            self.match.state.team2.choose_play_offense()
            self.match.state.team1.choose_play_defense()


class CoinFlip(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        if random.randint(0, 1) == 0:
            self.match.state.set_possession(0)
        else:
            self.match.state.set_possession(1)
        ChoosePlay(self.match)
