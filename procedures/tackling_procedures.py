from procedures.procedure import Procedure
from random import random, randint


from enums import Depth, Side
from utils import repeated_random


class YAC(Procedure):  # Yards after contact
    def __init__(self, match, runner, tackler):
        super().__init__(match)
        self._runner = runner
        self._tackler = tackler
        self._run_val = self.match.state.cur_off_players[self._runner][0]

    def step(self):
        tackling = (self._tackler.strength + self._tackler.tackling + self._tackler.elusiveness) / 3
        runner = (self._run_val.strength + 5 * self._run_val.carrying + self._run_val.elusiveness) / 3
        if tackling / (runner + tackling) > random() * 2:
            temp = 0
        elif tackling / (runner + tackling) > random() * 2:
            temp = 1
        elif 0.4 > random():
            temp = 2
        elif 0.6 > random():
            temp = 3
        else:
            temp = 4
        print("temp")
        print(temp)
        self.match.state.add_temp_yards(temp)


class Tackling(Procedure):
    def __init__(self, match, runner, sack=False, tackle_att=1, rush=False):
        super().__init__(match)
        self._runner = runner
        self._sack = sack
        self._run_val = self.match.state.cur_off_players[self._runner][0]
        self._tackle_att = tackle_att
        self._rush = rush
        self._tackler = self.match.state.cur_def_players[self.get_tackler(rush)][0]

    def step(self):
        # broken tackle - needs more yards from a tackle
        tackle_value = 28 * self._tackler.tackling + 18 * self._tackler.strength + 15 * self._tackler.elusiveness + \
                       7 * self._tackler.speed
        runner_value = self._run_val.strength * 2 + 3 * self._run_val.carrying + 2 * self._run_val.elusiveness + \
            self._run_val.speed
        # self.match.state._tackles += 1
        if random() > tackle_value / (tackle_value + runner_value) and self._tackle_att < 4:
            # self.match.state._tackles_broken += 1
            print("RETACKLE")
            print(self._runner)
            Tackling(self.match, self._runner, rush=self._rush, tackle_att=self._tackle_att+1)
        else:
            # Tackle and maybe a fumble
            Fumble(self.match, self._runner, self._tackler)

    def get_tackler(self, rush=False):
        # TODO: Later but attempts going to the house!
        sec_layer = True if self.match.state.temp_yards > 2 else False
        points = [0] * 11
        off_key = {a: self.match.state.cur_off_players[a][0] for a in self.match.state.cur_off_players}
        print(off_key)
        for i in range(len(self.match.state.cur_def_play.assignments)):
            dist = self.match.state.cur_def_play.assignments[i].area.\
                distance(self.match.state.cur_off_play.assignments[self._runner].field_loc)
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
        tackler = self.match.state.cur_def_players[max(range(len(points)), key=arg_max)][0]
        dist = self.match.state.cur_def_play.assignments[max(range(len(points)), key=arg_max)].area.\
            distance(self.match.state.cur_off_play.assignments[self._runner].field_loc)
        if rush and self._tackle_att == 1:
            temp_dist = 0
        else:
            temp_dist = 1 + repeated_random(int(dist * 2 + 3), self._run_val.speed / (self._run_val.speed + tackler.speed))
        self.match.state.add_temp_yards(temp_dist)
        return max(range(len(points)), key=arg_max)


class Fumble(Procedure):
    def __init__(self, match, runner, tackler):
        super().__init__(match)
        self._tackler = tackler
        self._runner = runner
        self._run_val = self.match.state.cur_off_players[self._runner][0]

    def step(self):
        tackler_value = self._tackler.strength + 2 * self._tackler.tackling + 500
        runner_value = self._run_val.strength * 2 + self._run_val.carrying + 500
        if random() < tackler_value / (25 * runner_value + tackler_value):
            if random() < 0.5:
                self.match.state.blue_flag()
        else:
            YAC(self.match, self._runner, self._tackler)
