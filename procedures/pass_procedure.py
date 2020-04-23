from procedures.tackling_procedures import *
from enums import OffensiveAssignments, DefensiveAssignments, Side
from utils import combine_values


class RouteRun(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        # Needs where the players are targeting really.
        # Take the final target by themselves.  Combine the rest a bit.
        # Work out check_down
        for i in range(len(self.match.state.cur_off_play.route.reads)):
            # Main route run
            for j in range(len(self.match.state.cur_off_play.route.reads)):
                if i != j:
                    # helping out
                    # Now I need to go from REC1 to Julio Jones or whoever
                    pass
        # Receiver 1-> some help from 2 and maybe 3
        # Receiver 2, some help from 1 and maybe 3
        # Receiver 3, some help from 1 and 2
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
        self.match.state.set_qb_time(min(qb_adj.values()))
        # TODO: Need to return these times somewhere going forward

    def _blocks(self) -> dict:
        blocks = {OffensiveAssignments.LEFT_BLOCK: [], OffensiveAssignments.CENTER_BLOCK: [],
                  OffensiveAssignments.RIGHT_BLOCK: []}
        for side in [OffensiveAssignments.LEFT_BLOCK,
                     OffensiveAssignments.CENTER_BLOCK, OffensiveAssignments.RIGHT_BLOCK]:
            for i in range(self.match.state.cur_off_assignments):
                player = self.match.state.cur_off_players[i]
                if self.match.state.cur_off_play.assignments[i] == side:
                    blocks[side].append((player.block * 6 * player.burst / 1000 + 3 * player.strength +
                                         player.positioning * player.burst / 1000) /
                                        (13 + 5 if random.random() > 0.9 else 0 - 5 if random.random() < 0.1 else 0 +
                                         0.5 if random.random() > 0.95 else 0 - 0.5 if random.random() < 0.05 else 0))

        return {Side.LEFT: combine_values(blocks[OffensiveAssignments.LEFT_BLOCK]),
                Side.CENTER: combine_values(blocks[OffensiveAssignments.CENTER_BLOCK]),
                Side.RIGHT: combine_values(blocks[OffensiveAssignments.RIGHT_BLOCK])}

    def _rush(self) -> dict:
        rushes = {DefensiveAssignments.LEFT_RUSH: [], DefensiveAssignments.CENTER_BLOCK: [],
                  DefensiveAssignments.RIGHT_BLOCK: []}
        for side in [DefensiveAssignments.LEFT_RUSH,
                     DefensiveAssignments.CENTER_RUSH, DefensiveAssignments.RIGHT_RUSH]:
            for i in range(self.match.state.cur_def_assignments):
                player = self.match.state.cur_def_players[i]
                if self.match.state.cur_off_play.assignments[i] == side:
                    rushes[side].append((player.rush * 6 * player.burst / 1000 + 3 * player.strength +
                                         player.speed * player.burst / 1000) /
                                        (13 + 5 if random.random() > 0.9 else 0 - 5 if random.random() < 0.1 else 0 +
                                         0.5 if random.random() > 0.95 else 0 - 0.5 if random.random() < 0.05 else 0))
        return {Side.LEFT: combine_values(rushes[DefensiveAssignments.LEFT_RUSH]),
                Side.CENTER: combine_values(rushes[DefensiveAssignments.CENTER_RUSH]),
                Side.RIGHT: combine_values(rushes[DefensiveAssignments.RIGHT_RUSH])}

    def _scan(self, block, rush) -> dict:
        effect = [rush[j] / block[j] for j in [Side.LEFT, Side.CENTER, Side.RIGHT]]
        vision_scan = Side.LEFT if effect[0] == max(effect) else Side.CENTER if effect[1] == max(effect) else Side.Right

        for i in range(self.match.state.cur_off_assignments):
            if self.match.state.cur_off_play.assignments[i] == OffensiveAssignments.SCAN_BLOCK:
                player = self.match.state.cur_def_players[i]
                block[vision_scan] += (player.vision * player.block * player.positioning / 6000000 +
                                       player.strength * player.positioning / 6000) if random() * 2000 < \
                                       500 + player.vision else 0
        return {Side.LEFT: block[Side.LEFT], Side.CENTER: block[Side.CENTER], Side.RIGHT: block[Side.RIGHT]}

    @staticmethod
    def _time_calculation(blocks, rushes) -> dict:
        return {Side.LEFT: 1, Side.CENTER: 2, Side.RIGHT: 3}

    @staticmethod
    def _qb_run(times) -> dict:
        # TODO:  Add on extra QB mobility time here
        scan = max(times, key=times.get)
        new_times = {x: times[x] for x in times}
        return {Side.LEFT: new_times[Side.LEFT], Side.CENTER: new_times[Side.LEFT], Side.RIGHT: new_times[Side.LEFT]}


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
