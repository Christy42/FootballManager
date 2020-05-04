from procedures.procedure import Procedure
from random import random, randint


from enums import Depth, Side
from utils import repeated_random


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
    def __init__(self, match, runner, sack=False, tackle_att=1, rush=False):
        super().__init__(match)
        self._runner = runner
        self._sack = sack
        self._tackle_att = tackle_att
        self._rush = rush
        self._tackler = self.match.state.cur_def_players[self.get_tackler(rush)][0]

    def step(self):
        # broken tackle - needs more yards from a tackle
        tackle_value = 30 * self._tackler.tackling + 18 * self._tackler.strength + 15 * self._tackler.elusiveness + \
                       7 * self._tackler.speed
        runner_value = self._runner.strength * 3 + self._runner.carrying + 2 * self._runner.elusiveness + \
            self._runner.speed
        if random() > tackle_value / (tackle_value + runner_value) and self._tackle_att < 3:
            # Extra yards, new tackler
            # Extra yards should take into account new tackler
            Tackling(self.match, self._runner, rush=self._rush, tackle_att=self._tackle_att+1)
        else:
            # Tackle and maybe a fumble
            Fumble(self.match, self._runner, self._tackler)

    def get_tackler(self, rush=False):
        # TODO: Need to deal with different scenarios from run though
        sec_layer = True if self.match.state.temp_yards > 2 else False
        points = [0] * 11
        off_key = {self.match.state.cur_off_players[a][0]: a for a in self.match.state.cur_off_players}
        for i in range(len(self.match.state.cur_def_play.assignments)):
            dist = self.match.state.cur_def_play.assignments[i].area.\
                distance(self.match.state.cur_off_play.assignments[off_key[self._runner]].field_loc)
            assign = self.match.state.cur_def_play.assignments[i]
            points[i] += randint(0, 40)
            if assign.blitz and rush:
                points[i] += 10 + randint(0, 10) - sec_layer * randint(0, 20)
            points[i] += 30 - dist * 5
            if self.match.state.temp_yards > 2 and assign.depth == Depth.BACK:
                points[i] -= 10
            if self.match.state.temp_yards > 5 and assign.depth in [Depth.SHORT, Depth.BACK]:
                points[i] -= 15
            if assign.target is not None and assign.target == self._runner:
                points[i] += 25 + randint(0, 20)
        arg_max = lambda j: points[j]
        tackler = self.match.state.cur_def_players[max(range(len(points)), key=arg_max)]
        dist = self.match.state.cur_def_play.assignments[max(range(len(points)), key=arg_max)].area.\
            distance(self.match.state.cur_off_play.assignments[off_key[self._runner]].field_loc)
        if rush:
            temp_dist = 0
        else:
            temp_dist = 1 + repeated_random(dist * 2 + 1, self._runner.speed / (self._runner.speed + tackler.speed))
        self.match.state.add_temp_yards(temp_dist)
        return max(range(len(points)), key=arg_max)


class Fumble(Procedure):
    def __init__(self, match, runner, tackler):
        super().__init__(match)
        self._tackler = tackler
        self._runner = runner

    def step(self):
        tackler_value = self._tackler.strength + 2 * self._tackler.tackling + 500
        runner_value = self._runner.strength * 2 + self._runner.carrying + 500
        if random() < tackler_value / (25 * runner_value + tackler_value):
            if random() < 0.5:
                self.match.state.blue_flag()
        else:
            YAC(self.match, self._runner, self._tackler)
