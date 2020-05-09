from procedures.tackling_procedures import *
from enums import Side, GenOff
from utils import combine_values, repeated_random
# import game as g

from plays.route import *


class RouteRun(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        # Needs where the players are targeting really.
        # Take the final target by themselves.  Combine the rest a bit.
        # Work out check_down
        routes_effect = {a: 0 for a in self.match.state.cur_off_play.route.reads}
        for i in self.match.state.cur_off_play.route.reads:
            dist_effect = round(self.match.state.cur_off_play.route.assignments[i].value / 5) + 2
            routes_effect[i] += (self.match.state.cur_off_players[i].speed * dist_effect +
                                 (8 - dist_effect) * self.match.state.cur_off_players[i].route_running) / 8
            # Need Coverage
            # Surely type of route should affect this heavily?  Maybe base off the level it goes to?
            # Or just get what you can done
            for j in range(len(self.match.state.cur_off_play.route.reads)):
                if i != j:
                    dist_effect = round(self.match.state.cur_off_play.route.assignments[i].value / 5) + 2
                    routes_effect[i] += (self.match.state.cur_off_players[i].speed * dist_effect +
                                         (8 - dist_effect) * self.match.state.cur_off_players[i].route_running) / 32
                    # helping out
                    # Now I need to go from REC1 to Julio Jones or whoever
        # Receiver 1-> some help from 2 and maybe 3
        # Receiver 2, some help from 1 and maybe 3
        # Receiver 3, some help from 1 and 2
        self.match.state.route_effect = routes_effect


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
        blocks = {Side.LEFT: [], Side.CENTER: [], Side.RIGHT: []}
        for side in [Side.LEFT, Side.CENTER, Side.RIGHT]:
            for i in GenOff:
                player = self.match.state.cur_off_players[i]
                if self.match.state.cur_off_play.assignments[i].side == side:
                    blocks[side].append((player.block * 6 * player.burst / 1000 + 3 * player.strength +
                                         player.positioning * player.burst / 1000) /
                                        (13 + 5 if random.random() > 0.9 else 0 - 5 if random.random() < 0.1 else 0 +
                                         0.5 if random.random() > 0.95 else 0 - 0.5 if random.random() < 0.05 else 0))
        return {Side.LEFT: combine_values(blocks[Side.LEFT]),
                Side.CENTER: combine_values(blocks[Side.CENTER]),
                Side.RIGHT: combine_values(blocks[Side.RIGHT])}

    def _rush(self) -> dict:
        rushes = {Side.LEFT: [], Side.CENTER: [], Side.RIGHT: []}
        for side in Side:
            for i in range(self.match.state.cur_def_assignments):
                player = self.match.state.cur_def_players[i]
                assignment = self.match.state.cur_def_play.assignments[i]
                if assignment.side == side and assignment.blitz:
                    rushes[side].append((player.rush * 6 * player.burst / 1000 + 3 * player.strength +
                                         player.speed * player.burst / 1000) /
                                        (13 + 5 if random.random() > 0.9 else 0 - 5 if random.random() < 0.1 else 0 +
                                         0.5 if random.random() > 0.95 else 0 - 0.5 if random.random() < 0.05 else 0))
        return {Side.LEFT: combine_values(rushes[Side.LEFT]), Side.CENTER: combine_values(rushes[Side.CENTER]),
                Side.RIGHT: combine_values(rushes[Side.RIGHT])}

    def _scan(self, block, rush) -> dict:
        effect = [rush[j] / block[j] for j in [Side.LEFT, Side.CENTER, Side.RIGHT]]
        vision_scan = Side.LEFT if effect[0] == max(effect) else Side.CENTER if effect[1] == max(effect) else Side.Right

        for i in GenOff:
            if self.match.state.cur_off_play.assignments[i] == BLOCK_SCAN:
                player = self.match.state.cur_def_players[i]
                block[vision_scan] += (player.vision * player.block * player.positioning / 6000000 +
                                       player.strength * player.positioning / 6000) if random() * 2000 < \
                                       500 + player.vision else 0
        return {Side.LEFT: block[Side.LEFT], Side.CENTER: block[Side.CENTER], Side.RIGHT: block[Side.RIGHT]}

    @staticmethod
    def _time_calculation(blocks: dict, rushes: dict) -> dict:
        times = {a: repeated_random(32, blocks[a] / rushes[a]) / 10 + 1.8 for a in blocks}
        return times

    def _qb_run(self, times: dict) -> dict:

        scan = max(times, key=times.get)
        new_times = {x: times[x] for x in times}
        player = self.match.state.cur_off_players[GenOff.QB]
        max_speed = 0
        for i in range(self.match.state.cur_def_assignments):
            max_speed = self.match.state.cur_def_players[i].rush * self.match.state.cur_def_players[i].speed \
                if self.match.state.cur_off_play.assignments[i] == scan else 0

        new_times[scan] = new_times[scan] + repeated_random(20, min(0.5, player.speed * player.awareness /
                                                                    (10 * max_speed))) / 10
        return new_times


class Pass(Procedure):
    def __init__(self, match, receiver):
        super().__init__(match)
        self._receiver = receiver

    def step(self):
        distance = BACK_CENTER.distance(self.match.state.cur_off_players[self._receiver].route.field_loc)
        # TODO: Use passing, distance from QB, awareness for accuracy, coverage values for difficulty
        if distance > self.match.state.cur_off_players[GenOff.QB].passing:
            pass
        else:
            pass


class DecisionMade(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        qb = self.match.state.cur_off_players[GenOff.QB]
        times = self.match.state.cur_off_play.route.times
        qb_time = min(self.match.state.qb_time.values())
        qb_time -= random() / 2 * (1 - qb.awareness / 1000)
        # Figure out right route.
        r_values = {}
        multi = 50  # used to favour initial reads
        for i in self.match.state.cur_off_play.route.reads:
            r_values.update({i: self.match.state.route_effect[i] * multi * (random() / 2 + 0.5)})
            multi = multi * 0.75
        r_values = {a: r_values[a] / sum(r_values.values()) for a in r_values}
        read = max(r_values, key=r_values.get)
        # Look to checkdown
        if max(r_values) < 100:
            # TODO: Adjust these numbers
            # Take sack
            if min(times) < 1.5:
                self.match.state.add_temp_yards(-5)
                return
            Pass(self.match, self.match.state.cur_off_play.route.checkdown)
        Pass(self.match, read)
        # Need time QB has
        # Need the time the routes take
        # Check reads, work out which is right (50, 30, 20) or (60, 40) of them being the right read) or dump off
        # Call pass attempt or call sack (or call QB run eventually) or take? sack


class AfterCatch(Procedure):
    def __init__(self, match, receiver):
        super().__init__(match)
        self._rec = receiver

    def step(self):
        if random() < 1:
            self.match.state.add_temp_yards(0)
        else:
            # TODO: How to decide on tackler
            self.match.state.add_temp_yards(self.match.state.cur_off_play.route.distance[self._rec])
            Tackling(self.match, self._rec, )