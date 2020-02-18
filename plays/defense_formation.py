class DefenseFormation:
    def __init__(self, no_dl, no_lb, no_cb, no_sf):
        self._no_dl = no_dl
        self._no_lb = no_lb
        self._no_cb = no_cb
        self._no_sf = no_sf

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
FOUR_FOUR = DefenseFormation(4, 4, 2, 1)
THREE_FOUR = DefenseFormation(3, 4, 2, 2)
FOUR_THREE = DefenseFormation(4, 3, 2, 2)
NICKEL = DefenseFormation(4, 2, 3, 2)
DIME = DefenseFormation(4, 1, 4, 2)
