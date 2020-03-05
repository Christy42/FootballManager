from procedures.procedure import Procedure
from procedures.run_procedure import Run
from enums import PlayStyle


class EndQuarter(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class EndHalf(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class TimeOut(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class RunClock(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class ChoosePlayers(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        if self.match.state.possession == 0:
            self.match.state.cur_off_players = \
                self.match.state.team_1.choose_offense(self.match.state.cur_off_play.formation)
            self.match.state.cur_def_players = self.match.state.team_2.choose_defense(self.match.state.cur_def_play.formation)
        else:
            self.match.state.cur_off_players = \
                self.match.state.team_2.choose_offense(self.match.state.cur_off_play.formation)
            self.match.state.cur_def_players = \
                self.match.state.team_1.choose_defense(self.match.state.cur_def_play.formation)
        RunPlay(self.match)


class RunPlay(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        # I guess something for if we have a run play or a pass play.
        if self.match.state.cur_off_play.style == PlayStyle.RUN:
            Run(self.match)
        elif self.match.state.cur_off_play.style == PlayStyle.PASS:
            pass
        elif self.match.state.cur_off_play.style == PlayStyle.SPECIAL:
            pass
