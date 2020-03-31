from procedures.procedure import Procedure
from procedures.choose_play import CoinFlip, ChoosePlay
from procedures.clock_procedure import ChoosePlayers
from procedures.end_play import EndPlay


class FullPlay(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        Restart(self.match)
        EndPlay(self.match)
        ChoosePlayers(self.match)
        ChoosePlay(self.match)
        CoinFlip(self.match)


class Restart(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        Restart(self.match)
        EndPlay(self.match)
        ChoosePlayers(self.match)
        ChoosePlay(self.match)
