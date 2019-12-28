from procedures.tackling_procedures import *
from enums import Side, RunStyle


# TODO: What types of run are there?  How do they differ.  Probably don't need new ones for each side
# TODO: Add more types of run but get these working first
class Run(Procedure):
    def __init__(self, match, side):
        super().__init__(match)
        self._side = side
        self._blockers = []

    def step(self):
        pass

    def ybc(self):
        pass

    def broken_tackle(self):
        pass


# TODO: More exp, agility based.  Bigger gains, bigger losses.
# TODO: So who is involved.  Full Back (maybe) and 5 linemen vs  DL and blitzers...
class ZoneBlockRun(Run):
    def __init__(self, match, side):
        super().__init__(match, side)

    def step(self):
        if self.match.state.offense_formation in []:
            self._blockers = []
        else:
            self._blockers = []
        block_power = self.blocking()
        def_power = self.rush()

    def blocking(self):
        if self._side == Side.LEFT:
            return 1
        elif self._side == Side.CENTER:
            return 2
        else:
            return 3

    def rush(self):
        if self._side == Side.LEFT:
            return 1
        elif self._side == Side.CENTER:
            return 2
        else:
            return 3


# TODO: Less exp based.  Smaller gains, smaller losses.
class ManBlockRun(Run):
    def __init__(self, match, side):
        super().__init__(match, side)
        pass

    def step(self):
        pass


# TODO: I mean, returns a number but doesn't do very much???
# Could I have a YBC stat?  But that doesn't really affect the
class YBCRun(Procedure):
    def __init__(self, match, style, side):
        super().__init__(match)
        self._side = side
        self._style = style

    def step(self):
        pass

    def blocking(self):
        if self._side == Side.LEFT:
            return 1
        elif self._side == Side.CENTER:
            return 2
        else:
            return 3

    def rush(self):
        if self._side == Side.LEFT:
            return 1
        elif self._side == Side.CENTER:
            return 2
        else:
            return 3
