from procedures.procedure import Procedure


class EndPlay(Procedure):
    # TODO: I guess calls a figure next play function which then calls run or pass etc. as appropriate
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        # TODO: Need to turn temp yards into real yards, recalculate down and distance.  Deal with TD/ Safety
        self.match.state.end_play_checks()
