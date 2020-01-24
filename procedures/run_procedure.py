from procedures.tackling_procedures import *
from enums import Side, RunStyle, OffensiveAssignments, DefensiveAssignments


# TODO: What types of run are there?  How do they differ.  Probably don't need new ones for each side
# TODO: Add more types of run but get these working first
class Run(Procedure):
    def __init__(self, match, side):
        super().__init__(match)
        self._side = side
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
        if self.match.state.cur_off_play.style == PlayStyle.RUN:
            if self.match.state.cur_off_play.direction == Side.LEFT:
                return choice([1, 2, 5, 6])
            elif self.match.state.cur_off_play.direction == Side.CENTER:
                return choice([2, 3, 6, 7])
            elif self.match.state.cur_off_play.direction == Side.RIGHT:
                return choice([3, 4, 7, 8])


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
        return (player.strength + 0.9 * player.rush + 0.1 * player.elusiveness + 0.2 * player.speed) / 2.2

    def blocking(self):
        # TODO: Who is actually involved in each position on this play?
        # Left blocking
        for i in range(self.match.state.cur_off_play.assignments):
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.LEFT_BLOCK:
                self._left_block += 0.9 * self.block_addition(self.match.state.cur_off_players[i])
            elif self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.CENTER_BLOCK:
                self._left_block += 0.1 * self.block_addition(self.match.state.cur_off_players[i])
        # Right blocking
        for i in range(self.match.state.cur_off_play.assignments):
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.RIGHT_BLOCK:
                self._right_block += 0.9 * self.block_addition(self.match.state.cur_off_players[i])
            elif self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.CENTER_BLOCK:
                self._right_block += 0.1 * self.block_addition(self.match.state.cur_off_players[i])
        # Center blocking
        for i in range(self.match.state.cur_off_play.assignments):
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.CENTER_BLOCK:
                self._center_block += 0.8 * self.block_addition(self.match.state.cur_off_players[i])
            elif self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.RIGHT_BLOCK:
                self._center_block += 0.1 * self.block_addition(self.match.state.cur_off_players[i])
            elif self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.LEFT_BLOCK:
                self._center_block += 0.1 * self.block_addition(self.match.state.cur_off_players[i])

    def form_adjustment(self, i):
        if self.match.state.defense_formation.dl > i:
            return 1
        elif self.match.state.defense_formation.dl + self.match.state.defense_formation.lb > i:
            return 0.9
        else:
            return 0.7

    def rush(self):
        # TODO: Who is actually involved in each position on this play?
        # Left blocking
        for i in range(self.match.state.cur_off_play.assignments):
            if self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.LEFT_RUSH:
                self._left_rush += 0.9 * self.rush_addition(self.match.state.cur_def_players[i]) * self.form_adjustment(i)
            elif self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.CENTER_RUSH:
                self._left_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i]) * self.form_adjustment(i)
        # Right blocking
        for i in range(self.match.state.cur_off_play.assignments):
            if self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.RIGHT_RUSH:
                self._right_rush += 0.9 * self.rush_addition(self.match.state.cur_def_players[i]) * self.form_adjustment(i)
            elif self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.CENTER_RUSH:
                self._right_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i]) * self.form_adjustment(i)
        # Center blocking
        for i in range(self.match.state.cur_off_play.assignments):
            if self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.CENTER_RUSH:
                self._center_rush += 0.8 * self.rush_addition(self.match.state.cur_def_players[i]) * self.form_adjustment(i)
            elif self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.RIGHT_RUSH:
                self._center_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i]) * self.form_adjustment(i)
            elif self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.LEFT_RUSH:
                self._center_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i]) * self.form_adjustment(i)
