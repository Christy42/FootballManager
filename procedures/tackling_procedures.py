from procedures.procedure import Procedure
from random import random


class YAC(Procedure):  # Yards after contact
    def __init__(self, match, runner, tackler):
        super().__init__(match)
        self._runner = runner
        self._tackler = tackler

    def step(self):
        tackling = (self._tackler.strength + self._tackler.tackling + self._tackler.elusiveness) / 3
        runner = (self._runner.strength + self._runner.carrying + self._runner.elusiveness) / 3
        if tackling / (runner + tackling) > random():
            temp = 0
        elif 0.5 > random():
            temp = 1
        elif 0.66 > random():
            temp = 2
        else:
            temp = 3
        self.match.state.add_temp_yards(temp)


class Tackling(Procedure):
    def __init__(self, match, runner, tackler):
        super().__init__(match)
        self._tackler = tackler[0]
        self._runner = runner[0]

    def step(self):
        # broken tackle - needs more yards from a tackle
        if random() > (self._tackler.strength + self._tackler.tackling) / \
                (self._runner.strength + self._runner.carrying):
            Tackling(self.match, self._runner, self._tackler)
        else:
            # Tackle and maybe a fumble
            Fumble(self.match, self._runner, self._tackler)
        # TODO: That should depend on how many yards have gone
        # TODO: Who is the tackler?


class Fumble(Procedure):
    def __init__(self, match, runner, tackler):
        super().__init__(match)
        self._tackler = tackler
        self._runner = runner

    def step(self):
        if random() > 10 * (self._tackler.strength + self._tackler.tackling) / \
                (self._runner.strength + self._runner.carrying):
            self.match.state.blue_flag()
        else:
            YAC(self.match, self._runner, self._tackler)
