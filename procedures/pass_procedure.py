from procedures.tackling_procedures import *
from enums import Side, GenOff
from utils import combine_values, repeated_random
# import game as g
from random import choice

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
        int_player = {a: None for a in self.match.state.cur_off_play.routes.reads}
        int_player[self.match.state.cur_off_play.routes.checkdown] = None
        for i in self.match.state.cur_off_play.routes.reads:
            receiver = self.match.state.cur_off_players[i][0]
            coverage_pl = []
            for j in range(len(self.match.state.cur_def_players)):
                if self.match.state.cur_def_play.assignments[j].area == self.match.state.cur_off_play.routes.assignments[i].field_loc:
                    coverage_pl.append(j)
            if len(coverage_pl) > 0:
                int_player[i] = choice(coverage_pl)
            if len(coverage_pl) == 0:
                delayed_cover = True  # coverage late getting there
                for j in range(len(self.match.state.cur_def_players)):
                    if self.match.state.cur_def_play.assignments[j].area.distance(self.match.state.cur_off_play.routes.assignments[i].field_loc) <= 2:
                        coverage_pl.append(j)
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
        checkdown = self.match.state.cur_off_play.routes.checkdown
        self.match.state.set_int_players(int_player)
        self.match.state.route_effect[checkdown] = 1 - self.match.state.cur_off_players[checkdown][0].route_running / 1300 - 0.2


