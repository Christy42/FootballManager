from copy import deepcopy
import math
from random import randint

from stack import Stack
from enums import Possession, PlayStyle, GenOff
from team.team import MatchTeam
from procedures.run_procedure import Run, YBCRun
from procedures.total_play import FullPlay, Restart, EndPlay, ChoosePlayers, ChoosePlay, CoinFlip
from procedures.clock_procedure import RunPlay
from procedures.kick_procedure import KickOff


class Test:
    def __init__(self, team_1_file, team_1_tactics, team_2_file, team_2_tactics):
        team_1 = MatchTeam.from_file(team_1_file, team_1_tactics)
        team_2 = MatchTeam.from_file(team_2_file, team_2_tactics)

        self.state = GameState(deepcopy(team_1), deepcopy(team_2))
        self._commentary = []

    def set_commentary(self, comm):
        self._commentary = comm

    def end_match(self):
        # TODO: Report back to the file to have a record of it.  The competition can deal with
        self.record_file_details()
        # TODO: Report back to the team files as well for stuff like fatigue and updating stats
        # TODO: Probably have another file for the stats

    def record_file_details(self):
        pass

    def step(self):
        """
        Runs the match by taking from the stack
        :return:
        """
        # EndGameProc(self)
        # PreGameProc(self)
        FullPlay(self)
        count = 0
        while True:
            count += 1
            # if count == 10000:
            #     self.state._stack.empty_out()
            # Check if the game is over
            if self.state.is_empty:
                return {self.state.team_1.id_no: self.state.team_1.state.score,
                        self.state.team_2.id_no: self.state.team_2.state.score}

            # Check the next item on the stack and run it.
            # TODO: Need to remove requirement for KickOff
            self.state.kicking = False
            proc = self.state.peek

            # Do action
            self.state.pop()
            # TODO: Each action should affect the game clock and the ball location
            # TODO: Do we need something checking the game clock for end of game / half etc.?
            # print(proc)
            proc.step()


class GameState:
    # Keeps track of the sets, games, points played as well as the stack of actions and the balance of a given point
    def __init__(self, team_1, team_2):
        self._yards_counted = 0
        self._actions_done = 0
        self._stack = Stack()
        self._possession = None
        self._ball_location = 35
        self._tackles = 0
        self.stats = {}
        self._tackles_broken = 0
        self._first_down_marker = 45
        self._team_1 = team_1
        self._team_2 = team_2
        self._time = GameTime()
        self._qb_time = 0
        self._team_1_pace = 25
        self._pass_effect = 0
        self._team_2_pace = 25
        self._down = 1
        self.routes_ran = {GenOff.REC1: 0, GenOff.REC4: 0, GenOff.REC3: 0, GenOff.REC2: 0, GenOff.REC5: 0}
        self._turnover = 0
        self._temp_yards = 0
        self._outcome = None
        self._reports = []
        self.cur_off_play = None
        self.cur_def_play = None
        self.tackler = 0
        self._initial = None
        self.cur_off_players = {}
        self.cur_def_players = []
        self.kicking = False
        self._max_run = 0
        self._int_players = {}

    @property
    def int_players(self):
        return self._int_players

    def set_int_players(self, players):
        self._int_players = players

    def set_qb_time(self, value):
        self._qb_time = value

    @property
    def qb_time(self):
        return self._qb_time

    def set_ball_loc(self, placement):
        self._ball_location = 35

    def set_comm_values(self, outcome=None):
        self._outcome = outcome

    def blue_flag(self):
        self._turnover = 0

    @property
    def offense(self):
        if self._possession == 0:
            return self.team_1
        return self.team_2

    @property
    def defense(self):
        if self._possession == 1:
            return self.team_1
        return self.team_2

    @property
    def temp_yards(self):
        return self._temp_yards

    def add_temp_yards(self, tmp):
        self._temp_yards += tmp

    def flush_temp_yards(self):
        print("THIS Updates everything")
        self._yards_counted += self._temp_yards
        print(self._yards_counted)
        print(self._temp_yards)
        self._max_run = max(self._max_run, self._temp_yards)
        self._ball_location = 35
        self._temp_yards = 0
        self._actions_done += 1
        if self._actions_done == 10000:
            self._stack.empty_out()
        self.tackler = 0
        self._qb_time = 0
        self._int_players = {}
        self.routes_ran = {GenOff.REC1: 0, GenOff.REC4: 0, GenOff.REC3: 0, GenOff.REC2: 0, GenOff.REC5: 0}

    def end_play_checks(self):
        self.flush_temp_yards()

    @property
    def outcome(self):
        return self._outcome

    @property
    def offense_formation(self):
        return self.cur_off_play.formation

    @property
    def defense_formation(self):
        return self.cur_def_play.formation

    def iterate_down(self):
        self._down = self._down % 4

    def set_initial(self, a):
        self._initial = a

    @property
    def ball_position(self):
        return self._ball_location

    @property
    def down(self):
        return self._down

    @property
    def team_1(self):
        return self._team_1

    @property
    def team_2(self):
        return self._team_2

    @property
    def qtime(self):
        return self._time.game_time

    def add_time(self, time_used):
        dfa = self._time.increase_time(0)

    @property
    def report(self):
        return [self._reports[i].to_yaml() for i in range(len(self._reports))]

    @property
    def report_pure(self):
        return self._reports

    @property
    def stack_size(self):
        return self._stack.size()

    @property
    def is_empty(self):
        return self._stack.is_empty

    @property
    def possession(self):
        return self._possession

    def set_possession(self, possession):
        self._possession = possession

    def pop(self):
        self._stack.pop()

    def append_report(self, item):
        self._reports.append(item)

    def set_pass_effect(self, value):
        self._pass_effect = value

    @property
    def pass_effect(self):
        return self._pass_effect

    @property
    def peek(self):
        return self._stack.peek

    def push(self, step):
        self._stack.push(step)

    @property
    def items(self):
        return self._stack.items

    def turnover(self):
        if self._possession == Possession.TEAM_1:
            self._possession = Possession.TEAM_2
        else:
            self._possession = Possession.TEAM_1

    def update_previous_score(self, new_score):
        self._reports[-1].update_score(new_score)


class GameTime:
    def __init__(self):
        self._half = 1
        self._quarter = 1
        self._minutes = 0
        self._seconds = 0

    @property
    def game_time(self):
        return self._minutes, self._seconds

    @property
    def quarter(self):
        return self._quarter

    def increase_time(self, seconds):
        self._minutes += math.floor((self._seconds + seconds) / 60)
        self._seconds = (self._seconds + seconds) % 60
        if self._minutes >= 15:
            self._minutes = 0
            self._seconds = 0
            self._quarter += 1
            print("quarter " + str(self._quarter))
            if self._quarter == 3:
                print("XChange")
                self._half += 1
                return 1
                # TODO: How to reset the half????
        return 0

    def reset_time(self):
        self._minutes = 0
        self._seconds = 0


b = Test("sample//team1.yaml", "sample//team1tactics.yaml", "sample//team2.yaml", "sample//team2tactics.yaml")
b.step()
print(b.state.possession)

print("XXXX")
# Need to ensure this is limited to just the run actions
print(b.state._actions_done)
print(b.state._yards_counted / b.state._actions_done)
print(b.state.stats)
print({a: b.state.stats[a] / 10000 for a in b.state.stats})
