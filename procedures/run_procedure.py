from random import choice, randint

from procedures.tackling_procedures import Tackling
from procedures.procedure import Procedure
from enums import GenOff, RunStyle, OffAssign, Side, Depth
from plays.coverage import Coverage


# TODO: What types of run are there?  How do they differ.  Probably don't need new ones for each side
# TODO: Add more types of run but get these working first
class Run(Procedure):
    def __init__(self, match):
        super().__init__(match)
        self._side = self.match.state.cur_off_play.side
        self._blockers = []

    def step(self):
        # TODO: How to figure tackler
        Tackling(self.match, self.match.state.cur_off_players[self.match.state.cur_off_play.runner],
                 self.match.state.cur_def_players[self.get_tackler()])
        YBCRun(self.match)

    def ybc(self):
        pass

    def broken_tackle(self):
        pass

    def get_tackler(self):
        sec_layer = True if self.match.state.temp_yards > 2 else False
        tackler = 10
        points = [0] * 11
        for i in range(len(self.match.state.cur_def_play.assignments)):
            if self.match.state.cur_def_play.assignments[i].blitz:
                points[i] += 10 + randint(0, 5) - sec_layer * randint(0, 5)
            if (self.match.state.cur_off_play.side == Side.LEFT and
                    self.match.state.cur_def_play.assignments[i].side in [Side.LEFT, Side.CENT_L]):
                points[i] += 10 + randint(0, 5)
            elif (self.match.state.cur_off_play.side == Side.RIGHT and
                    self.match.state.cur_def_play.assignments[i].side in [Side.RIGHT, Side.CENT_R]):
                points[i] += 10 + randint(0, 5)
            elif (self.match.state.cur_off_play.side == Side.CENTER and
                    self.match.state.cur_def_play.assignments[i].side == Side.CENTER):
                points[i] += 10 + randint(0, 5)
            if self.match.state.cur_def_play.assignments[i].depth in [Depth.SHORT, Depth.BACK]:
                points[i] += 5 + randint(0, 3)
            elif self.match.state.cur_def_play.assignments[i].depth in [Depth.MID, Depth.DEEP]:
                points[i] -= 5 - randint(0, 3)
        arg_max = lambda j: points[j]
        return max(range(len(points)), key=arg_max)


# TODO: I mean, returns a number but doesn't do very much???
# Could I have a YBC stat?  But that doesn't really affect the
class YBCRun(Procedure):
    def __init__(self, match):
        super().__init__(match)
        self._left_block = 0
        self._center_block = 0
        self._right_block = 0
        self._left_rush = 0
        self._center_rush = 0
        self._right_rush = 0

    def step(self):
        self.blocking()
        self.rush()
        if self.match.state.cur_off_play.side == Side.LEFT:
            self.match.state.add_temp_yards((self._left_block - self._left_rush) / 100)
        elif self.match.state.cur_off_play.side == Side.CENTER:
            self.match.state.add_temp_yards((self._center_block - self._center_rush) / 100)
        elif self.match.state.cur_off_play.side == Side.RIGHT:
            self.match.state.add_temp_yards((self._right_block - self._right_rush) / 100)
        # how do we figure the yards??

    def block_addition(self, player):
        if self.match.state.cur_off_play.block_style == RunStyle.ZONE:
            return (player.strength + 1.5 * player.blocking + 0.2 * player.elusiveness + 0.1 * player.speed) / 2.8
        elif self.match.state.cur_off_play.block_style == RunStyle.MAN:
            return (player.strength * 1.5 + player.blocking + 0.05 * player.elusiveness) / 2.55

    @staticmethod
    def rush_addition(player):
        return (player.strength + 0.9 * player.rushing + 0.1 * player.elusiveness + 0.2 * player.speed) / 2.2

    def blocking(self):
        # TODO: Who is actually involved in each position on this play?
        # Left blocking
        for i in GenOff:
            if self.match.state.cur_off_play.assignments[i] == OffAssign.LEFT_BLOCK:
                self._left_block += 0.9 * self.block_addition(self.match.state.cur_off_players[i][0])
            elif self.match.state.cur_off_play.assignments[i] == OffAssign.CENTER_BLOCK:
                self._left_block += 0.1 * self.block_addition(self.match.state.cur_off_players[i][0])
        # Right blocking
        for i in GenOff:
            if self.match.state.cur_off_play.assignments[i] == OffAssign.RIGHT_BLOCK:
                self._right_block += 0.9 * self.block_addition(self.match.state.cur_off_players[i][0])
            elif self.match.state.cur_off_play.assignments[i] == OffAssign.CENTER_BLOCK:
                self._right_block += 0.1 * self.block_addition(self.match.state.cur_off_players[i][0])
        # Center blocking
        for i in GenOff:
            if self.match.state.cur_off_play.assignments[i] == OffAssign.CENTER_BLOCK:
                self._center_block += 0.8 * self.block_addition(self.match.state.cur_off_players[i][0])
            elif self.match.state.cur_off_play.assignments[i] == OffAssign.RIGHT_BLOCK:
                self._center_block += 0.1 * self.block_addition(self.match.state.cur_off_players[i][0])
            elif self.match.state.cur_off_play.assignments[i] == OffAssign.LEFT_BLOCK:
                self._center_block += 0.1 * self.block_addition(self.match.state.cur_off_players[i][0])

    def form_adjustment(self, i):
        if self.match.state.defense_formation.no_dl > i:
            return 1
        elif self.match.state.defense_formation.no_dl + self.match.state.defense_formation.no_lb > i:
            return 0.9
        else:
            return 0.7

    def rush(self):
        # TODO: Who is actually involved in each position on this play?
        # Left blocking
        for i in range(len(self.match.state.cur_off_play.assignments)):
            assignment = self.match.state.cur_def_play.assignments[i]
            if assignment.side == Side.LEFT and assignment.blitz:
                self._left_rush += 0.9 * self.rush_addition(self.match.state.cur_def_players[i][0]) \
                                   * self.form_adjustment(i)
            elif assignment.side == Side.CENTER and assignment.blitz:
                self._left_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i][0]) \
                                   * self.form_adjustment(i)
        # Right blocking
        for i in range(len(self.match.state.cur_off_play.assignments)):
            assignment = self.match.state.cur_def_play.assignments[i]
            if assignment.side == Side.RIGHT and assignment.blitz:
                self._right_rush += 0.9 * self.rush_addition(self.match.state.cur_def_players[i][0]) \
                                    * self.form_adjustment(i)
            elif assignment.side == Side.CENTER and assignment.blitz:
                self._right_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i][0]) *\
                                    self.form_adjustment(i)
        # Center blocking
        for i in range(len(self.match.state.cur_off_play.assignments)):
            assignment = self.match.state.cur_def_play.assignments[i]
            if assignment.side == Side.CENTER and assignment.blitz:
                self._center_rush += 0.8 * self.rush_addition(self.match.state.cur_def_players[i][0]) \
                                     * self.form_adjustment(i)
            elif assignment.side == Side.RIGHT and assignment.blitz:
                self._center_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i][0]) \
                                     * self.form_adjustment(i)
            elif assignment.side == Side.LEFT and assignment.blitz:
                self._center_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i][0]) \
                                     * self.form_adjustment(i)