class PassBlock(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        block_values = self._blocks()
        rush_values = self._rush()

        self.match.state.stats["left rush"] = self.match.state.stats.get("left rush", 0) + rush_values[Side.LEFT]
        self.match.state.stats["center rush"] = self.match.state.stats.get("center rush", 0) + rush_values[Side.CENTER]
        self.match.state.stats["right rush"] = self.match.state.stats.get("right rush", 0) + rush_values[Side.RIGHT]
        scan_blocks = self._scan(block_values, rush_values)
        self.match.state.stats["left block"] = self.match.state.stats.get("left block", 0) + scan_blocks[Side.LEFT]
        self.match.state.stats["center block"] = self.match.state.stats.get("center block", 0) + scan_blocks[Side.CENTER]
        self.match.state.stats["right block"] = self.match.state.stats.get("right block", 0) + scan_blocks[Side.RIGHT]
        times = self._time_calculation(scan_blocks, rush_values)
        self.match.state.stats["qb time1"] = self.match.state.stats.get("qb time1", 0) + min(times.values())
        qb_adj = self._qb_run(times)
        self.match.state.set_qb_time(min(qb_adj.values()))
        self.match.state.stats["qb time"] = self.match.state.stats.get("qb time", 0) + min(qb_adj.values())
        self.match.state.stats["left time"] = self.match.state.stats.get("left time", 0) + qb_adj[Side.LEFT]
        self.match.state.stats["center time"] = self.match.state.stats.get("center time", 0) + qb_adj[Side.CENTER]
        self.match.state.stats["right time"] = self.match.state.stats.get("right time", 0) + qb_adj[Side.RIGHT]

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
                                        (10 + (5 if random() > 0.9 else 0) - (5 if random() < 0.1 else 0) +
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
        print("AAAAAA")
        print(blocks)
        print({a: blocks[a] / rushes[a] for a in blocks})
        times = {a: repeated_random(32, blocks[a] / (rushes[a] + blocks[a])) / 10 + 1.8 for a in blocks}
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
        self.match.state.stats["distance"] = self.match.state.stats.get("distance", 0) + distance
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
        times = {a: self.match.state.cur_off_play.routes.timing[a] for a in self.match.state.cur_off_play.routes.timing
                 if a in self.match.state.cur_off_play.routes.reads or
                 a == self.match.state.cur_off_play.routes.checkdown}
        qb_time = self.match.state.qb_time
        qb_time -= random() / 2 * (1 - qb.awareness / 1000)
        self.match.state.stats["qb_time"] = self.match.state.stats.get("qb_time", 0) + qb_time
        self.match.state.stats["qb_times"] = self.match.state.stats.get("qb_times", 0) + 1
        self.match.state.stats["times"] = self.match.state.stats.get("times", 0) + min(times.values())
        self.match.state.stats["mtimes"] = self.match.state.stats.get("mtimes", 0) + max(times.values())
        read_val = {a: 0 for a in self.match.state.cur_off_play.routes.reads}
        for i in range(len(self.match.state.cur_off_play.routes.reads)):
            read_val[self.match.state.cur_off_play.routes.reads[i]] = 100 - i * 25
        read_val[self.match.state.cur_off_play.routes.checkdown] = 15
        print(read_val)
        read_val = {a: read_val[a] * (1.1 - self.match.state.route_effect[a]) for a in read_val}
        read_val = {a: read_val[a] + (-200 if times[a] >= qb_time else 0) + (25 if times[a] + (1000 - qb.awareness) / 500 <= qb_time else 0) for a in read_val}
        read_val["sack"] = 0
        read_val = {a: read_val[a] + randint(0, 150 - int(qb.awareness / 10)) for a in read_val}
        print(qb_time)
        print(read_val)
        print("XTimes")
        print(times)

        # Figure out right route.
        read = max(read_val, key=read_val.get)
        print(read)
        self.match.state.stats["pass attempt"] = self.match.state.stats.get("pass attempt", 0) + 1
        if type(read) == str:
            self.match.state.stats["sack"] = self.match.state.stats.get("sack", 0) + 1
            # TODO: Fumble chance: eventually - not vital!!!
            self.match.state.add_temp_yards(-5)
            return
        self.match.state.stats[read] = self.match.state.stats.get(read, 0) + 1
        Passing(self.match, read)


class AfterCatch(Procedure):
    def __init__(self, match, receiver):
        super().__init__(match)
        self._rec = receiver

    def step(self):
        receiver = self.match.state.cur_off_players[self._rec][0]
        catch = random()
        self.match.state.stats["catch attempt"] = self.match.state.stats.get("catch attempt", 0) + 1
        self.match.state.stats["pass eff"] = self.match.state.stats.get("pass eff", 0) + self.match.state.pass_effect
        self.match.state.stats["route eff"] = self.match.state.stats.get("route eff", 0) + self.match.state.route_effect[self._rec]
        self.match.state.stats["route yards"] = self.match.state.stats.get("route yards", 0) + self.match.state.cur_off_play.routes.yards[self._rec]
        if self.match.state.int_players[self._rec] is not None:
            self.match.state.stats["int chance"] = self.match.state.stats.get("int chance", 0) + 1
            defender = self.match.state.cur_def_players[self.match.state.int_players[self._rec]][0]
            qb = self.match.state.cur_off_players[GenOff.QB][0]
            print("TEST INT")
            print(min(self.match.state.route_effect[self._rec] * defender.coverage / qb.passing * 0.45, 0.4) * min(self.match.state.route_effect[self._rec] * defender.coverage / qb.passing * 0.45, 0.4))
            if random() <= min(self.match.state.route_effect[self._rec] * defender.coverage / qb.passing * 0.45, 0.4):
                if random() <= min(self.match.state.route_effect[self._rec] * defender.coverage / qb.passing * 0.45,
                                   0.3):
                    self.match.state.stats["int"] = self.match.state.stats.get("int", 0) + 1
                    self.match.state.blue_flag()
                    self.match.state.add_temp_yards(self.match.state.cur_off_play.routes.yards[self._rec])
                    return
        if catch > 0.98 or catch * 1000 > (receiver.catching + self.match.state.pass_effect) * \
                (1 - self.match.state.route_effect[self._rec]):
            self.match.state.stats["drop"] = self.match.state.stats.get("drop", 0) + 1
            self.match.state.add_temp_yards(0)
        else:
            print("catch")
            # TODO: Need a few potential yards from the pass / catch
            self.match.state.stats["catch"] = self.match.state.stats.get("catch", 0) + 1
            print(self.match.state.cur_off_play.routes.yards)
            self.match.state.add_temp_yards(self.match.state.cur_off_play.routes.yards[self._rec])
            Tackling(self.match, self._rec)
