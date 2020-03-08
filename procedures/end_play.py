from procedures.procedure import Procedure


class EndPlay(Procedure):
    # TODO: I guess calls a figure next play function which then calls run or pass etc. as appropriate
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        # TODO: Need to turn temp yards into real yards, recalculate down and distance.  Deal with TD/ Safety
        print("result")
        print(self.match.state._time.game_time)
        print(self.match.state._time.quarter)
        print("end_res")
        self.match.state.end_play_checks()
        if self.match.state._time.quarter >= 5:
            EndGame(self.match)


class EndGame(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        self.match.state._stack.empty_out()
