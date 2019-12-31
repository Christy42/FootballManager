from procedures.procedure import Procedure


class YAC(Procedure):
    def __init__(self, match, runner, tackler):
        super().__init__(match)
        self._runner = runner
        self._tackler = tackler

    def step(self):
        max(0, self._runner.strength + self._runner.carrying - self._tackler - self._tackler)


class Tackling(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass


class Fumble(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass
