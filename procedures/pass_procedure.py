from procedures.tackling_procedures import *
from enums import OffensiveAssignments, DefensiveAssignments, Side
from utils import combine_values


class RouteRun(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class PassBlock(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        block_values = self._blocks()
        rush_values = self._rush()
        scan_blocks = self._scan(block_values, rush_values)
        times = self._time_calculation(scan_blocks, rush_values)
        qb_adj = self._qb_run(times)
        # TODO: Need to return these times somewhere going forward

    def _blocks(self):
        left_block = []
        right_block = []
        center_block = []
        for i in range(self.match.state.cur_off_assignments):
            player = self.match.state.cur_off_players[i]
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.LEFT_BLOCK:
                left_block.append((player.block * 6 + 3 * player.strength + player.positioning) /
                                  (10 + 3 if random.random() > 0.8 else 0 - 3 if random.random() < 0.3 else 0 +
                                   0.5 if random.random() > 0.95 else 0 - 0.5 if random.random() < 0.05 else 0))
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.CENTER_BLOCK:
                pass
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.RIGHT_BLOCK:
                pass
        left_value = combine_values(left_block)
        right_value = combine_values(right_block)
        center_value = combine_values(center_block)
        return {Side.LEFT: left_value, Side.CENTER: center_value, Side.RIGHT: right_value}

    def _rush(self):
        left_rush = []
        right_rush = []
        center_rush = []
        for i in range(self.match.state.cur_def_assignments):
            if self.match.state.cur_off_play.assignments[i] == DefensiveAssignments.LEFT_RUSH:
                left_rush.append(self.match.state.cur_off_players[i].rush)
            if self.match.state.cur_off_play.assignments[i] == DefensiveAssignments.CENTER_RUSH:
                center_rush.append(self.match.state.cur_off_players[i].rush)
            if self.match.state.cur_off_play.assignments[i] == DefensiveAssignments.RIGHT_RUSH:
                right_rush.append(self.match.state.cur_off_players[i].rush)
        left_value = combine_values(left_rush)
        right_value = combine_values(right_rush)
        center_value = combine_values(center_rush)
        return {Side.LEFT: left_value, Side.CENTER: center_value, Side.RIGHT: right_value}

    def _scan(self, block, rush):
        for i in range(self.match.state.cur_off_assignments):
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.SCAN_BLOCK:
                if rush[Side.LEFT] / block[Side.LEFT] > \
                        max(rush[Side.CENTER] / block[Side.CENTER], rush[Side.RIGHT] / block[Side.RIGHT]):
                    pass
                elif rush[Side.RIGHT] / block[Side.RIGHT] > \
                        max(rush[Side.CENTER] / block[Side.CENTER], rush[Side.LEFT] / block[Side.LEFT]):
                    pass
                elif rush[Side.CENTER] / block[Side.CENTER] > \
                        max(rush[Side.RIGHT] / block[Side.RIGHT], rush[Side.LEFT] / block[Side.LEFT]):
                    pass
        return {Side.LEFT: block[Side.LEFT], Side.CENTER: block[Side.CENTER], Side.RIGHT: block[Side.RIGHT]}

    @staticmethod
    def _time_calculation(blocks, rushes):
        return {Side.LEFT: 1, Side.CENTER: 2, Side.RIGHT: 3}

    @staticmethod
    def _qb_run(times):
        # TODO:  Add on extra QB mobility time here
        if min(times[Side.LEFT], times[Side.CENTER]) > times[Side.RIGHT]:
            pass
        elif min(times[Side.RIGHT], times[Side.CENTER]) > times[Side.LEFT]:
            pass
        elif max(times[Side.RIGHT], times[Side.LEFT]) > times[Side.CENTER]:
            pass
        return {Side.LEFT: 1, Side.CENTER: 2, Side.RIGHT: 3}


class Pass(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        if random.random() > 0.5:
            pass
        else:
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
