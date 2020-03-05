from procedures.procedure import Procedure

import random
import time


class CoinFlip(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        if random.randint(0, 1) == 0:
            self.match.state.set_possession(0)
        else:
            self.match.state.set_possession(1)


class ChoosePlay(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        if self.match.state.possession == 0:
            self.match.state.cur_off_play = self.match.state.team_1.choose_play_offense()
            self.match.state.cur_def_play = self.match.state.team_2.choose_play_defense()
        else:
            self.match.state.cur_off_play = self.match.state.team_2.choose_play_offense()
            self.match.state.cur_def_play = self.match.state.team_1.choose_play_defense()
        print("X")
        print(self.match.state._stack.items)
