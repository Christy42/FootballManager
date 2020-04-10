from procedures.tackling_procedures import *
from enums import OffensiveAssignments, DefensiveAssignments


class RouteRun(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class PassBlock(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        left_block = l_count = center_block = right_block = c_count = r_count = 0
        center_block = 0
        right_block = 0
        for i in range(self.match.state.cur_off_assignments):
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.LEFT_BLOCK:
                pass
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.CENTER_BLOCK:
                pass
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.RIGHT_BLOCK:
                pass
        for i in range(self.match.state.cur_def_assignments):
            if self.match.state.cur_off_play.assignments[i] == DefensiveAssignments.LEFT_RUSH:
                pass
            if self.match.state.cur_off_play.assignments[i] == DefensiveAssignments.CENTER_RUSH:
                pass
            if self.match.state.cur_off_play.assignments[i] == DefensiveAssignments.RIGHT_RUSH:
                pass
        for i in range(self.match.state.cur_off_assignments):
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.SCAN_BLOCK:
                pass
        # TODO:  Add on extra QB mobility time here
        pass


class Pass(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class DecisionMade(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        # Need time QB has
        # Need the time the routes take
        # Check reads, work out which is right (50, 30, 20 or (60, 40) of them being the right read) or dump off
        # Call pass attempt or call sack (or call QB run eventually)
        pass


class AfterCatch(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass
