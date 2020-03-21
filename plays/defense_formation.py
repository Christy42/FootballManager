class DefenseFormation:
    def __init__(self, no_dl=0, no_lb=0, no_cb=0, no_sf=0, no_kr=0):
        self._no_dl = no_dl
        self._no_lb = no_lb
        self._no_cb = no_cb
        self._no_sf = no_sf
        self._no_kr = no_kr

    @property
    def no_kr(self):
        return self._no_kr

    @property
    def no_dl(self):
        return self._no_dl

    @property
    def no_lb(self):
        return self._no_lb

    @property
    def no_cb(self):
        return self._no_cb

    @property
    def no_sf(self):
        return self._no_sf


# TODO: Need kick formations
FOUR_FOUR = DefenseFormation(no_dl=4, no_lb=4, no_cb=2, no_sf=1)
THREE_FOUR = DefenseFormation(no_dl=3, no_lb=4, no_cb=2, no_sf=2)
FOUR_THREE = DefenseFormation(no_dl=4, no_lb=3, no_cb=2, no_sf=2)
NICKEL = DefenseFormation(no_dl=4, no_lb=2, no_cb=3, no_sf=2)
DIME = DefenseFormation(no_dl=4, no_lb=1, no_cb=4, no_sf=2)
KICK_RETURN = DefenseFormation(no_cb=4, no_lb=4, no_kr=1, no_sf=0)
