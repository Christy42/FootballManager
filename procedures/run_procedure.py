from random import randint, random

from procedures.tackling_procedures import Tackling
from procedures.procedure import Procedure
from enums import GenOff, Side, Depth


# TODO: What types of run are there?  How do they differ.  Probably don't need new ones for each side
# TODO: Add more types of run but get these working first
class Run(Procedure):
    def __init__(self, match):
        super().__init__(match)
        self._side = self.match.state.cur_off_play.side
        self._blockers = []

    def step(self):
        print("Tackling")
        print(self.match.state.cur_off_play.runner)
        Tackling(self.match, self.match.state.cur_off_play.runner, rush=True)
        YBCRun(self.match)


# TODO: I mean, returns a number but doesn't do very much???
# Could I have a YBC stat?  But that doesn't really affect the
class YBCRun(Procedure):
    def __init__(self, match):
        super().__init__(match)
        self._blocks = {Side.LEFT: 0, Side.CENTER: 0, Side.RIGHT: 0}
        self._rushes = {Side.LEFT: 0, Side.CENTER: 0, Side.RIGHT: 0}

    def step(self):
        self.blocking()
        self.rush()
        amend = 4
        temp = {Side.LEFT: 0, Side.CENTER: 0, Side.RIGHT: 0}
        for side in [Side.LEFT, Side.CENTER, Side.RIGHT]:
            for i in range(-3, 6):
                if random() < self._rushes[side] / (self._rushes[side] + self._blocks[side] * amend + randint(0, 1100)) or i == 5:
                    temp[side] = i
                    break
        side = self.match.state.cur_off_play.side
        if temp[side] > 0:
            temp_value = temp[side] + sum([min(temp[a], 0) for a in [Side.LEFT, Side.CENTER, Side.RIGHT] if a != side]) / 2
        else:
            temp_value = temp[side]
        self.match.state.stats["ybc"] = self.match.state.stats.get("ybc", 0) + temp_value
        self.match.state.add_temp_yards(temp_value)

    @staticmethod
    def block_addition(player):
        return (player.strength * 1.5 + player.blocking + 0.05 * player.elusiveness) / 2.55

    @staticmethod
    def rush_addition(player):
        return (player.strength + 0.9 * player.rushing + 0.1 * player.elusiveness + 0.2 * player.speed) / 2.2

    def blocking(self):
        count = {Side.LEFT: 0, Side.CENTER: 0, Side.RIGHT: 0}
        for i in GenOff:
            assignment = self.match.state.cur_off_play.assignments[i]
            for side in [Side.LEFT, Side.CENTER, Side.RIGHT]:
                if assignment.side == side and assignment.blocking:
                    count[side] += 1
                    self._blocks[side] += (0.8 if side == Side.CENTER else 0.9) * \
                        self.block_addition(self.match.state.cur_off_players[i][0])
                elif (assignment.side == Side.CENTER or side == Side.CENTER) and assignment.blocking:
                    self._blocks[side] += 0.1 * self.block_addition(self.match.state.cur_off_players[i][0])
        for side in [Side.LEFT, Side.CENTER, Side.RIGHT]:
            self._blocks[side] = round(self._blocks[side] * (1 - min(count[side] - 1, 6) / 10))

    def form_adjustment(self, i):
        return 1 if self.match.state.defense_formation.no_dl > i else 0.9 \
            if self.match.state.defense_formation.no_dl + self.match.state.defense_formation.no_lb > i else 0.7

    def rush(self):
        count = {Side.LEFT: 0, Side.CENTER: 0, Side.RIGHT: 0}
        for i in range(len(self.match.state.cur_off_play.assignments)):
            assignment = self.match.state.cur_def_play.assignments[i]
            for side in [Side.LEFT, Side.CENTER, Side.RIGHT]:
                if assignment.side == side and assignment.blitz:
                    count[side] += 1
                    self._rushes[side] += (0.8 if side == Side.CENTER else 0.9) * self.rush_addition(self.match.state.cur_def_players[i][0]) \
                                   * self.form_adjustment(i)
                elif (side == Side.CENTER or assignment == Side.CENTER) and assignment.blitz:
                    self._rushes[side] += 0.1 * self.rush_addition(self.match.state.cur_def_players[i][0]) \
                                       * self.form_adjustment(i)
        for side in [Side.LEFT, Side.CENTER, Side.RIGHT]:
            self._rushes[side] = round(self._rushes[side] * (1 - min(count[side] - 1, 6) / 10))
