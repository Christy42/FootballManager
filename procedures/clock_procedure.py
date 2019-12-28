from procedures.procedure import Procedure


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
