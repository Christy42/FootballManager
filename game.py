from copy import deepcopy
import math

from stack import Stack
from enums import Possession
from team.team import MatchTeam


class Match:
    def __init__(self, team_1_file, team_1_tacs, team_2_file, team_2_tacs):
        team_1 = MatchTeam.from_file(team_1_file, team_1_tacs)
        team_2 = MatchTeam.from_file(team_2_file, team_2_tacs)
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

        while True:
            # Check if the game is over
            if self.state.is_empty:
                return {self.state.team_1.id: self.state.team_1.state.score,
                        self.state.team_2.id: self.state.team_2.state.score}

            # Check the next item on the stack and run it.
            proc = self.state.peek
            # Do action
            self.state.pop()
            # TODO: Each action should affect the game clock and the ball location
            # TODO: Do we need something checking the game clock for end of game / half etc.?
            proc.step()


class GameState:
    # Keeps track of the sets, games, points played as well as the stack of actions and the balance of a given point
    def __init__(self, team_1, team_2):
        self._stack = Stack()
        self._possession = None
        self._ball_location = 35
        self._first_down_marker = 45
        self._team_1 = team_1
        self._team_2 = team_2
        self._time = GameTime()
        self._offense_formation = ""
        self._defense_formation = ""
        self._down = 1
        self._turnover = 0
        self._temp_yards = 0
        self._quarter = 1
        self._outcome = None
        self._reports = []
        self._cur_off_play = None
        self._cur_def_play = None
        self._cur_off_players = []
        self._cur_Def_players = []

    def set_comm_values(self, outcome=None):
        self._outcome = outcome

    @property
    def temp_yards(self):
        return self._temp_yards

    def add_temp_yards(self, tmp):
        self._temp_yards += tmp

    def flush_temp_yards(self):
        self._ball_location += self._temp_yards
        if self._ball_location >= self._first_down_marker:
            self._first_down_marker = min(100, self._ball_location + 10)
            self.reset_down()
        else:
            self.iterate_down()
        self._temp_yards = 0

    def end_play_checks(self):
        self._touchback_check()
        self._turnover_check()
        self._safety_check()
        self._td_check()

    def _turnover_check(self):
        if self._turnover == 1:
            self._turnover = 0
            self.reset_down()
            self._ball_location = 100 - self._ball_location
            # TODO: Turn over possession

    def _td_check(self):
        if self._ball_location > 100:
            if self._possession == 0:
                self.team_1.add_points(6)
            # TODO: Need to restart here, Need the extra point attempt here as well
            return True

    def _safety_check(self):
        if self._turnover == 0 and self._ball_location < 0:
            return True

    def _touchback_check(self):
        if self._turnover == 1 and self._ball_location > 100:
            return True

    @property
    def outcome(self):
        return self._outcome

    @property
    def offense_formation(self):
        return self._offense_formation

    @property
    def defense_formation(self):
        return self._defense_formation

    def iterate_down(self):
        self._down = self._down % 4 + 1

    def reset_down(self):
        self._down = 1

    @property
    def quarter(self):
        return self._quarter

    @property
    def team_1(self):
        return self._team_1

    @property
    def team_2(self):
        return self._team_2

    @property
    def qtime(self):
        return self._time.game_time

    def increase_quarter(self):
        # TODO: Need to do things for the quarter -> 3 and quarter 5
        self._quarter += 1

    def add_time(self, time_used):
        self._time.increase_time(time_used)
        if self._time.game_time[0] >= 15:
            self.increase_quarter()
            self._time.reset_time()

    @property
    def report(self):
        return [self._reports[i].to_yaml() for i in range(len(self._reports))]

    @property
    def report_pure(self):
        return self._reports

    @property
    def offense(self):
        if self._possession == Possession.TEAM_1:
            return self._team_1
        elif self._possession == Possession.TEAM_2:
            return self._team_2

    @property
    def stack_size(self):
        return self._stack.size()

    @property
    def defense(self):
        if self._possession == Possession.TEAM_1:
            return self._team_2
        elif self._possession == Possession.TEAM_2:
            return self._team_1

    @property
    def is_empty(self):
        return self._stack.is_empty

    def set_possession(self, possession):
        self._possession = possession

    def pop(self):
        self._stack.pop()

    def append_report(self, item):
        self._reports.append(item)

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
        self._minutes = 0
        self._seconds = 0

    @property
    def game_time(self):
        return self._minutes, self._seconds

    def increase_time(self, seconds):
        self._minutes += math.floor((self._seconds + seconds) / 60)
        self._seconds = (self._seconds + seconds) % 60

    def reset_time(self):
        self._minutes = 0
        self._seconds = 0
