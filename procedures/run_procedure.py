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
        pass

    def ybc(self):
        pass

    def broken_tackle(self):
        pass


# TODO: More exp, agility based.  Bigger gains, bigger losses.
# TODO: So who is involved.  Full Back (maybe) and 5 linemen vs  DL and blitzers...
class ZoneBlockRun(Run):
    def __init__(self, match, side):
        super().__init__(match, side)

    def step(self):
        if self.match.state.offense_formation in []:
            self._blockers = []
        else:
            self._blockers = []
        block_power = self.blocking()
        def_power = self.rush()

    def blocking(self):
        if self._side == Side.LEFT:
            return 1
        elif self._side == Side.CENTER:
            return 2
        else:
            return 3

    def rush(self):
        if self._side == Side.LEFT:
            return 1
        elif self._side == Side.CENTER:
            return 2
        else:
            return 3


# TODO: Less exp based.  Smaller gains, smaller losses.
class ManBlockRun(Run):
    def __init__(self, match, side):
        super().__init__(match, side)
        pass

    def step(self):
        pass


# TODO: I mean, returns a number but doesn't do very much???
# Could I have a YBC stat?  But that doesn't really affect the
class YBCRun(Procedure):
    def __init__(self, match, side):
        super().__init__(match)
        self._side = side
        self._left_block = 0
        self._center_block = 0
        self._right_block = 0
        self._left_rush = 0
        self._center_rush = 0
        self._right_rush = 0

    def step(self):
        pass

    def block_addition(self, player):
        if self.match.state.cur_off_play.block_style == RunStyle.ZONE:
            return 0
        elif self.match.state.cur_off_play.block_style == RunStyle.MAN:
            return 0

    @staticmethod
    def rush_addition(player):
        return 0

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
        pass

    def rush(self):
        # TODO: Who is actually involved in each position on this play?
        # Left blocking
        for i in range(self.match.state.cur_off_play.assignments):
            if self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.LEFT_RUSH:
                self._left_rush += 0.9 * self.rush_addition(self.match.state.cur_def_players[i])
            elif self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.CENTER_RUSH:
                self._left_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i])
        # Right blocking
        for i in range(self.match.state.cur_off_play.assignments):
            if self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.RIGHT_RUSH:
                self._right_rush += 0.9 * self.rush_addition(self.match.state.cur_def_players[i])
            elif self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.CENTER_RUSH:
                self._right_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i])
        # Center blocking
        for i in range(self.match.state.cur_off_play.assignments):
            if self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.CENTER_RUSH:
                self._center_rush += 0.8 * self.rush_addition(self.match.state.cur_def_players[i])
            elif self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.RIGHT_RUSH:
                self._center_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i])
            elif self.match.state.cur_def_play.assignments[i] == DefensiveAssignments.LEFT_RUSH:
                self._center_rush += 0.1 * self.rush_addition(self.match.state.cur_def_players[i])
