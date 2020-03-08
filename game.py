from copy import deepcopy
import math
from random import randint, choices

from stack import Stack
from enums import Possession, PlayStyle, Position
from team.team import MatchTeam
from procedures.total_play import FullPlay


class Match:
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

        while True:
            # Check if the game is over
            if self.state.is_empty:
                return {self.state.team_1.id_no: self.state.team_1.state.score,
                        self.state.team_2.id_no: self.state.team_2.state.score}

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
        self._team_1_pace = 25
        self._team_2_pace = 25
        self._down = 1
        self._turnover = 0
        self._temp_yards = 0
        self._outcome = None
        self._reports = []
        self.cur_off_play = None
        self.cur_def_play = None
        self.tackler = 0
        self._initial = None
        self.cur_off_players = []
        self.cur_def_players = []

    def set_players(self):
        # Offense
        for position in [Position.OT, Position.OG, Position.C, Position.WR, Position.TE, Position.FB, Position.QB,
                         Position.P, Position.K, Position.G]:
            for i in range(self.cur_off_play.formation.positions[position]):
                self.cur_off_players.append(choices(self.offense.players[position],
                                                    self.offense.player_weights[position])[0])

        for position in [Position.DE, Position.DT, Position.OLB, Position.MLB, Position.CB, Position.S, Position.N,
                         Position.KR, Position.PR]:
            for i in range(self.cur_def_play.formation.positions[position]):
                self.cur_def_players.append(choices(self.defense.players[position],
                                                    self.defense.player_weights[position])[0])

    def set_comm_values(self, outcome=None):
        self._outcome = outcome

    def blue_flag(self):
        self._turnover = 1

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
        self._ball_location = round(self._temp_yards + self._ball_location, 2)
        print("loc " + str(self._ball_location))
        print("possession " + str(self._possession))
        print("down " + str(self._down))
        if self._ball_location >= self._first_down_marker:
            self._first_down_marker = min(100, self._ball_location + 10)
            self.reset_down()
        else:
            self.iterate_down()
        self._temp_yards = 0
        self.tackler = 0

    def end_play_checks(self):
        self.flush_temp_yards()
        self._touchback_check()
        self._turnover_check()
        self._safety_check()
        self._td_check()
        # Doubling up here a bit makes this difficult

        if self.cur_off_play.style == PlayStyle.RUN and self._possession == 0:
            self.add_time(min(self._team_1_pace if self._possession == 0 else self._team_2_pace + randint(5, 10), 40))
        else:
            # TODO: Need to deal with catches in bounds or out of bounds.  Maybe this goes elsewhere?
            self.add_time(randint(5, 10))

    def _turnover_check(self):
        if self._turnover == 1:
            self._turnover = 0
            self.reset_down()
            self._ball_location = 100 - self._ball_location
            self._switch_possession()

    def _switch_possession(self):
        self._possession = (self._possession + 1) % 2

    def _td_check(self):
        if self._ball_location > 100:
            if self._possession == 0:
                self.team_1.state.add_score(6)
            else:
                self.team_2.state.add_score(6)
            self._ball_location = 35
            self._switch_possession()
            # TODO: Need to restart here, Need the extra point attempt here as well

    def _safety_check(self):
        if self._turnover == 0 and self._ball_location < 0:
            if self._possession == 0:
                self.team_2.state.add_score(2)
            else:
                self.team_1.state.add_score(2)
                # TODO: Safety punt

    def _touchback_check(self):
        if self._turnover == 1 and self._ball_location > 100:
            self._ball_location = 80

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
        if self._down == 4:

            self.blue_flag()
        self._down = self._down % 4 + 1

    def set_initial(self, a):
        self._initial = a

    def reset_down(self):
        self._down = 1

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
        dfa = self._time.increase_time(time_used)
        print("dfa " + str(dfa))
        if dfa == 1:
            print("The half is changing")
            self.set_possession((self._initial + 1) % 2)
            self._ball_location = 35

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


b = Match("sample//team1.yaml", "sample//team1tactics.yaml", "sample//team2.yaml", "sample//team2tactics.yaml")
b.step()
print(b.state.possession)
# for player in b.state.cur_def_players:
#    print(player[0].name)
# print("XXXXXXXXXXXXXX")
# for player in b.state.cur_off_players:
#     print(player[0].name)
print("XXXX")
print(b.state.team_1.state.score)
print(b.state.team_2.state.score)
