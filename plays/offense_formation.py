class OffenseFormation:
    def __init__(self, no_tes, no_wrs, no_rbs, shotgun):
        self._no_tes = no_tes
        self._no_wrs = no_wrs
        self._no_rbs = no_rbs
        self._shotgun = shotgun

    @property
    def no_tes(self):
        return self._no_tes

    @property
    def no_wrs(self):
        return self._no_wrs

    @property
    def no_rbs(self):
        return self._no_rbs


# TODO: Kick formations
SINGLEBACK = OffenseFormation(1, 3, 1, False)
I_FORM = OffenseFormation(1, 2, 2, False)
SHOTGUN = OffenseFormation(1, 3, 1, True)
DOUBLE_TE_SET = OffenseFormation(2, 2, 1, False)
SPREAD = OffenseFormation(0, 4, 1, True)
