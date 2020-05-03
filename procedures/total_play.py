from procedures.procedure import Procedure
from procedures.choose_play import CoinFlip, ChoosePlay
from procedures.clock_procedure import ChoosePlayers
from procedures.end_play import EndPlay


class AssignDefense(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        for i in range(len(self.match.state.cur_def_players)):
            self.match.state.cur_def_play.assignments[i].amend_area(self.match.state.cur_off_play.routes)


class FullPlay(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        Restart(self.match)
        EndPlay(self.match)
        AssignDefense(self.match)
        ChoosePlayers(self.match)
        ChoosePlay(self.match)
        CoinFlip(self.match)


class Restart(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        Restart(self.match)
        EndPlay(self.match)
        AssignDefense(self.match)
        ChoosePlayers(self.match)
        ChoosePlay(self.match)
