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
        routes_effect = {a: 0 for a in self.match.state.cur_off_play.routes.reads}
        cov_effect = {a: 0 for a in self.match.state.cur_off_play.routes.reads}
        delayed_cover = False
        for i in self.match.state.cur_off_play.routes.reads:
            receiver = self.match.state.cur_off_players[i][0]
            coverage_pl = []
            for j in range(len(self.match.state.cur_def_players)):
                if self.match.state.cur_def_play.assignments[j].area == self.match.state.cur_off_play.routes.assignments[i].field_loc:
                    coverage_pl.append(j)
            if len(coverage_pl) == 0:
                delayed_cover = True  # coverage late getting there
                for j in range(len(self.match.state.cur_def_players)):
                    if self.match.state.cur_def_play.assignments[j].area.distance(self.match.state.cur_off_play.routes.assignments[i].field_loc) <= 2:
                        coverage_pl.append(j)
            # TODO: Use actual distances here
            dist_effect = round(self.match.state.cur_off_play.routes.assignments[i].yards / 5) + 2
            routes_effect[i] += (receiver.speed * dist_effect + (8 - dist_effect) * receiver.elusiveness +
                                 receiver.awareness * 2 + receiver.route_running * 6) / 16
            for j in range(len(self.match.state.cur_off_play.routes.reads)):
                if i != j:
                    routes_effect[i] += (receiver.speed * dist_effect + (8 - dist_effect) * receiver.elusiveness +
                                         receiver.awareness * 4 + receiver.route_running * 4) / 128
                    # Now I need to go from REC1 to Julio Jones or whoever
            for k in coverage_pl:
                defender = self.match.state.cur_def_players[k][0]
                cov_effect[i] += (defender.awareness * 2 + defender.speed * dist_effect + defender.coverage * 6 +
                                  defender.elusiveness + (8 - dist_effect)) / (16 + 16 * delayed_cover)
        self.match.state.route_effect = {a: cov_effect[a] / (routes_effect[a] + cov_effect[a])
                                         for a in self.match.state.cur_off_play.routes.reads}


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
                player = self.match.state.cur_off_players[i][0]
                if self.match.state.cur_off_play.assignments[i].side == side:
                    blocks[side].append((player.blocking * 6 * player.burst / 1000 + 3 * player.strength +
                                         player.positioning * player.burst / 1000) /
                                        (13 + (5 if random() > 0.9 else 0) - (5 if random() < 0.1 else 0) +
                                         (0.5 if random() > 0.95 else 0) - (0.5 if random() < 0.05 else 0)))
        return {Side.LEFT: combine_values(blocks[Side.LEFT]),
                Side.CENTER: combine_values(blocks[Side.CENTER]),
                Side.RIGHT: combine_values(blocks[Side.RIGHT])}

    def _rush(self) -> dict:
        rushes = {Side.LEFT: [], Side.CENTER: [], Side.RIGHT: []}
        for side in Side:
            for i in range(len(self.match.state.cur_def_play.assignments)):
                player = self.match.state.cur_def_players[i][0]
                assignment = self.match.state.cur_def_play.assignments[i]
                if assignment.side == side and assignment.blitz:
                    rushes[side].append((player.rushing * 6 * player.burst / 1000 + 3 * player.strength +
                                         player.speed * player.burst / 1000) /
                                        (13 + (5 if random() > 0.9 else 0) - (5 if random() < 0.1 else 0) +
                                         (0.5 if random() > 0.95 else 0) - (0.5 if random() < 0.05 else 0)))
        return {Side.LEFT: combine_values(rushes[Side.LEFT]), Side.CENTER: combine_values(rushes[Side.CENTER]),
                Side.RIGHT: combine_values(rushes[Side.RIGHT])}

    def _scan(self, block, rush) -> dict:
        effect = [rush[j] / block[j] for j in [Side.LEFT, Side.CENTER, Side.RIGHT]]
        vision_scan = Side.LEFT if effect[0] == max(effect) else Side.CENTER if effect[1] == max(effect) else Side.RIGHT

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
        player = self.match.state.cur_off_players[GenOff.QB][0]
        max_speed = 0
        for i in range(len(self.match.state.cur_def_play.assignments)):
            max_speed = self.match.state.cur_def_players[i][0].rushing * self.match.state.cur_def_players[i][0].speed \
                if self.match.state.cur_def_play.assignments[i].side == scan else 0

        new_times[scan] = new_times[scan] + repeated_random(20, min(0.5, player.speed * player.awareness /
                                                                    (0.01 + (10 * max_speed)))) / 10
        return new_times


class Pass(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        DecisionMade(self.match)
        RouteRun(self.match)
        PassBlock(self.match)


class Passing(Procedure):
    def __init__(self, match, receiver):
        super().__init__(match)
        self._receiver = receiver

    def step(self):
        distance = BACK_CENTER.distance(self.match.state.cur_off_play.assignments[self._receiver].field_loc)
        qb = self.match.state.cur_off_players[GenOff.QB][0]
        passing = qb.passing * (random() / 2 + 0.75)
        effect = max(min(125 - distance * 25 + (passing - 100) / 6 + randint(-6, 6), 150), 0)
        print("effect")
        print(effect)
        route_effect = self.match.state.route_effect[self._receiver]
        effect += max(min(125 - route_effect * 125 + (qb.passing + qb.awareness - 200) / 12 + randint(-6, 6), 150), 0)
        print(effect)
        self.match.state.set_pass_effect(effect)
        AfterCatch(self.match, self._receiver)


class DecisionMade(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        qb = self.match.state.cur_off_players[GenOff.QB][0]
        times = self.match.state.cur_off_play.routes.timing
        qb_time = self.match.state.qb_time
        qb_time -= random() / 2 * (1 - qb.awareness / 1000)
        # Figure out right route.
        r_values = {}
        multi = 50  # used to favour initial reads
        for i in self.match.state.cur_off_play.routes.reads:
            r_values.update({i: self.match.state.route_effect[i] * multi * (random() / 2 + 0.5)})
            multi = multi * 0.75
        r_values = {a: r_values[a] / sum(r_values.values()) for a in r_values}
        read = max(r_values, key=r_values.get)
        # Look to checkdown
        if max(r_values.values()) < 0.3:
            # TODO: Adjust these numbers
            # Take sack
            print("Sack check")
            print(times)
            print(r_values)
            if min(times.values()) < qb_time:
                # TODO: Eventually adjust sack times
                self.match.state.add_temp_yards(-5)
                return
            Passing(self.match, self.match.state.cur_off_play.route.checkdown)
        Passing(self.match, read)
        # Need time QB has
        # Need the time the routes take
        # Check reads, work out which is right (50, 30, 20) or (60, 40) of them being the right read) or dump off
        # Call pass attempt or call sack (or call QB run eventually) or take? sack


class AfterCatch(Procedure):
    def __init__(self, match, receiver):
        super().__init__(match)
        self._rec = receiver

    def step(self):
        receiver = self.match.state.cur_off_players[self._rec][0]
        catch = random()
        if catch > 0.98 or catch * 1000 > (receiver.catching + self.match.state.pass_effect) * \
                self.match.state.route_effect[self._rec]:
            self.match.state.stats["catch"] = self.match.state.stats.get("catch")
            self.match.state.add_temp_yards(0)
        else:
            print("catch")
            # TODO: How to decide on tackler
            self.match.state.add_temp_yards(self.match.state.cur_off_play.routes.yards[self._rec])
            Tackling(self.match, self._rec, )
