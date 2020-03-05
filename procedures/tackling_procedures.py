from procedures.procedure import Procedure
from random import random, choice

from enums import PlayStyle, Side, Direction


class YAC(Procedure):
    def __init__(self, match, runner, tackler):
        super().__init__(match)
        self._runner = runner
        self._tackler = tackler

    def step(self):
        self.match.state.add_temp_yards(max(0, self._runner.strength + self._runner.carrying -
                                            self._tackler.strength - self._tackler.tackling))


class GetTackler(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        # TODO: Vary these based off of formation and weighted probabilities
        if self.match.state.cur_off_play.style == PlayStyle.RUN:
            if self.match.state.cur_off_play.direction == Direction.LEFT:
                return choice([1, 2, 5, 6])
            elif self.match.state.cur_off_play.direction == Direction.MIDDLE:
                return choice([2, 3, 6, 7])
            elif self.match.state.cur_off_play.direction == Direction.RIGHT:
                return choice([3, 4, 7, 8])


class Tackling(Procedure):
    def __init__(self, match, runner, tackler):
        super().__init__(match)
        self._tackler = tackler[0]
        print(tackler)
        print(runner)
        self._runner = runner[0]

    def step(self):
        if random() > (self._tackler.strength + self._tackler.tackling / self._runner.strength + self._runner.carrying):
            # TODO: How many more yards from a failed tackle and who is the next tackler (if any)
            Tackling(self.match, self._runner, self._tackler)
            pass
        else:
            Fumble(self.match, self._runner, self._tackler)
        # TODO: That should depend on how many yards have gone
        # TODO: Who is the tackler?


class Fumble(Procedure):
    def __init__(self, match, runner, tackler):
        super().__init__(match)
        self._tackler = tackler
        self._runner = runner

    def step(self):
        if random() > (self._tackler.strength + self._tackler.tackling / self._runner.strength + self._runner.carrying):
            self.match.state.blue_flag = 1
            EndPlay(self.match)
            # TODO: Eventually need a return distance but works for now
        else:
            YAC(self.match, self._runner, self._tackler)
