from copy import deepcopy

from procedures.tackling_procedures import *


class Match:
    def __init__(self, team_1_file, team_1_tacs, team_2_file, team_2_tacs):
        team_1 = MatchPlayer.from_file(team_1_file, team_1_tacs)
        team_2 = MatchPlayer.from_file(team_2_file, team_2_tacs)
        self.state = GameState(deepcopy(team_1), deepcopy(team_2))
        self._commentary = []

    @property
    def required_sets(self):
        return self._required_sets

    def set_commentary(self, comm):
        self._commentary = comm

    def end_match(self):
        # TODO: Report back to the file to have a record of it.  The competition can deal with
        self.record_file_details()
        # TODO: Report back to the player files as well for stuff like fatigue and updating stats
        # TODO: Probably have another file for the stats

    def record_file_details(self):
        print("HERE WE ARE")
        to_print = {"report": self.state.report, "game_scores_1": self.state.player_1.state.games_won_in_match,
                    "games_scores_2": self.state.player_2.state.games_won_in_match,
                    "point_scores_1": self.state.player_1.state.points_won_in_match,
                    "point_scores_2": self.state.player_2.state.points_won_in_match,
                    "statistics player_1": self.state.player_1.statistics.to_file,
                    "statistics player_2": self.state.player_2.statistics.to_file,
                    "commentary": self._commentary}
        with open(self._file_name, "w") as comm_file:
            yaml.safe_dump(to_print, comm_file)
        # TODO: Match scores,game by game
        # TODO: Winner in an easy to read format
        # TODO: Stats like aces etc.  Where are these stored to begin with
        # TODO: The report for the commentary (Outcomes)
        # TODO: Turn all these actions into Procedures at some stage

    def step(self):
        """
        Runs the match by taking from the stack
        :return:
        """
        EndGameProc(self)
        PreGameProc(self)

        while True:
            # Check if the game is over
            if self.state.is_empty:
                return {self.state.player_1.id: self.state.player_1.state.games_won_in_match,
                        self.state.player_2.id: self.state.player_2.state.games_won_in_match}

            # Check the next item on the stack and run it.
            proc = self.state.peek
            # Do action
            self.state.pop()
            proc.step()


class GameState:
    # Keeps track of the sets, games,points played as well as the stack of actions and the balance of a given point
    def __init__(self, team_1, team_2):
        self._set_number = 0
        self._stack = Stack()
        self._server = None
        self._reports = []
        self._first_serve_point = None
        self._game_number = 0
        self._point_number = 0
        self._balance = 0
        self._player_1 = player_1
        self._player_2 = player_2
        self._outcome = None

    def set_comm_values(self, outcome=None):
        self._outcome = outcome

    @property
    def outcome(self):
        return self._outcome

    def first_serve(self):
        self._first_serve_point = Service.FIRST_SERVE

    def second_serve(self):
        self._first_serve_point = Service.SECOND_SERVE

    @property
    def service(self):
        return self._first_serve_point

    @property
    def balance(self):
        return self._balance

    @property
    def report(self):
        return [self._reports[i].to_yaml() for i in range(len(self._reports))]

    @property
    def report_pure(self):
        return self._reports

    @property
    def set_number(self):
        return self._set_number

    @property
    def server(self):
        if self._server == ServerOutcome.PLAYER_1:
            return self._player_1
        elif self._server == ServerOutcome.PLAYER_2:
            return self._player_2

    @property
    def stack_size(self):
        return self._stack.size()

    @property
    def returner(self):
        if self._server == ServerOutcome.PLAYER_1:
            return self._player_2
        elif self._server == ServerOutcome.PLAYER_2:
            return self._player_1

    @property
    def player_1(self):
        return self._player_1

    @property
    def player_2(self):
        return self._player_2

    @property
    def is_empty(self):
        return self._stack.is_empty

    def set_server(self, server_style):
        self._server = server_style

    def pop(self):
        self._stack.pop()

    def append_report(self, item):
        self._reports.append(item)

    @property
    def peek(self):
        return self._stack.peek

    def set_balance(self, value):
        self._balance = value

    def push(self, step):
        self._stack.push(step)

    @property
    def items(self):
        return self._stack.items

    def end_game(self):
        self.change_server()
        self._game_number += 1

    def end_set(self):
        self._set_number += 1
        self._game_number = 0

    def change_server(self):
        if self._server == ServerOutcome.PLAYER_1:
            self._server = ServerOutcome.PLAYER_2
        else:
            self._server = ServerOutcome.PLAYER_1

    def update_previous_score(self, new_score):
        self._reports[-1].update_score(new_score)


class PractiseMatch(Match):
    def __init__(self, sets, player_1_file, player_2_file, file_name,
                 player_1_tacs, player_2_tacs, final_set_tie_break=True):
        super().__init__(sets, player_1_file, player_2_file, file_name,
                         player_1_tacs, player_2_tacs, final_set_tie_break)
        player_1 = PractisePlayer.from_file(player_1_file, player_1_tacs)
        player_2 = PractisePlayer.from_file(player_2_file, player_2_tacs)
        self.state = MatchState(deepcopy(player_1), deepcopy(player_2))
